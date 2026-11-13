---
name: readme-review
description: Review a replication package README against the Social Science Data Editors Template README. Use when asked to check, review, assess, or improve a README for a replication package (economics, social science, journal data editor). Reports structure, content, and style issues; if the replication package is available, saves an improved copy as README-ai-edited.
---

# README review (SSDE Template)

Reference: the Template README, <https://social-science-data-editors.github.io/template_README/template-README.html> (source: `social-science-data-editors/template_README`, file `template-README.md`).

The Template is a **suggestion, not a gate**. Never say a README "fails". Say what differs and why it matters to a replicator.

Skill version: see `VERSION` in this folder. Print it in the report.

## Inputs

1. The README (Markdown, plain text, PDF, Word, or LaTeX). Required.
2. The replication package (folder, zip, or file listing). Optional.

Decide the mode:

- **Review-only mode**: only the README is available. Produce the report. Do not write an edited copy.
- **Edit mode**: the package (or at least its file tree) is available. Produce the report **and** an edited copy.

If the README is not in English, review it anyway, flag it as check A0, and write the edited copy in English.

## Procedure

Work through checks A, B, C in order. Collect findings; write the report at the end.

### A. Structure: is the README organized per the Template?

Compare headings against `references/template-sections.md`.

- A0. README is in English.
- A1. Each required section is present, under a recognizable heading (exact wording not required; map synonyms, e.g. "Data sources" = "Data Availability and Provenance Statements").
- A2. Sections appear in roughly the Template order. Flag order only when it hurts the replicator (e.g. run instructions before software requirements).
- A3. Template boilerplate removed: no `> INSTRUCTIONS:` lines, no unedited example text (e.g. "Ruggles et al, 2018", "Stata version 15", "4-core Intel-based laptop with MacOS version 10.14.4"), no unfilled blanks (`___`).
- A4. File is named `README` plus a suffix (`.md`, `.pdf`, `.txt`, `.docx`, `.tex`), at the package root. Flag if a PDF version appears to be missing (the Template asks for one).

### B. Content: does each section say something meaningful?

For each section, apply the "must contain" list in `references/template-sections.md`. A section is **empty** if it has no content, **placeholder** if it contains only template text or "TBD", and **thin** if it misses items from its list.

Key questions, in order of importance:

- B1. Data: is every data source named, cited, and given a way to obtain it (URL, DOI, contact, cost, wait time)? Are redistribution rights stated?
- B2. Dataset list: is every data file in the package described?
- B3. Software: are all software and packages listed **with versions**? Is there a setup script?
- B4. Randomness: is the seed location stated, or the absence of randomness stated?
- B5. Runtime and storage: approximate time and disk space, and the machine it was last run on.
- B6. Instructions: a numbered, strictly sequential list a replicator can follow without guessing.
- B7. Table/figure map: every table and figure in the paper mapped to a program (and output file). In-text numbers addressed.
- B8. References: every citation in the README resolves to a full reference.

In edit mode, verify claims against the package (see `references/package-checks.md`). Examples: a listed file that does not exist; a data file present but not listed; `set seed` found in code but README says no randomness; packages loaded in code but missing from the software list.

### C. Style: is it as short and clear as possible?

Apply `references/style-guide.md`. In short:

- C1. No chatty or promotional prose; no AI-speak.
- C2. Lists preferred over prose **and** over tables. Tables only where the Template uses them and the content is truly tabular (data summary, file list, table/figure map).
- C3. Instructions in strict chronological order, one action per step.
- C4. No duplicated content across sections.

Quote the offending sentence (shortened if long) and give the shorter replacement.

## Output 1: the report (always)

Use the format in `references/report-format.md`. Rules:

- Lead with a one-line verdict and counts of findings by priority.
- Findings are a list, grouped by section, each tagged **High** (blocks replication), **Medium** (slows replication), or **Low** (style, polish).
- Each finding: what is wrong, where (heading or line), concrete fix.
- Do not praise. Do not restate what is fine, except a single "Sections with no findings" line.
- End with the feedback line from `references/report-format.md`.

Save as `README-review.md` next to the README when you can write files; otherwise print it.

## Output 2: the edited copy (edit mode only)

- Never modify the original README.
- Save as the original name plus `-ai-edited`, before the extension: `README.md` → `README-ai-edited.md`. If the original is PDF, Word, or LaTeX, write `README-ai-edited.md` in Markdown.
- Start from the original text. Keep the author's content and wording where it is acceptable; restructure into Template sections; apply style fixes.
- Fill gaps **only with facts found in the package** (file names, seeds, package lists, table-to-program mapping). Cite the source file in an HTML comment if helpful, e.g. `<!-- from programs/config.do line 12 -->`.
- Anything you cannot verify goes in as a visible placeholder: `[AUTHOR TO VERIFY: ...]` or `[AUTHOR TO PROVIDE: ...]`. Never invent data sources, versions, runtimes, URLs, DOIs, licenses, or hardware.
- Do not include `> INSTRUCTIONS` text or Template examples.
- At the top, add one comment: `<!-- AI-edited draft from README-review skill vX.Y.Z on YYYY-MM-DD. Review every change before use. -->`
- After writing, list in the report which sections were changed and how many placeholders remain.

## Things not to do

- Do not run the replication code.
- Do not judge the research, the econometrics, or the paper.
- Do not require exact Template headings or checkboxes; content matters, form is a suggestion.
- Do not pad the report. If the README is good, the report is short.
