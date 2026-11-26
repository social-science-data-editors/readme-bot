---
title: Security and privacy
---

readme-bot is text: instructions an AI assistant follows. It does not communicate with any (other) servers. All changes are local - they are not sent to us! 

:::{dropdown} Where do my files go? — To the AI provider you choose. Nowhere else: not to us, not to your journal.
:open:

The skill has no code and makes no network calls. Whatever you give your AI assistant goes to that assistant's provider (Anthropic, OpenAI, Google, Microsoft, …) under your account's terms. 

- **Review only:** the AI reads only the README.
- **Review + edited copy:** the AI also accesses your replication package, including any data that may be there. Alternatively, you share only a file listing. A listing (for example the output of `find . -type f`) is enough for most checks and contains no data.
:::

:::{dropdown} My package has confidential or restricted data. — Do not make it available (check your ToU).

- Check your data use agreement and your institution's AI policy before giving any part of the package to an AI tool (not just this one).
- Safe default: give the README and a file listing, not the data.
- If your institution has an enterprise or education AI account (often with no-training or zero-data-retention (ZDR) terms), use that rather than a personal account.
:::

:::{dropdown} Will it run my code or change my files? — It is told not to. Keep an eye on it anyway.

- The skill tells the assistant not to run the replication code.
- It never modifies your README. It writes two new files: `README-review.md` and, in edit mode, `README-ai-edited.md`.
- Coding agents (Claude Code, Codex, Copilot agent mode, Cursor) can run commands on your machine. Keep their approval prompts on, and point them at a copy of the package.
:::

:::{dropdown} What exactly am I installing? — Five Markdown files and two one-line text files.

The skill has no scripts, no executables, no dependencies. You can read the Markdown files before you install:

- [`SKILL.md`](https://github.com/social-science-data-editors/readme-bot/blob/main/skills/readme-review/SKILL.md): the procedure.
- [`references/`](https://github.com/social-science-data-editors/readme-bot/tree/main/skills/readme-review/references): Template checklist, style guide, package checks, report format.
- `VERSION` and `FEEDBACK_URL`: the version number and the survey link.

The single-file prompt ([`readme-review-prompt.md`](https://github.com/social-science-data-editors/readme-bot/blob/main/prompts/readme-review-prompt.md)) is the same content, but concatenated.
:::

:::{dropdown} Can it make things up? — AI can. The skill is built to make that visible.

- The edited copy fills gaps only with facts found in the package (file names, seeds, package lists).
- Anything it cannot verify appears as `[AUTHOR TO VERIFY: …]` or `[AUTHOR TO PROVIDE: …]`.
- It is told never to invent data sources, versions, runtimes, URLs, DOIs, licenses, or hardware. It may still do so. Check every change before you use it.
- If you find an invented fact, tell us in the survey. Our target is zero.
:::

:::{dropdown} What happens to my survey answers? — Anonymized, reviewed by us, private by default.

- The survey runs on Cornell University's Qualtrics subscription with anonymized responses (no IP address or location stored).
- Email is optional, if you want a reply. Our scripts do not actually pull it into the pull request.
- Each response becomes one pull request in a **private** GitHub repository. A maintainer includes it or rejects it.
- We quote you in public (anonymized) only if you say yes.
- Before a maintainer reads it, free text is checked automatically for links, code, and instructions aimed at an AI. Nobody, human or AI, applies your text to the skill directly: a maintainer writes any change.

Details: [feedback plan](https://github.com/social-science-data-editors/readme-bot/blob/main/feedback/FEEDBACK_PLAN.md).
:::
