#!/usr/bin/env python3
"""Pull Qualtrics survey responses and open one pull request per new response.

Runs inside a checkout of the PRIVATE feedback repository
(social-science-data-editors/readme-bot-feedback); see feedback/FEEDBACK_PLAN.md.
Each PR adds responses/<date>-<responseId>.md to that repository. A maintainer
includes the response by approving the PR (the feedback repo's merge workflow
merges it); rejecting means closing it.

Environment (from GitHub secrets/variables):
  QUALTRICS_BASE_URL   e.g. https://cornell.ca1.qualtrics.com
  QUALTRICS_API_TOKEN  Qualtrics API token
  QUALTRICS_SURVEY_ID  SV_xxxxxxxxxxxx
  GH_TOKEN             token gh can use to push branches and open PRs

Usage:
  qualtrics_to_prs.py --repo-dir <feedback checkout>     fetch, open PRs
  qualtrics_to_prs.py --from-file x.json --dry-run       test on a saved export
Field mapping: feedback/qualtrics-map.json in readme-bot (override with --map)
Standard library only.
"""

import argparse
import io
import json
import os
import re
import subprocess
import sys
import time
import urllib.request
import zipfile
from pathlib import Path

TOOL_ROOT = Path(__file__).resolve().parent.parent
MAP_FILE = TOOL_ROOT / "feedback" / "qualtrics-map.json"
ROOT = Path.cwd()  # target repo; set from --repo-dir
LABEL = "feedback:response"
EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
MAX_TEXT = 2000


# ---------- Qualtrics ----------

def api(method, path, body=None, raw=False):
    base = os.environ["QUALTRICS_BASE_URL"].rstrip("/")
    req = urllib.request.Request(
        f"{base}/API/v3{path}",
        method=method,
        data=json.dumps(body).encode() if body is not None else None,
        headers={"X-API-TOKEN": os.environ["QUALTRICS_API_TOKEN"],
                 "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        data = r.read()
    return data if raw else json.loads(data)


def export_responses():
    sid = os.environ["QUALTRICS_SURVEY_ID"]
    start = api("POST", f"/surveys/{sid}/export-responses",
                {"format": "json", "compress": True, "useLabels": True})
    pid = start["result"]["progressId"]
    for _ in range(60):
        res = api("GET", f"/surveys/{sid}/export-responses/{pid}")["result"]
        if res["status"] == "complete":
            break
        if res["status"] == "failed":
            sys.exit("Qualtrics export failed")
        time.sleep(5)
    else:
        sys.exit("Qualtrics export timed out")
    blob = api("GET", f"/surveys/{sid}/export-responses/{res['fileId']}/file", raw=True)
    with zipfile.ZipFile(io.BytesIO(blob)) as z:
        return json.loads(z.read(z.namelist()[0]))


# ---------- Mapping and cleaning ----------

def field(resp, key):
    """Look up a key in labels first (choice text), then values."""
    for part in ("labels", "values"):
        v = resp.get(part, {}).get(key)
        if v not in (None, "", []):
            return ", ".join(map(str, v)) if isinstance(v, list) else str(v)
    return ""


def clean(text):
    text = EMAIL_RE.sub("[email removed]", text.strip())
    if len(text) > MAX_TEXT:
        text = text[:MAX_TEXT] + " [truncated]"
    return text


def to_record(resp, m):
    rec = {name: field(resp, key) for name, key in m["fields"].items()}
    rec["response_id"] = resp.get("responseId", "")
    rec["recorded"] = field(resp, "recordedDate")[:10]
    rec["finished"] = field(resp, "finished") in ("1", "True", "true")
    return rec


def eligible(rec):
    if not rec["finished"] or not rec["response_id"]:
        return False, "unfinished"
    return True, ""


def render(rec, m):
    lines = ["---"]
    for k in ["response_id", "recorded", "skill_version", "role", "tool", "mode",
              "usefulness", "false_findings", "missed_issues", "invented_facts",
              "length"]:
        lines.append(f"{k}: {json.dumps(rec.get(k, ''))}")
    lines.append(f"public_quote_ok: {json.dumps(rec['public_quote'])}")
    lines += ["status: included", "---", ""]
    for k, title in [("false_findings_text", "Findings that were wrong"),
                     ("missed_issues_text", "Problems that were missed"),
                     ("invented_facts_text", "Invented facts in the edited copy"),
                     ("suggestion", "Other suggestions")]:
        t = clean(rec.get(k, ""))
        if t:
            lines += [f"## {title}", "", t, ""]
    return "\n".join(lines)


def pr_body(rec):
    flags = []
    if rec.get("invented_facts", "").lower().startswith("yes"):
        flags.append("**Reports invented facts in edited copy: prioritize.**")
    return "\n".join([
        f"Survey response `{rec['response_id']}` (skill v{rec.get('skill_version') or '?'}, "
        f"{rec.get('role') or 'role not given'}, usefulness {rec.get('usefulness') or '?'}/5).",
        *flags,
        "",
        "Review before deciding:",
        "- [ ] No confidential data, names, or unpublished results in the text.",
        f"- Public quoting allowed by respondent: **{'yes' if rec.get('public_quote') else 'no'}**.",
        "- [ ] Feedback is about the skill (Template issues go to template_README).",
        "",
        "**Approve** to include this response (auto-merges). **Close** to reject.",
        "Edits to the file before approving are fine (e.g. redaction).",
    ])


# ---------- Git / GitHub ----------

def run(*cmd, check=True):
    return subprocess.run(cmd, check=check, text=True, capture_output=True, cwd=ROOT).stdout.strip()


def pr_exists(branch):
    out = run("gh", "pr", "list", "--state", "all", "--head", branch,
              "--json", "number", "--jq", "length")
    return out not in ("", "0")


def open_pr(rec, path, content, base):
    branch = f"feedback/response-{rec['response_id']}"
    if pr_exists(branch):
        return "exists"
    run("git", "checkout", "-q", "-B", branch, f"origin/{base}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    run("git", "add", str(path))
    run("git", "commit", "-q", "-m", f"Add feedback response {rec['response_id']}")
    run("git", "push", "-q", "-f", "origin", branch)
    run("gh", "pr", "create", "--base", base, "--head", branch, "--label", LABEL,
        "--title", f"Feedback: {rec['recorded']} v{rec.get('skill_version') or '?'} "
                   f"({rec.get('usefulness') or '?'}/5)",
        "--body", pr_body(rec))
    run("git", "checkout", "-q", "--detach", f"origin/{base}")
    return "opened"


# ---------- Main ----------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--from-file")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--base", default=os.environ.get("BASE_BRANCH", "main"))
    ap.add_argument("--repo-dir", default=".", help="checkout of the feedback repo")
    ap.add_argument("--out-subdir", default="responses")
    ap.add_argument("--map", default=str(MAP_FILE))
    a = ap.parse_args()

    global ROOT
    ROOT = Path(a.repo_dir).resolve()
    out_dir = ROOT / a.out_subdir
    m = json.loads(Path(a.map).read_text())
    data = json.loads(Path(a.from_file).read_text()) if a.from_file else export_responses()

    counts = {"opened": 0, "exists": 0, "skipped": 0}
    for resp in data.get("responses", []):
        rec = to_record(resp, m)
        rec["public_quote"] = rec.get("consent", "") == m["consent_yes"]
        ok, why = eligible(rec)
        if not ok:
            counts["skipped"] += 1
            print(f"skip {rec['response_id'] or '?'}: {why}")
            continue
        path = out_dir / f"{rec['recorded']}-{rec['response_id']}.md"
        content = render(rec, m)
        if path.exists():
            counts["exists"] += 1
            continue
        if a.dry_run:
            print(f"--- would open PR for {path.relative_to(ROOT)}\n{content}\n{pr_body(rec)}\n")
            counts["opened"] += 1
            continue
        counts[open_pr(rec, path, content, a.base)] += 1
    print(json.dumps(counts))


if __name__ == "__main__":
    main()
