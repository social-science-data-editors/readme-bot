# Feedback survey questions (Qualtrics)

Keep the survey under 2 minutes. The source of truth is [survey-spec.json](survey-spec.json); `scripts/create_survey.py` builds the survey from it via the Qualtrics API and writes the real question IDs to `qualtrics-map.json`. The table below is generated (`scripts/build.sh`); edit the spec, not the table. IDs Q1–Q13 are labels (Qualtrics "data export tags"), not Qualtrics question IDs.

Opening text (shown above Q1): see `intro` in the spec. It asks respondents to answer themselves; an AI assistant may only help draft Q10.

Embedded data: `skill_version`, filled from the link.

<!-- BEGIN GENERATED TABLE -->
| # | Page | Question | Type | Required | Shown if |
|---|---|---|---|---|---|
| Q1 | 1 | Your role | Single choice: Author / Data editor or journal staff / Replicator / Other | Yes |  |
| Q2 | 1 | How did you run it? | Single choice: Claude Code / claude.ai (skill upload) / Other chatbot with the prompt file / Other | Yes |  |
| Q3 | 1 | Mode | Single choice: Review only / Review + edited copy | Yes |  |
| Q4 | 2 | How useful was the report? (1 = not useful, 5 = very useful) | Scale: 1 / 2 / 3 / 4 / 5 | Yes |  |
| Q5 | 2 | Did the report flag anything that was **not** a real problem? | Single choice: Yes / No | Yes |  |
| Q6 | 2 | Did it **miss** a problem you know about? | Single choice: Yes / No | Yes |  |
| Q7 | 2 | Did the edited copy contain invented facts (versions, URLs, data sources, runtimes)? | Single choice: Yes / No / Did not check | Yes | Q3 = Review + edited copy |
| Q8 | 2 | Was the report the right length? | Single choice: Too short / About right / Too long | No |  |
| Q5a | 3 | Which finding was not a real problem, and why? | Long text | No | Q5 = Yes |
| Q6a | 3 | What was missed? | Long text | No | Q6 = Yes |
| Q7a | 3 | Which facts were invented? | Long text | No | Q7 = Yes |
| Q9 | 3 | Any other suggestion? | Long text | No |  |
| Q10 | 3 | Proposed changes to the skill. If you (or your AI assistant) analyzed why the review went wrong, paste the analysis and concrete changes here, e.g. "In references/style-guide.md, add: ...". Plain text; no code to run. | Long text | No |  |
| Q11 | 4 | Who wrote the Q10 text? | Single choice: I did / AI assistant, I reviewed it / AI assistant, not reviewed | No | Q10 not empty |
| Q12 | 4 | May we quote your answers, anonymized, in public (e.g. in a change to the skill)? | Single choice: Yes / No | Yes |  |
| Q13 | 4 | Email, if you want a reply (never published) | Short text, email validation | No |  |
<!-- END GENERATED TABLE -->

- Each page is one Qualtrics block; "Shown if" always refers to an earlier page. Follow-up text questions (Q5a–Q7a) are separate questions, not text boxes on a choice, so they export under a predictable key (`QIDn_TEXT`).
- Q7 "Yes" is flagged as priority in the PR.
- Q10 is untrusted input. The pull script vets it (and all other free text) before it reaches a maintainer; see "Security vetting" in [FEEDBACK_PLAN.md](FEEDBACK_PLAN.md). It is never applied to the skill directly: a maintainer rewrites any change they accept.
- Q12 is recorded as `public_quote_ok`. "No" still yields a (private) PR; the response is then used only in aggregate or in the maintainer's own words.
- Q13 has no `field`, so it is not in `qualtrics-map.json` and never leaves Qualtrics.
