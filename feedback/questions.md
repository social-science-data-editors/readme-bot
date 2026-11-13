# Feedback survey questions (Qualtrics)

Keep the survey under 2 minutes. IDs Q1–Q13 are labels for this document; map them to the survey's real question IDs in `qualtrics-map.json`.

Opening text:

> Thanks for testing the README review skill. Your answers (without your email) are shared with the skill's maintainers in a private repository, where a maintainer decides whether to use them. Please do not include confidential data, unpublished results, or names. Please answer yourself; do not let an AI assistant fill in the survey. An assistant may help you draft the text for Q10.

Embedded data: `skill_version`, filled from the link.

| # | Question | Type | Required |
|---|---|---|---|
| Q1 | Your role | Single choice: author / data editor or journal staff / replicator / other | Yes |
| Q2 | How did you run it? | Single choice: Claude Code / claude.ai (skill upload) / other chatbot with the prompt file / other | Yes |
| Q3 | Mode | Single choice: review only / review + edited copy | Yes |
| Q4 | How useful was the report? | Scale 1–5 (1 = not useful, 5 = very useful) | Yes |
| Q5 | Did the report flag anything that was **not** a real problem? | Yes / no, with text entry on "yes": "Which finding, and why was it wrong?" | Yes |
| Q6 | Did it **miss** a problem you know about? | Yes / no, with text entry on "yes": "What was missed?" | Yes |
| Q7 | Did the edited copy contain invented facts (versions, URLs, data sources, runtimes)? | Yes / no / did not check, with text entry on "yes" | Shown if Q3 = edited copy |
| Q8 | Was the report the right length? | Too short / about right / too long | No |
| Q9 | Any other suggestion? | Long text | No |
| Q10 | Proposed changes to the skill. If you (or your AI assistant) analyzed why the review went wrong, paste the analysis and concrete changes here, e.g. "In `references/style-guide.md`, add: …". Plain text; no code to run. | Long text (up to 10,000 characters) | No |
| Q11 | Who wrote the Q10 text? | Single choice: I did / AI assistant, I reviewed it / AI assistant, not reviewed | Shown if Q10 is not empty |
| Q12 | May we quote your answers, anonymized, in public (e.g. in a change to the skill)? | Yes / No | Yes |
| Q13 | Email, if you want a reply (never published) | Short text, email validation | No |

- Q7 "yes" is flagged as priority in the PR.
- Q10 is untrusted input. The pull script vets it (and all other free text) before it reaches a maintainer; see "Security vetting" in [FEEDBACK_PLAN.md](FEEDBACK_PLAN.md). It is never applied to the skill directly: a maintainer rewrites any change they accept.
- Q12 is recorded as `public_quote_ok`. "No" still yields a (private) PR; the response is then used only in aggregate or in the maintainer's own words.
- Q13 is not mapped in `qualtrics-map.json`, so it never leaves Qualtrics.
