---
title: What to expect
kernelspec:
  name: python3
  display_name: Python 3
  language: python

---

```{code-cell} python
:tags: [remove-cell]
import json
from IPython.display import display
site = json.load(open("site.json"))
```

You always get a report. You also get an edited copy of your README  when the assistant can see the actual package. A good README gets a short report, one that has issues a longer report.

::::{grid} 1 1 2 2

:::{card} `README-review.md`
:header: Always

- One-line verdict and counts by priority.
- Findings by section: what is wrong, where, and the fix.
- A feedback link: We would like to hear from you.
:::

:::{card} `README-ai-edited.md`
:header: If the package is available

- Your README, restructured into Template sections.
- Your wording kept where it works.
- Gaps filled only from the package; the rest marked `AUTHOR TO`.
- Your original file is untouched.
:::

::::

## Priorities

- **High**: a replicator probably could not proceed or could not reproduce a result (no data access, no entry point, unmapped tables, missing software).
- **Medium**: a replicator might be able to run the package, but would lose time or guess (no versions, no runtime, unclear order).
- **Low**: style or polish.

## A report looks like this

_Illustrative excerpt, not a real review._

```{code-cell} python
:tags: [remove-input]
report = f'''
# README review: README.pdf

- Skill: readme-review v{site["skill_version"]} · Template v{site["template_version"]} · 2026-11-13
- Mode: edit (package available)
- Verdict: Close to Template; data access details and table map incomplete.
- Findings: 2 High · 3 Medium · 4 Low

## B. Content

### Data Availability and Provenance Statements
- **High** — The survey data has no access instructions. Fix: give the
  URL or contact, cost, and expected wait time.

### List of tables and programs
- **High** — Tables 4–6 are not mapped to a program. Fix: add rows for
  them (code found in programs/03_robustness.do).

## C. Style
- **Low** — Overview: "In this comprehensive replication package, we are
  delighted to provide…" → "This package contains the data and Stata
  code to produce all tables and figures."
'''
print(report.strip())
```

:::{warning} This is a test version
Expect some findings that are not real problems, and some real problems it misses. Results also differ by AI tool and model. That is what the [next step](feedback.md) is for.
:::
