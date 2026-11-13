# Feedback survey questions

Use the same questions on either platform (Google Forms or Qualtrics). Keep the survey under 2 minutes.

Opening text (shown above Q1):

> Thanks for testing the README review skill. Do not paste confidential data, unpublished results, or full README text. Answers are reviewed by a person before they lead to any change. Anonymized summaries may appear in public GitHub issues.

| # | Question | Type | Required |
|---|---|---|---|
| Q0 | Skill version | Short text, prefilled from the link, hidden if the platform allows | Yes |
| Q1 | Your role | Single choice: author / data editor or journal staff / replicator / other | Yes |
| Q2 | How did you run it? | Single choice: Claude Code / claude.ai (skill upload) / other chatbot with the prompt file / other | Yes |
| Q3 | Mode | Single choice: review only / review + edited copy | Yes |
| Q4 | How useful was the report? | Scale 1–5 (1 = not useful, 5 = very useful) | Yes |
| Q5 | Did the report flag anything that was **not** a real problem? | Yes / no + text "Which finding, and why was it wrong?" | Yes |
| Q6 | Did it **miss** a problem you know about? | Yes / no + text "What was missed?" | Yes |
| Q7 | (If edited copy) Did the edited copy contain invented facts (versions, URLs, data sources, runtimes)? | Yes / no / did not check + text | If Q3 = edited copy |
| Q8 | Was the report the right length? | Too short / about right / too long | No |
| Q9 | Any other suggestion? | Long text | No |
| Q10 | May we quote your answers (anonymized) in a public GitHub issue? | Yes / no | Yes |
| Q11 | Email, if you want a reply | Short text (email validation) | No |

Q7 is the most important question for safety: any "yes" gets top priority in vetting.

Q10 = "no" means: use the response only in aggregate, never quoted or paraphrased in an issue.
