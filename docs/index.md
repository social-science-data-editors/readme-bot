---
title: What it is
site:
  hide_toc: true
  hide_outline: true
  hide_title_block: true
  hide_footer_links: true
---

+++ {"kind": "centered", "class": "rb-hero"}

Social Science Data Editors · Skill v0.1.0 · test version

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

**How a review works, and how your feedback changes the skill.** Each box links to the page that covers it. _Claude-generated._

**Your side**

::::{grid} 1 2 4 4

:::{card} 1 · Your README
:link: use.md
Plus the package or a file listing (optional).
:::

:::{card} 2 · Your AI assistant
:link: use.md
Runs the readme-review skill or prompt file.
:::

:::{card} 3 · Report
:link: expect.md
`README-review.md` and, if it saw the package, `README-ai-edited.md`.
:::

:::{card} 4 · You check it
:link: expect.md
Fix your README; verify every AI edit yourself.
:::

::::

**Maintainers' side** — step 7 feeds a new skill version back into step 2.

::::{grid} 1 2 3 3

:::{card} 5 · Feedback survey
:link: feedback.md
About 2 minutes, anonymized; answered by you, not AI.
:::

:::{card} 6 · Private repository
:link: security.md
One pull request per response; free text is vetted.
:::

:::{card} 7 · Maintainers
:link: feedback.md
Approve or reject, and write the next skill version.
:::

::::

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

readme-bot · [GitHub](https://github.com/social-science-data-editors/readme-bot) · MIT license · Based on the [Template README](https://social-science-data-editors.github.io/template_README/) v1.2.

Approved by Lars Vilhuber.
:::
