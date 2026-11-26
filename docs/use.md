---
title: How to use it
---

Pick the card that matches your tool. All three give the same review. Links always point to the current version.

::::{grid} 1 1 3 3
:class: col-page-right

:::{card} Claude Code (or another agent that reads skills)
:header: Coding agent

1. Copy the folder [`skills/readme-review/`](https://github.com/social-science-data-editors/readme-bot/tree/main/skills/readme-review) into `.claude/skills/` in the package, or into `~/.claude/skills/` for all projects.
2. Open the package folder.
3. Ask: _"Review the README in this package."_
:::

:::{card} claude\.ai
:header: Chat with skills

1. Download [`readme-review.zip`](https://github.com/social-science-data-editors/readme-bot/releases/latest/download/readme-review.zip) (latest release).
2. Settings → Capabilities → Skills → upload the zip.
3. In a new chat, attach the README (and the package zip or a file listing). Ask for a review.
:::

:::{card} ChatGPT, Gemini, Copilot, others
:header: Any chatbot

1. Download [`readme-review-prompt.md`](https://github.com/social-science-data-editors/readme-bot/blob/main/prompts/readme-review-prompt.md).
2. Paste it into the chat, or attach it.
3. Attach the README, and if you can, the package or its file listing.
:::

::::

## Tips

- Say _"review only"_ if you do not want an edited copy.
- Large package or restricted data? Give a file listing instead of the files: `find . -type f > files.txt` (macOS, Linux) or `dir /s /b > files.txt` (Windows).
- READMEs in PDF, Word, LaTeX, or plain text work. The edited copy is always Markdown.
- Non-English README? It is reviewed anyway; the edited copy is in English.
