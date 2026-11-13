# Changelog

## 0.1.0 — 2026-11-13

- First version of the `readme-review` skill: structure, content, and style checks against Template README v1.2; optional `README-ai-edited` copy when the package is available.
- Generated single-file prompt.
- Feedback pipeline: Qualtrics survey → daily workflow in the private `readme-bot-feedback` repo opens one PR per response → maintainer approval merges it.
- Survey free-text field for proposed skill changes (may be drafted by the user's AI assistant); all free text vetted by the pull script and flagged PRs labeled `feedback:security-flag`. The skill points to the survey but leaves answering it to the human.
