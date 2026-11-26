#!/usr/bin/env python3
"""Write docs/site.json: the values the website pages show.

The pages are MyST notebooks (docs/*.md) that read this file in a code cell when
the site is built; nothing is edited into them. Sources:

  skill_version     skills/readme-review/VERSION
  survey_url        skills/readme-review/FEEDBACK_URL, with {VERSION} filled in
  template_version  TEMPLATE_VERSION
  approvers         git history: everyone who authored or committed, minus bots

Called by scripts/build.sh; standard library only.
"""
import json
import re
import subprocess
from pathlib import Path

root = Path(__file__).resolve().parent.parent
skill = root / "skills" / "readme-review"
DEFAULT_SURVEY = "https://github.com/social-science-data-editors/readme-bot/issues"


def read(path):
    return path.read_text().strip() if path.exists() else ""


def approvers():
    log = subprocess.run(
        ["git", "-C", str(root), "log", "--format=%an|%ae%n%cn|%ce"],
        capture_output=True, text=True,
    ).stdout
    bots = re.compile(r"\[bot\]|^(GitHub|Claude)\||noreply@(github\.com|anthropic\.com)$", re.I)
    names = {l.split("|")[0] for l in log.splitlines() if l and not bots.search(l)}
    return ", ".join(sorted(names)) or "the maintainers"


version = read(skill / "VERSION")
data = {
    "skill_version": version,
    "survey_url": read(skill / "FEEDBACK_URL").replace("{VERSION}", version) or DEFAULT_SURVEY,
    "template_version": read(root / "TEMPLATE_VERSION"),
    "approvers": approvers(),
}
(root / "docs" / "site.json").write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
print("Wrote docs/site.json")
