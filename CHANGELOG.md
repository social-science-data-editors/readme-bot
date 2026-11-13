# Changelog

## 0.1.0 — 2026-11-13

- First version of the `readme-review` skill: structure, content, and style checks against Template README v1.2; optional `README-ai-edited` copy when the package is available.
- Generated single-file prompt.
- Feedback pipeline: Qualtrics survey → daily workflow in the private `readme-bot-feedback` repo opens one PR per response → maintainer approval merges it.
- Survey free-text field for proposed skill changes (may be drafted by the user's AI assistant); all free text vetted by the pull script and flagged PRs labeled `feedback:security-flag`. The skill points to the survey but leaves answering it to the human.
- Survey defined in `feedback/survey-spec.json` and created via the Qualtrics API (`scripts/create_survey.py`), which writes the field map (including the survey ID) and `FEEDBACK_URL`. The exported QSF is committed as `feedback/survey.qsf`.
- Survey `SV_3UW3jQbuNPpLtSC` built via the API; anonymized, bot detection and security fields on. Responses with a reCAPTCHA score below 0.5 are flagged as likely bots.
