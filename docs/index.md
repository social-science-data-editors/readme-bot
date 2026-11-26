---
title: What it is
site:
  hide_toc: true
  hide_outline: true
  hide_title_block: true
  hide_footer_links: true
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

+++ {"kind": "centered", "class": "rb-hero"}

Social Science Data Editors · Skill v{eval}`site["skill_version"]` · test version

## readme-bot

An AI skill that reviews the README of a replication package against the [Template README](https://social-science-data-editors.github.io/template_README/template-README.html), and tells you what a replicator would miss. Works with Claude, ChatGPT, Gemini, Copilot, and others.

+++ {"kind": "justified"}

## What it is

readme-bot is a set of instructions for an AI assistant. You give the assistant your README, and optionally the replication package. It returns a list of differences from the Template README, ranked by how much they would slow a replicator down.

::::{grid} 1 1 3 3

:::{card} A · Structure
Are the Template's sections present, in a sensible order? Any redundant or example text present?
:::

:::{card} B · Content
Does each section have meaningful content, i.e., what a replicator needs: data access, file list, software versions, seed, runtime, run order, table and figure map, references?
:::

:::{card} C · Style
Is the README short and plain? A good README has lists, not long prose; has steps in the order you run them. No unnecessary filler, no AI-speak.
:::

::::

:::::{div}
:class: rb-flow

::::{div}
:class: rb-step rb-you rb-s1

**1 · Your README**

plus the package or a file listing (optional)
::::

::::{div}
:class: rb-step rb-you rb-s2

**2 · Your AI assistant**

runs the [readme-review skill](use.md) or prompt file
::::

::::{div}
:class: rb-step rb-you rb-s3

**3 · Report**

`README-review.md` + `README-ai-edited.md` ([what to expect](expect.md))
::::

::::{div}
:class: rb-step rb-you rb-s4

**4 · You check it**

fix your README; verify every AI edit yourself
::::

::::{div}
:class: rb-step rb-them rb-s5

**5 · Feedback survey**

~2 minutes, anonymized; answered by you, not AI ([how](feedback.md))
::::

::::{div}
:class: rb-step rb-them rb-s6

**6 · Private repository**

one pull request per response; free text vetted
::::

::::{div}
:class: rb-step rb-them rb-s7

**7 · Maintainers**

approve or reject; write the next skill version, which feeds back into step 2
::::

::::{div}
:class: rb-lane rb-lane-you

Your side
::::

::::{div}
:class: rb-lane rb-lane-them

Maintainers' side
::::

:::::

:::{div}
:class: rb-flow-caption

**How a review works (top) and how your feedback changes the skill (bottom).**
:::

### Who it is for

- **Authors**, before submitting a replication package.
- **Data editors and journal staff**, as a first pass before a human review.
- **Replicators**, to see quickly what a README leaves out.

### What it is not

- Not a gate. The Template is a suggestion; the review says what differs and why it matters. It never says a README "fails".
- Not a journal decision. Passing or failing a data editor's check is still up to the data editor.
- Not a review of your research. It does not judge the paper, the methods, or the results, and it does not run your code.

+++ {"class": "rb-footer-block"}

:::{div}
:class: rb-footer

readme-bot · [GitHub](https://github.com/social-science-data-editors/readme-bot) · MIT license · Based on the [Template README](https://social-science-data-editors.github.io/template_README/) v{eval}`site["template_version"]`.

Approved by {eval}`site["approvers"]`.
:::
