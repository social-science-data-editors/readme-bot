# README review: README.qmd

- Skill: readme-review v0.1.0 · Template v1.2 · 2026-11-27
- Mode: edit (package available)
- Verdict: Close to Template; content is unusually thorough, but a few leftover template artifacts, a missing Overview/Randomness statement, two unlisted data files and a version inconsistency should be fixed.
- Findings: 1 High · 4 Medium · 6 Low

## A. Structure

- **Medium** — No "Overview" section: the package summary, entry point, and total runtime are scattered across "Structure", "Code" and "Computational requirements" instead of stated up front. Fix: add a short Overview after "Authors" (done in edited copy).
- **Low** — "List of tables and figures" (table/figure map) is placed before "Dataset list" and before "Computational requirements", reversing the Template order. Fix: move "Dataset list" ahead of the table/figure map, or note this is intentional.

## B. Content

### List of tables and figures

- **High** — Leftover Template instruction comments not removed: `<!--- Your programs should clearly identify... -->` and `<!--- pick one -->` (lines ~186–195), with both options left in ("All numbers... " and "All tables and figures...") instead of one being chosen/merged. Fix: delete the HTML comments; state directly that both numbers and exhibits are reproduced (done in edited copy).

### Dataset list

- **High** — Two data files present in `data/` are not listed: `paris-arr-areas.Rds` and `pra-all-prices.Rds`. Fix: add them to the table with source/notes (placeholders added in edited copy; author to fill in).

### Computational requirements — Software requirements

- **Medium** — Stata version stated inconsistently: "Code" section says "stata versions 14 as well as 19.5"; "Software requirements" says "Stata 14, Stata 18.5 and StataNow". Fix: state one consistent set of tested versions.
- **Medium** — "Manual Setup of R" and "The Full Automatic Run Script" checklist both say "Verify you have R version **4.2.2**", contradicting "Software requirements" which correctly requires R **4.4.2** (matches `renv.lock`). Fix: correct both occurrences to 4.4.2 (done in edited copy).

### Computational requirements — Controlled Randomness

- **Medium** — No statement on random-number use (Template 4b). A seed is in fact set once, at `code/LandUse.jl/src/estimation.jl:347` (`Random.seed!(20230101)`). Fix: add a short "Controlled Randomness" subsection naming this location (done in edited copy).

## C. Style

- **Low** — Typos: "Naviate" → "Navigate" (×2, Instructions section); "decribes" → "describes" (Agricultural Yield section); "sreenshots" → "screenshots" (Dataset list, `images` row); "historial" → "historical" (Dataset list, `shlomo-angel` row); "straighforward" → "straightforward" (Software requirements). Fixed in edited copy.

## Sections with no findings

Authors, Data availability and provenance statements (rights, availability summary, data source details), Description of programs/code, License for Code, Hardware requirements, Instructions to replicators (sequencing), Software citations/References.

## Edited copy

- File: `README-ai-edited.qmd`
- Sections changed: Overview (added), List of tables and figures (comments removed, wording merged), Dataset list (two rows added), Computational requirements (Controlled Randomness subsection added, Stata version flagged, R version typo fixed), Instructions to replicators (typo fixes), Dataset list typos.
- Placeholders left for the author: 3 (search for `AUTHOR TO`)

---

Feedback on this review (to be answered by you, not by an AI assistant): https://cornell.yul1.qualtrics.com/jfe/form/SV_blzbYfhetCOJ2GW?skill_version=0.1.0
