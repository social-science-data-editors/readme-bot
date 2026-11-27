"""Validate a readme-review skill run against its own spec.

Uses tests/fixtures/Oswald/ (a real run: README.qmd -> README-review.md +
README-ai-edited.qmd) as the sample output. Checks the report against
skills/readme-review/references/report-format.md and the edited copy against
the edit-mode rules in skills/readme-review/SKILL.md. Catches drift between
what the skill is supposed to produce and what it actually produced for a
given model/version -- not a test of the underlying replication code.

Standard library only, run with pytest.
"""
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills" / "readme-review"
FIXTURE = ROOT / "tests" / "fixtures" / "Oswald"

VERSION = (SKILL / "VERSION").read_text().strip()


@pytest.fixture(scope="module")
def report_text():
    return (FIXTURE / "README-review.md").read_text()


@pytest.fixture(scope="module")
def edited_text():
    return (FIXTURE / "README-ai-edited.qmd").read_text()


@pytest.fixture(scope="module")
def original_text():
    return (FIXTURE / "README.qmd").read_text()


# --- report: references/report-format.md shape -----------------------------

def test_report_title_names_the_readme_file(report_text):
    assert report_text.startswith("# README review: README.qmd")


def test_report_declares_current_skill_version(report_text):
    m = re.search(r"Skill: readme-review v([\d.]+)", report_text)
    assert m, "missing 'Skill: readme-review vX.Y.Z' line"
    assert m.group(1) == VERSION


def test_report_declares_a_mode(report_text):
    m = re.search(r"^- Mode: (.+)$", report_text, re.MULTILINE)
    assert m, "missing Mode line"
    assert m.group(1).strip() in ("review-only", "edit (package available)")


def test_report_has_nonempty_verdict(report_text):
    m = re.search(r"^- Verdict: (.+)$", report_text, re.MULTILINE)
    assert m and m.group(1).strip()


def test_report_never_says_the_readme_fails(report_text):
    # SKILL.md: "The Template is a suggestion, not a gate. Never say a README 'fails'."
    assert not re.search(r"\bfails?\b", report_text, re.IGNORECASE)


def test_report_has_required_section_headings(report_text):
    for heading in ("## A. Structure", "## B. Content", "## C. Style",
                     "## Sections with no findings"):
        assert heading in report_text


@pytest.mark.xfail(
    reason="known bug in the fixture's own report: header miscounts High/Low "
    "bullets (High says 1, body has 2; Low says 6, body has 2 bullets covering "
    "6 typo instances) -- see issue to be filed against this fixture",
    strict=True,
)
def test_report_findings_counts_match_actual_bullets(report_text):
    m = re.search(
        r"^- Findings: (\d+) High . (\d+) Medium . (\d+) Low$",
        report_text, re.MULTILINE,
    )
    assert m, "missing 'Findings: n High · n Medium · n Low' line"
    declared = {k: int(v) for k, v in zip(("High", "Medium", "Low"), m.groups())}
    actual = {
        level: len(re.findall(rf"^- \*\*{level}\*\*", report_text, re.MULTILINE))
        for level in ("High", "Medium", "Low")
    }
    assert declared == actual, (
        f"declared counts {declared} do not match actual bullet counts {actual}"
    )


def test_report_edited_copy_block_present_in_edit_mode(report_text):
    assert "## Edited copy" in report_text
    for field in ("File:", "Sections changed:", "Placeholders left for the author:"):
        assert field in report_text


@pytest.mark.xfail(
    reason="known bug in the fixture's own report: 'Placeholders left for the "
    "author: 3' undercounts the actual 6 [AUTHOR TO ...] tags in the edited "
    "copy -- see issue to be filed against this fixture",
    strict=True,
)
def test_report_placeholder_count_matches_edited_copy(report_text, edited_text):
    m = re.search(r"Placeholders left for the author: (\d+)", report_text)
    assert m, "missing placeholder count line"
    declared = int(m.group(1))
    actual = len(re.findall(r"\[AUTHOR TO (?:VERIFY|PROVIDE):", edited_text))
    assert declared == actual, (
        f"report declares {declared} placeholders, edited copy contains {actual}"
    )


def test_report_ends_with_feedback_line_for_current_version(report_text):
    feedback_template = (SKILL / "FEEDBACK_URL").read_text().strip()
    expected = feedback_template.replace("{VERSION}", VERSION)
    assert expected in report_text


# --- edited copy: SKILL.md edit-mode rules ----------------------------------

def test_edited_copy_has_ai_edited_marker_comment(edited_text):
    assert re.search(
        r"<!--\s*AI-edited draft from README-review skill v[\d.]+ on \d{4}-\d{2}-\d{2}\.",
        edited_text,
    )


def test_edited_copy_marker_version_matches_skill_version(edited_text):
    m = re.search(r"AI-edited draft from README-review skill v([\d.]+)", edited_text)
    assert m and m.group(1) == VERSION


def test_edited_copy_has_no_leftover_template_instructions(edited_text):
    assert "> INSTRUCTIONS" not in edited_text
    assert "<!---" not in edited_text, "leftover Template HTML comment not removed"


def test_edited_copy_placeholders_use_the_documented_bracket_syntax(edited_text):
    for m in re.finditer(r"\[AUTHOR TO ([A-Z]+):", edited_text):
        assert m.group(1) in ("VERIFY", "PROVIDE"), (
            f"unexpected placeholder kind: {m.group(0)}"
        )


def test_original_readme_is_untouched_by_the_edit(original_text):
    # The fixture ships both files; the only contract we can check here is that
    # editing happened on a copy, i.e. the original still has no AI marker.
    assert "AI-edited draft from README-review skill" not in original_text


def test_edited_copy_filename_follows_convention():
    original = FIXTURE / "README.qmd"
    edited = FIXTURE / "README-ai-edited.qmd"
    assert edited.name == original.stem + "-ai-edited" + original.suffix
