#!/usr/bin/env python3
"""Create the feedback survey in Qualtrics from feedback/survey-spec.json.

Builds the survey through the Qualtrics API (survey-definitions): one block per
page, questions with required/display logic, embedded data from the URL, then
publishes and activates it. Writes:
  feedback/qualtrics-map.json         survey ID and real question IDs
  skills/readme-review/FEEDBACK_URL   anonymous link with ?skill_version={VERSION}
Not done here (do by hand, see feedback/FEEDBACK_PLAN.md): anonymize responses,
share the project, export the QSF to feedback/survey.qsf.

Environment: QUALTRICS_BASE_URL, QUALTRICS_API_TOKEN (or QUALTRICS_API_KEY).

Usage:
  create_survey.py --dry-run          print API payloads, write nothing
  create_survey.py --placeholder-map  write qualtrics-map.json with simulated IDs
  create_survey.py --markdown         regenerate feedback/questions.md (whole file)
  create_survey.py                    create the survey (live)
  create_survey.py --survey-id SV_x   fill an existing blank survey (live; add --dry-run to check)
Standard library only.
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SPEC = ROOT / "feedback" / "survey-spec.json"
MAP = ROOT / "feedback" / "qualtrics-map.json"
QUESTIONS_MD = ROOT / "feedback" / "questions.md"
FEEDBACK_URL = ROOT / "skills" / "readme-review" / "FEEDBACK_URL"
PLACEHOLDER = "Click to write the question text"


# ---------- API ----------

class Api:
    def __init__(self, dry, quiet=False):
        self.dry, self.quiet = dry, quiet
        self.n = 0
        if not dry:
            self.base = os.environ["QUALTRICS_BASE_URL"].rstrip("/")
            if not self.base.startswith("http"):
                self.base = "https://" + self.base
            self.token = os.environ.get("QUALTRICS_API_TOKEN") or os.environ["QUALTRICS_API_KEY"]

    def __call__(self, method, path, body=None, fake=None):
        if self.dry:
            if not self.quiet:
                print(f"{method} /API/v3{path}")
                if body is not None:
                    print(json.dumps(body, indent=1))
            return fake or {}
        req = urllib.request.Request(
            f"{self.base}/API/v3{path}", method=method,
            data=json.dumps(body).encode() if body is not None else None,
            headers={"X-API-TOKEN": self.token, "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.loads(r.read() or b"{}").get("result", {})
        except urllib.error.HTTPError as e:
            sys.exit(f"{method} {path} failed: {e.code} {e.read().decode(errors='replace')}")


# ---------- Question payloads ----------

def choices(labels):
    return ({str(i): {"Display": c} for i, c in enumerate(labels, 1)},
            list(range(1, len(labels) + 1)))


def validation(q):
    s = {"ForceResponse": "ON" if q.get("required") else "OFF",
         "ForceResponseType": "ON" if q.get("required") else "OFF", "Type": "None"}
    if q.get("validate") == "email":
        s.update(Type="ContentType", ContentType="ValidEmail")
    return {"Settings": s}


def display_logic(cond, qids, spec_q):
    src = spec_q[cond["question"]]
    qid = qids[cond["question"]]
    if cond.get("not_empty"):
        loc, op = f"q://{qid}/ChoiceTextEntryValue", "NotEmpty"
        desc = f"If {cond['question']} is not empty"
    else:
        n = src["choices"].index(cond["choice"]) + 1
        loc, op = f"q://{qid}/SelectableChoice/{n}", "Selected"
        desc = f"If {cond['question']} = {cond['choice']}"
    expr = {"LogicType": "Question", "QuestionID": qid, "QuestionIsInLoop": "no",
            "ChoiceLocator": loc, "Operator": op, "QuestionIDFromLocator": qid,
            "LeftOperand": loc, "Type": "Expression", "Description": desc}
    return {"0": {"0": expr, "Type": "If"}, "Type": "BooleanExpression", "inPage": False}


def payload(q, qids, spec_q):
    p = {"QuestionText": q["text"], "DataExportTag": q["id"],
         "Configuration": {"QuestionDescriptionOption": "UseText"},
         "Validation": validation(q), "Language": []}
    t = q["type"]
    if t in ("single", "scale"):
        c, order = choices(q["choices"])
        p.update(QuestionType="MC", Selector="SAHR" if t == "scale" else "SAVR",
                 SubSelector="TX", Choices=c, ChoiceOrder=order)
    elif t == "text_long":
        p.update(QuestionType="TE", Selector="ESTB")
    elif t == "text_short":
        p.update(QuestionType="TE", Selector="SL")
    elif t == "intro":
        p.update(QuestionType="DB", Selector="TB")
        p.pop("Validation")
    else:
        sys.exit(f"unknown type {t} in {q['id']}")
    if q.get("show_if"):
        p["DisplayLogic"] = display_logic(q["show_if"], qids, spec_q)
    return p


def export_key(q, qid):
    """Key of the answer in a Qualtrics JSON response export."""
    return f"{qid}_TEXT" if q["type"].startswith("text") else qid


# ---------- Build ----------

def all_questions(spec):
    return [q for page in spec["pages"] for q in page]


def check(spec):
    seen = {}
    for i, page in enumerate(spec["pages"]):
        for q in page:
            c = q.get("show_if")
            if c and seen.get(c["question"], i) >= i:
                sys.exit(f"{q['id']}: show_if must refer to a question on an earlier page")
            seen[q["id"]] = i


def use_existing(survey, api, reset=False):
    """Return the default block of an existing, empty survey.
    reset=True first deletes all questions and non-default blocks (e.g. after a failed run)."""
    d = api("GET", f"/survey-definitions/{survey}",
            fake={"Questions": {}, "Blocks": {"BL_1": {"Type": "Default", "BlockElements": []}}})
    questions = d.get("Questions", {})
    real = [q for q, v in questions.items() if v.get("QuestionText") != PLACEHOLDER]
    if real and not reset:
        sys.exit(f"{survey} already has {len(real)} question(s): {', '.join(real)}; "
                 "use a blank survey (or delete its questions) to avoid duplicates.")
    for q in questions:  # stock placeholder, or everything with reset
        api("DELETE", f"/survey-definitions/{survey}/questions/{q}")
    blocks = d.get("Blocks", {})
    if reset:
        for b, v in blocks.items():
            if v.get("Type") == "Standard":
                api("DELETE", f"/survey-definitions/{survey}/blocks/{b}")
    default = [b for b, v in blocks.items() if v.get("Type") == "Default"]
    if not default:
        sys.exit(f"{survey}: no default block found")
    return default[0]


def create(spec, api, survey=None, reset=False):
    if survey:
        default_block = use_existing(survey, api, reset)
    else:
        sid = api("POST", "/survey-definitions",
                  {"SurveyName": spec["name"], "Language": "EN", "ProjectCategory": "CORE"},
                  fake={"SurveyID": "SV_DRYRUN", "DefaultBlockID": "BL_1"})
        survey, default_block = sid["SurveyID"], sid["DefaultBlockID"]
    blocks = [default_block]
    for i in range(1, len(spec["pages"])):
        b = api("POST", f"/survey-definitions/{survey}/blocks",
                {"Type": "Standard", "Description": f"Page {i + 1}"},
                fake={"BlockID": f"BL_{i + 1}"})
        blocks.append(b["BlockID"])

    spec_q = {q["id"]: q for q in all_questions(spec)}
    qids = {}
    intro = {"id": "intro", "type": "intro", "text": spec["intro"]}
    for page, block in zip([[intro] + spec["pages"][0]] + spec["pages"][1:], blocks):
        for q in page:
            api.n += 1
            r = api("POST", f"/survey-definitions/{survey}/questions?blockId={block}",
                    payload(q, qids, spec_q), fake={"QuestionID": f"QID{api.n}"})
            qids[q["id"]] = r["QuestionID"]

    # Flow: embedded data first, then the blocks in page order.
    flow = api("GET", f"/survey-definitions/{survey}/flow",
               fake={"FlowID": "FL_1", "Type": "Root", "Flow": [
                   {"Type": "Block", "ID": default_block, "FlowID": "FL_2"}]})
    existing = {e.get("ID"): e for e in flow.get("Flow", []) if e.get("ID")}
    n = 2 + len(existing)
    elems = [{"Type": "EmbeddedData", "FlowID": f"FL_{n}", "EmbeddedData": [
        {"Description": f, "Type": "Recipient", "Field": f, "VariableType": "String",
         "DataVisibility": [], "AnalyzeText": False} for f in spec["embedded_data"]]}]
    for b in blocks:
        if b not in existing:
            n += 1
        elems.append(existing.get(b) or {"Type": "Standard", "ID": b, "FlowID": f"FL_{n}"})
    flow.update(Flow=elems, Properties={"Count": n})
    api("PUT", f"/survey-definitions/{survey}/flow", flow)

    api("POST", f"/survey-definitions/{survey}/versions",
        {"Description": "Created by scripts/create_survey.py", "Published": True})
    api("PUT", f"/surveys/{survey}", {"isActive": True})
    return survey, qids


def write_map(spec, survey, qids):
    m = {"_comment": "GENERATED by scripts/create_survey.py from survey-spec.json. "
                     "Record field -> key in the Qualtrics JSON export. survey_id may be "
                     "overridden by the QUALTRICS_SURVEY_ID environment variable. "
                     "The email question is deliberately not mapped.",
         "survey_id": survey,
         "consent_yes": spec["consent_yes"],
         "fields": {"skill_version": "skill_version",
                    # Survey options -> Security: bot detection + include security fields
                    "bot_score": "Q_RecaptchaScore",
                    "bot_status": "Q_RecaptchaStatus"}}
    for q in all_questions(spec):
        if q.get("field"):
            m["fields"][q["field"]] = export_key(q, qids[q["id"]])
    MAP.write_text(json.dumps(m, indent=2) + "\n")
    print(f"wrote {MAP.relative_to(ROOT)}")


# ---------- Markdown table ----------

TYPE_TEXT = {"single": "Single choice", "scale": "Scale", "text_long": "Long text",
             "text_short": "Short text"}


def markdown(spec):
    rows = ["| # | Page | Question | Type | Required | Shown if |", "|---|---|---|---|---|---|"]
    for i, page in enumerate(spec["pages"], 1):
        for q in page:
            t = TYPE_TEXT[q["type"]]
            if q.get("choices"):
                t += ": " + "; ".join(q["choices"])
            if q.get("validate"):
                t += f", {q['validate']} validation"
            c = q.get("show_if")
            cond = "" if not c else (f"{c['question']} not empty" if c.get("not_empty")
                                     else f"{c['question']} = {c['choice']}")
            text = q["text"].replace("<b>", "**").replace("</b>", "**").replace("|", "\\|")
            rows.append(f"| {q['id']} | {i} | {text} | {t} | "
                        f"{'Yes' if q.get('required') else 'No'} | {cond} |")
    out = [
        "<!-- AUTO-GENERATED by scripts/create_survey.py from feedback/survey-spec.json. "
        "DO NOT EDIT: edit the spec; a workflow regenerates this file. -->",
        "",
        "# Feedback survey questions (Qualtrics)",
        "",
        "> **Auto-generated, do not edit.** Source: [survey-spec.json](survey-spec.json). "
        "Manual edits are overwritten by the \"Generate survey questions\" workflow.",
        "",
        f"Survey name: {spec['name']}. "
        "`scripts/create_survey.py` builds the survey from the spec via the Qualtrics API "
        "and writes the real question IDs to `qualtrics-map.json`. "
        "IDs Q1–Q13 are labels (Qualtrics \"data export tags\"), not Qualtrics question IDs. "
        "Keep the survey under 2 minutes.",
        "",
        "Opening text (shown above Q1):",
        "",
        f"> {spec['intro']}",
        "",
        "Embedded data (filled from the link): " + ", ".join(f"`{f}`" for f in spec["embedded_data"]) + ".",
        "",
        *rows,
        "",
        *[f"- {n}" for n in spec.get("notes", [])],
    ]
    QUESTIONS_MD.write_text("\n".join(out) + "\n")
    print(f"updated {QUESTIONS_MD.relative_to(ROOT)}")


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--dry-run", action="store_true")
    g.add_argument("--placeholder-map", action="store_true")
    g.add_argument("--markdown", action="store_true")
    ap.add_argument("--survey-id", help="fill this existing, blank survey instead of creating one")
    ap.add_argument("--reset", action="store_true",
                    help="with --survey-id: first delete ALL its questions and extra blocks")
    a = ap.parse_args()
    spec = json.loads(SPEC.read_text())
    check(spec)
    if a.markdown:
        return markdown(spec)

    api = Api(dry=a.dry_run or a.placeholder_map, quiet=a.placeholder_map)
    if a.reset and not a.survey_id:
        sys.exit("--reset needs --survey-id")
    survey, qids = create(spec, api, a.survey_id, a.reset)
    if a.dry_run:
        print(json.dumps({"survey_id": survey, "qids": qids}, indent=1))
        return
    if a.placeholder_map:
        return write_map(spec, "", qids)

    write_map(spec, survey, qids)
    link = f"{api.base}/jfe/form/{survey}?skill_version={{VERSION}}"
    FEEDBACK_URL.write_text(link + "\n")
    print(f"wrote {FEEDBACK_URL.relative_to(ROOT)}: {link}")
    print("Next: anonymize responses, share the project, export the QSF "
          "(feedback/FEEDBACK_PLAN.md), bump VERSION, run scripts/build.sh.")


if __name__ == "__main__":
    main()
