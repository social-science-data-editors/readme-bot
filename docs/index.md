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

{button}`How to use it <use.md>`
{button}`Give feedback <feedback.md>`

+++ {"kind": "justified"}

## What it is

readme-bot is a set of instructions for an AI assistant. You give the assistant your README, and optionally the replication package. It returns a list of differences from the Template README, ranked by how much they would slow a replicator down.

::::{grid} 1 1 3 3

:::{card} A · Structure
Are the Template's sections there, in a sensible order, with the Template's instructions and example text removed?
:::

:::{card} B · Content
Does each section say what a replicator needs: data access, file list, software versions, seed, runtime, run order, table and figure map, references?
:::

:::{card} C · Style
Is it short and plain? Lists over prose, steps in the order you run them, no filler, no AI-speak.
:::

::::

```{figure} images/workflow.svg
:alt: How readme-bot works, and how your feedback changes it. Top row, your side - 1 your README and optional package go to 2 an AI assistant with the readme-review skill, which writes 3 a report and an optional edited copy, which 4 you check. Bottom row, maintainers' side - 5 you answer a short feedback survey, 6 each response becomes a pull request in a private repository after automated vetting, 7 maintainers approve or reject it and write skill changes, which loop back into the skill at step 2.
:class: rb-infographic

**Claude-generated.** How a review works (top) and how your feedback changes the skill (bottom).
```

### Who it is for

- **Authors**, before submitting a replication package.
- **Data editors and journal staff**, as a first pass before a human review.
- **Replicators**, to see quickly what a README leaves out.

### What it is not

- Not a gate. The Template is a suggestion; the review says what differs and why it matters. It never says a README "fails".
- Not a journal decision. Passing or failing a data editor's check is still up to the data editor.
- Not a review of your research. It does not judge the paper, the methods, or the results, and it does not run your code.

+++ {"kind": "centered"}

## Four more steps

::::{grid} 1 2 4 4

:::{card} 2 · Security and privacy
:link: security.md
Where your files go, and what you are installing.
:::

:::{card} 3 · How to use it
:link: use.md
Coding agent, claude\.ai, or any chatbot.
:::

:::{card} 4 · What to expect
:link: expect.md
The report, the edited copy, and the priorities.
:::

:::{card} 5 · Give feedback
:link: feedback.md
Two minutes that decide what gets fixed next.
:::

::::

+++ {"class": "rb-footer-block"}

:::{div}
:class: rb-footer

readme-bot · [GitHub](https://github.com/social-science-data-editors/readme-bot) · MIT license · Based on the [Template README](https://social-science-data-editors.github.io/template_README/) v1.2. Page and infographic are Claude-generated.

Approved by Lars Vilhuber.
:::
