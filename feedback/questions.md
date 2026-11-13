# Feedback survey questions (Qualtrics)

Keep the survey under 2 minutes. IDs Q1–Q11 are labels for this document; map them to the survey's real question IDs in `qualtrics-map.json`.

Opening text:

> Thanks for testing the README review skill. If you agree (last question), your answers will be published in a public GitHub pull request on social-science-data-editors/readme-bot, where a maintainer decides whether to include them. Do not include confidential data, unpublished results, names, or README text.

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
| Q10 | May we publish your answers (without your email) in a public GitHub pull request? | Yes / No | Yes |
| Q11 | Email, if you want a reply (never published) | Short text, email validation | No |

- Q7 "yes" is flagged as priority in the PR.
- Q10 "No": the response stays in Qualtrics; it is never turned into a PR.
- Q11 is not mapped in `qualtrics-map.json`, so it never leaves Qualtrics.
