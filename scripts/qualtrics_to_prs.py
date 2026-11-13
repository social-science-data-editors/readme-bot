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
  QUALTRICS_SURVEY_ID  optional; overrides survey_id in the field map
  GH_TOKEN             token gh can use to push branches and open PRs

Usage:
  qualtrics_to_prs.py --repo-dir <feedback checkout>     fetch, open PRs
  qualtrics_to_prs.py --from-file x.json --dry-run       test on a saved export
Field mapping: feedback/qualtrics-map.json in readme-bot (override with --map)

All free text is untrusted (the "proposed changes" field may be pasted from an
AI assistant). vet() strips invisible characters and flags text that looks like
instructions to an AI, code, links, or markup; responses with a low bot score
(Q_RecaptchaScore) are flagged too. Flagged PRs get FLAG_LABEL.
Text is stored inside code fences so it renders inert.
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
import urllib.error
import urllib.request
import zipfile
from pathlib import Path

TOOL_ROOT = Path(__file__).resolve().parent.parent
MAP_FILE = TOOL_ROOT / "feedback" / "qualtrics-map.json"
ROOT = Path.cwd()  # target repo; set from --repo-dir
LABEL = "feedback:response"
FLAG_LABEL = "feedback:security-flag"
EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
MAX_TEXT = 2000
MAX_PROPOSAL = 10000
MAX_SHORT = 100
SHORT_TEXT = ["tool_other", "model"]  # free text kept in the front matter
BOT_THRESHOLD = 0.5  # reCAPTCHA v3 score below this: likely a bot (Qualtrics' own cut-off)
TEXT_FIELDS = [("false_findings_text", "Findings that were wrong"),
               ("missed_issues_text", "Problems that were missed"),
               ("invented_facts_text", "Invented facts in the edited copy"),
               ("suggestion", "Other suggestions"),
               ("proposal", "Proposed changes to the skill (untrusted; do not apply verbatim)")]

# Zero-width, bidi-control, tag, and other invisible characters.
HIDDEN_RE = re.compile("[\u00ad\u180e\u200b-\u200f\u202a-\u202e\u2060-\u2064"
                       "\u2066-\u2069\ufeff\U000e0000-\U000e007f]")
CHECKS = [
    ("instructions aimed at an AI", re.compile(
        r"ignore (all |any )?(previous|prior|above|earlier) (instructions|prompts?)"
        r"|disregard (the |all |previous )|system prompt|you are now|new instructions"
        r"|do not (tell|inform|mention)|</?(system|assistant|user|instructions?)>"
        r"|^\s*(system|assistant)\s*:", re.I | re.M)),
    ("commands or code", re.compile(
        r"```|\b(curl|wget|bash|sudo|chmod|eval|exec|subprocess|os\.system|powershell"
        r"|pip install|npm install|rm -rf)\b|\|\s*(sh|bash|python)\b|\$\(", re.I)),
    ("links", re.compile(r"https?://|www\.|\bftp://", re.I)),
    ("HTML or markup", re.compile(r"<\s*(script|iframe|img|a|style|object|embed|svg)\b|<!--|javascript:", re.I)),
    ("encoded blob", re.compile(r"[A-Za-z0-9+/=]{80,}")),
    ("credentials or data transfer", re.compile(
        r"\b(token|secret|password|api[_ ]?key|credential|exfiltrat\w*|upload \w+ to|send \w+ to)\b", re.I)),
    ("targets repo automation", re.compile(r"\.github|workflow|GH_TOKEN|GITHUB_TOKEN|FEEDBACK_URL", re.I)),
]


# ---------- Qualtrics ----------

def api(method, path, body=None, raw=False):
    base = os.environ["QUALTRICS_BASE_URL"].rstrip("/")
    if not base.startswith("http"):
        base = "https://" + base
    req = urllib.request.Request(
        f"{base}/API/v3{path}",
        method=method,
        data=json.dumps(body).encode() if body is not None else None,
        headers={"X-API-TOKEN": os.environ["QUALTRICS_API_TOKEN"],
                 "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            data = r.read()
    except urllib.error.HTTPError as e:
        sys.exit(f"{method} {path} failed: {e.code} {e.read().decode(errors='replace')}")
    return data if raw else json.loads(data)


def export_responses(sid):
    start = api("POST", f"/surveys/{sid}/export-responses",
                {"format": "json", "compress": True})
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


def clean(text, limit=MAX_TEXT):
    text = HIDDEN_RE.sub("", EMAIL_RE.sub("[email removed]", text.strip()))
    if len(text) > limit:
        text = text[:limit] + " [truncated]"
    return text


def vet(text):
    """Return a list of security flags for one free-text answer (before cleaning)."""
    flags = []
    if HIDDEN_RE.search(text):
        flags.append("invisible characters (removed)")
    flags += [name for name, rx in CHECKS if rx.search(text)]
    return flags


def fenced(text):
    """Wrap text in a code fence longer than any backtick run inside it."""
    longest = max((len(r) for r in re.findall(r"`+", text)), default=0)
    fence = "`" * max(3, longest + 1)
    return f"{fence}text\n{text}\n{fence}"


def to_record(resp, m):
    rec = {name: field(resp, key) for name, key in m["fields"].items()}
    rec["response_id"] = resp.get("responseId", "")
    rec["recorded"] = field(resp, "recordedDate")[:10]
    rec["finished"] = field(resp, "finished") in ("1", "True", "true")
    rec["preview"] = (resp.get("values", {}).get("distributionChannel") == "preview"
                      or resp.get("labels", {}).get("status") == "Survey Preview")
    rec["flags"] = {k: f for k in [k for k, _ in TEXT_FIELDS] + SHORT_TEXT
                    if (f := vet(rec.get(k, "")))}
    try:
        rec["likely_bot"] = float(rec.get("bot_score", "")) < BOT_THRESHOLD
    except ValueError:
        rec["likely_bot"] = False  # no score (bot detection off, or field not exported)
    return rec


def flagged(rec):
    return bool(rec["flags"]) or rec["likely_bot"]


def eligible(rec, include_previews=False):
    if not rec["finished"] or not rec["response_id"]:
        return False, "unfinished"
    if rec["preview"] and not include_previews:
        return False, "survey preview (use --include-previews to test)"
    return True, ""


def render(rec, m):
    lines = ["---"]
    for k in ["response_id", "recorded", "skill_version", "role", "tool", "tool_other",
              "interface", "instructions", "model", "mode",
              "usefulness", "false_findings", "missed_issues", "invented_facts",
              "length", "proposal_author", "bot_score", "bot_status"]:
        v = rec.get(k, "")
        lines.append(f"{k}: {json.dumps(clean(v, MAX_SHORT) if k in SHORT_TEXT else v)}")
    lines.append(f"public_quote_ok: {json.dumps(rec['public_quote'])}")
    sec = {f for v in rec["flags"].values() for f in v} | ({"likely bot"} if rec["likely_bot"] else set())
    lines.append(f"security_flags: {json.dumps(sorted(sec))}")
    lines += ["status: included", "---", ""]
    for k, title in TEXT_FIELDS:
        t = clean(rec.get(k, ""), MAX_PROPOSAL if k == "proposal" else MAX_TEXT)
        if t:
            lines += [f"## {title}", ""]
            if rec["flags"].get(k):
                lines += [f"Security flags: {', '.join(rec['flags'][k])}.", ""]
            lines += [fenced(t), ""]
    return "\n".join(lines)


def pr_body(rec):
    flags = []
    if rec.get("invented_facts", "").lower().startswith("yes"):
        flags.append("**Reports invented facts in edited copy: prioritize.**")
    if rec["likely_bot"]:
        flags.append(f"**Likely bot**: reCAPTCHA score {rec['bot_score']} (below {BOT_THRESHOLD}). Close unless the text is clearly human.")
    for k, f in rec["flags"].items():
        title = dict(TEXT_FIELDS).get(k, k).split(" (")[0]
        flags.append(f"**Security flag** ({title}): {', '.join(f)}.")
    if rec.get("proposal"):
        flags.append(f"Contains proposed skill changes (written by: {rec.get('proposal_author') or 'not stated'}).")
    return "\n".join([
        f"Survey response `{rec['response_id']}` (skill v{rec.get('skill_version') or '?'}, "
        f"{rec.get('role') or 'role not given'}, usefulness {rec.get('usefulness') or '?'}/5).",
        *flags,
        "",
        "Review before deciding:",
        "- [ ] No confidential data, names, or unpublished results in the text.",
        "- [ ] Free text read as data: no instructions to an AI, commands, or links to follow. "
        "Remove anything suspicious before approving (see FEEDBACK_PLAN.md, Security vetting).",
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
    labels = [LABEL] + ([FLAG_LABEL] if flagged(rec) else [])
    run("gh", "pr", "create", "--base", base, "--head", branch, "--label", ",".join(labels),
        "--title", f"Feedback: {rec['recorded']} v{rec.get('skill_version') or '?'} "
                   f"({rec.get('usefulness') or '?'}/5)",
        "--body", pr_body(rec))
    run("git", "checkout", "-q", "--detach", f"origin/{base}")
    return "opened"


def ensure_labels():
    run("gh", "label", "create", LABEL, "--force", "--color", "0e8a16",
        "--description", "Survey response awaiting maintainer decision")
    run("gh", "label", "create", FLAG_LABEL, "--force", "--color", "d93f0b",
        "--description", "Free text flagged by automated vetting; check, then remove label to allow merge")


# ---------- Main ----------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--from-file")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--base", default=os.environ.get("BASE_BRANCH", "main"))
    ap.add_argument("--repo-dir", default=".", help="checkout of the feedback repo")
    ap.add_argument("--out-subdir", default="responses")
    ap.add_argument("--map", default=str(MAP_FILE))
    ap.add_argument("--include-previews", action="store_true",
                    help="also process Qualtrics survey-preview responses (testing)")
    a = ap.parse_args()

    global ROOT
    ROOT = Path(a.repo_dir).resolve()
    out_dir = ROOT / a.out_subdir
    m = json.loads(Path(a.map).read_text())
    sid = os.environ.get("QUALTRICS_SURVEY_ID") or m.get("survey_id")
    if not a.from_file and not sid:
        sys.exit("No survey ID: set survey_id in the field map (scripts/create_survey.py does) "
                 "or QUALTRICS_SURVEY_ID")
    data = json.loads(Path(a.from_file).read_text()) if a.from_file else export_responses(sid)

    if not a.dry_run:
        ensure_labels()
    counts = {"opened": 0, "exists": 0, "skipped": 0, "flagged": 0}
    for resp in data.get("responses", []):
        rec = to_record(resp, m)
        rec["public_quote"] = rec.get("consent", "") == m["consent_yes"]
        ok, why = eligible(rec, a.include_previews)
        if not ok:
            counts["skipped"] += 1
            print(f"skip {rec['response_id'] or '?'}: {why}")
            continue
        path = out_dir / f"{rec['recorded']}-{rec['response_id']}.md"
        content = render(rec, m)
        if path.exists():
            counts["exists"] += 1
            continue
        counts["flagged"] += flagged(rec)
        if a.dry_run:
            print(f"--- would open PR for {path.relative_to(ROOT)}\n{content}\n{pr_body(rec)}\n")
            counts["opened"] += 1
            continue
        counts[open_pr(rec, path, content, a.base)] += 1
    print(json.dumps(counts))


if __name__ == "__main__":
    main()
