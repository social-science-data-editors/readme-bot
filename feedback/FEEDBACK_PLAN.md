# Feedback plan

How users report on the README review skill, how a person vets each response, and how vetted feedback becomes a change via pull request.

## Principles

- No response changes the skill without a person reading it, deciding, and writing the issue.
- Raw responses stay in the survey platform. The public repo gets only anonymized, vetted summaries.
- Every response is tied to a skill version, so feedback can be matched to the prompt that produced it.

## Flow

1. User runs the skill. The report ends with a feedback link carrying the skill version.
2. User fills in the survey ([questions](questions.md)).
3. Response lands in a private sheet or Qualtrics project with status `new`.
4. Vetter triages on a fixed schedule (suggested: every two weeks).
5. Accepted feedback → GitHub issue using the **Vetted feedback** template, anonymized.
6. Maintainer (or contributor) opens a PR that fixes the issue, bumps `VERSION`, rebuilds, and updates `CHANGELOG.md`.
7. Vetter records the issue/PR link against the response and, if the respondent left an email, replies.

## Option A: Google Forms

### Deploy

1. Create the form from a shared/team Google account, not a personal one. Add at least two maintainers as editors.
2. Add the questions from [questions.md](questions.md). Mark Q0 as short answer; add a description "Filled in automatically".
3. Settings:
   - Responses → "Collect email addresses": **off** (Q11 is optional instead).
   - "Limit to 1 response": off (no sign-in required).
4. Responses → "Link to Sheets" → create a new sheet. Restrict sharing to maintainers.
5. In the sheet, add vetting columns to the right of the form columns: `status` (new / accepted / rejected / duplicate / needs-info), `vetter`, `vetted_on`, `summary` (anonymized paraphrase), `issue_url`. Add data validation on `status`.
6. Get the prefilled link: ⋮ menu → "Get pre-filled link" → type `VERSION` in Q0 → "Get link". The link looks like `https://docs.google.com/forms/d/e/<id>/viewform?usp=pp_url&entry.<n>=VERSION`.
7. Replace the trailing `VERSION` with `{VERSION}` and put the link into `skills/readme-review/FEEDBACK_URL` via PR (see "Wire the link" below).
8. Optional: Tools → Notification rules on the sheet → email maintainers on new responses.

### Notes

- Free, fast to set up, easy to share.
- Q0 cannot be truly hidden; the description tells users not to change it.
- Check whether your institution allows research-adjacent data in Google Workspace.

## Option B: Qualtrics

### Deploy

1. Create a survey in the institutional Qualtrics account. Share the project with maintainers (Collaborate → edit + view results).
2. Survey flow → add **Embedded Data** at the top: field `skill_version`. Qualtrics fills it from the URL parameter of the same name. This replaces Q0; it is truly hidden.
3. Add Q1–Q11 from [questions.md](questions.md). Use display logic for Q7 (show if Q3 = edited copy).
4. Survey options → Security → **Anonymize responses**: on (strips IP and location). Q11 remains if the user chooses to give it.
5. Data & Analysis → add embedded-data fields for vetting: `status`, `vetter`, `vetted_on`, `summary`, `issue_url`. Vetters edit these in Data & Analysis (Edit Response) or keep them in an exported vetting sheet.
6. Distributions → Anonymous link. The feedback URL is `https://<org>.qualtrics.com/jfe/form/SV_<id>?skill_version={VERSION}`.
7. Put that into `skills/readme-review/FEEDBACK_URL` via PR.
8. Optional: Actions → email task to maintainers on each new response.

### Notes

- Usually covered by an institutional license and data agreement; better if feedback may ever be used in research (check IRB rules before publishing any analysis of responses).
- Hidden version field, display logic, and anonymization are built in.
- Slightly more setup; sharing with external co-maintainers may need guest accounts.

## Recommendation

- Use **Qualtrics** if an institutional license is available: responses may contain fragments of unpublished replication packages, and the institutional data agreement plus built-in anonymization is the safer home.
- Use **Google Forms** for a quick pilot or if co-maintainers outside the institution need direct access.
- The rest of the plan (vetting, issues, PRs) is identical.

## Vetting

Done by a maintainer, on a schedule. For each `new` response:

1. **Safety first.** If Q7 = yes (invented facts in the edited copy), handle it now, not on schedule.
2. **Screen.** Reject spam, off-topic, or unusable responses (`rejected`, note why).
3. **Scrub.** If the response contains confidential details, names, or README text: do not copy them anywhere. Write the `summary` in your own words.
4. **Classify.**
   - Skill problem (false positive, missed issue, invented content, wrong tone, too long) → `accepted`.
   - Disagreement with the Template itself → `accepted`, but the issue goes to `social-science-data-editors/template_README`, not here.
   - Already reported → `duplicate`, link the existing issue.
   - Cannot tell what went wrong → `needs-info` (reply if an email was given; otherwise `rejected` after one cycle).
5. **Respect consent.** If Q10 = no, do not quote or paraphrase the response in an issue. Count it only in aggregate.
6. **File.** For `accepted`: open an issue with the **Vetted feedback** template. Paste the `summary`, not the raw text. Record `issue_url`, `vetter`, `vetted_on`.

Retention: delete raw responses 12 months after they are vetted; the sheet row (status, summary, issue link) may stay.

## Integration via pull request

1. Branch from the default branch. Edit only `skills/readme-review/` (and docs).
2. Bump `skills/readme-review/VERSION` (semantic versioning):
   - patch: wording, examples, style rules;
   - minor: new or changed checks;
   - major: changed report format or output file names.
3. Run `scripts/build.sh` to regenerate `prompts/readme-review-prompt.md`. CI fails if it is stale.
4. Add a `CHANGELOG.md` entry that cites the issue.
5. Open the PR. Write `Closes #<issue>` in the body. The PR template asks the author to confirm the issue was vetted.
6. Merge after review by a maintainer other than the PR author when possible.
7. After merge: tag `v<VERSION>`; the release workflow attaches `readme-review.zip`.

### Wire the link

Once the survey exists, one small PR:

- Put the URL (with `{VERSION}`) in `skills/readme-review/FEEDBACK_URL`.
- Bump the patch version and run `scripts/build.sh`.

### Optional automation (not required)

Automation may help with bookkeeping but never replaces the vetter's decision.

- Google Forms: an Apps Script on the sheet can open a GitHub issue when a vetter sets `status` = `accepted`, using only the `summary` column. Store a fine-grained token (Issues: write, this repo only) in Script Properties, never in the script.
- Qualtrics: a Workflow with a Web Service task can do the same, triggered on the `status` field.
- Either way, issues created this way are labeled `feedback:vetted` and contain only the vetter's summary.

## Measures

Review per skill version, every release:

- number of responses;
- mean usefulness (Q4);
- share reporting false findings (Q5), missed issues (Q6), invented facts (Q7). Target for Q7: zero.
