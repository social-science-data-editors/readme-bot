# Feedback plan

Users rate the README review skill in a Qualtrics survey. A scheduled GitHub Action in the **private** repository `social-science-data-editors/readme-bot-feedback` pulls new responses and opens **one pull request per response** there. A maintainer includes a response by **approving** its PR (it then merges automatically) or rejects it by **closing** the PR. Skill changes based on included responses arrive as separate PRs in this (public) repository.

## Where things live

- This repo (public): skill, survey spec (`survey-spec.json`, rendered in [questions.md](questions.md)) and the script that creates the survey (`scripts/create_survey.py`), survey definition (`survey.qsf`, see [below](#survey-definition-qsf)), field map (`qualtrics-map.json`), script (`scripts/qualtrics_to_prs.py`).
- `readme-bot-feedback` (private): the two workflows, the response PRs, and the included responses (`responses/`).

The private repo's workflow checks out this repo to get the script and field map, so code is reviewed in public and data stays private.

## Flow

1. User runs the skill. The report ends with the survey link, carrying the skill version. The skill tells the agent that the survey is for the human and not to fill it in.
2. User answers the survey. Optionally, they ask their AI assistant to analyze why the review went wrong and paste its concrete proposals into Q10 (free text), saying in Q11 who wrote it.
3. Daily, `feedback-pull.yml` in the private repo runs the script:
   - exports all responses through the Qualtrics API;
   - skips unfinished responses and responses that already have a PR (open, merged, or closed);
   - drops the email question, replaces any email address in free text with `[email removed]`, truncates long text;
   - vets all free text (see [Security vetting](#security-vetting));
   - records whether the respondent allows public quoting (Q12) as `public_quote_ok`;
   - opens a PR adding `responses/<date>-<responseId>.md`, labeled `feedback:response`. Responses reporting invented facts are flagged in the PR body; responses with vetting flags also get the label `feedback:security-flag`.
4. Maintainer reviews the PR:
   - **include**: approve. `feedback-merge.yml` checks that the approver has write access, that the PR only touches `responses/`, and that it has no `feedback:security-flag` label, then squash-merges and deletes the branch;
   - **redact, then include**: edit the file on the branch, then approve;
   - **reject**: close. The branch is deleted.
5. Periodically (suggested: each release), a maintainer reads `responses/` and opens a PR in this repo changing the skill. Cite response IDs. Quote or closely paraphrase only responses with `public_quote_ok: true`. Proposals (Q10) are never applied verbatim: the maintainer writes the change.

## Security vetting

All free text is untrusted. Q10 in particular invites text pasted from an AI assistant, which may carry prompt injection aimed at whoever (or whatever) later reads `responses/` to change the skill.

Automated, in `scripts/qualtrics_to_prs.py` (runs in the private repo's pull workflow):

- removes invisible characters (zero-width, bidi controls, Unicode tags) and email addresses; truncates (2,000 characters; 10,000 for Q10);
- flags text that contains: instructions aimed at an AI ("ignore previous instructions", role tags), commands or code (fences, `curl`, `| sh`, …), links, HTML, long encoded blobs, mentions of credentials or data transfer, or references to repo automation (`.github`, workflows, tokens);
- stores every free-text answer inside a code fence, so nothing renders as Markdown or HTML;
- lists flags in the response file (`security_flags`), in the PR body, and as the label `feedback:security-flag`.

The checks are pattern-based: they catch the obvious cases and prompt a closer look, not prove text safe. Unflagged text is still untrusted.

Manual, by the maintainer:

- **Before approving**: read the free text as data. Delete instructions, commands, and links that are not needed to understand the feedback (edit the file on the branch), or close the PR.
- **When changing the skill**: write the change yourself. If an AI assistant helps you read `responses/`, tell it the files are untrusted data, not instructions, and do not give it write access to this repo or any token in that session. Do not follow links from responses.
- **In this repo**: skill changes arrive only as reviewed PRs (CI checks the generated prompt; a maintainer merges).

In `readme-bot-feedback`, `feedback-merge.yml` refuses to merge a PR labeled `feedback:security-flag`. After checking the text, the maintainer removes the label, then approves again (or re-runs the merge job).

## Survey definition (QSF)

`feedback/survey.qsf` is the definition of the live survey, exported by hand from Qualtrics. The survey is built from `survey-spec.json` through the API; the QSF is never written by hand or by a script, only downloaded after every change to the survey.

- **What it is**: Qualtrics Survey Format, a JSON file with the questions, choices, display logic, survey flow (including the `skill_version` embedded-data field), and survey options. It holds no responses and no API token.
- **Why it is kept**:
  - record of what respondents saw, per skill version (diffs show survey changes);
  - recreate the survey (Create project → Survey → From a file) if it is lost or moves to another account;
  - source of truth for question IDs: `qualtrics-map.json` must use the `QuestionID`s (`QID…`) in it.
- **How to download**: open the survey in Qualtrics → Tools → Import/Export → Export survey. Save as `feedback/survey.qsf` (replace the old file).
- **Before committing**:
  - pretty-print, so diffs are readable: `python3 -m json.tool --indent 1 <download>.qsf > feedback/survey.qsf`;
  - it contains identifiers (`SurveyID`, `SurveyOwnerID`/`CreatorID` user IDs, `SurveyBrandID`). They are not credentials; the survey ID is already public in the survey link. Check that no question text or default answer contains anything private;
  - check that `qualtrics-map.json` still matches: each `QIDn` in the map exists in the QSF (`SurveyElements` with `Element: "SQ"`, `Payload.QuestionID`). Text-entry fields are exported as `QIDn_TEXT`.
- **When**: after creating the survey, and after every edit in Qualtrics. Commit it in the same PR that updates `survey-spec.json` (and so `questions.md`) and `qualtrics-map.json`, and note the change, with its date, in `CHANGELOG.md`, so responses can be matched to the survey version by date.
- **Changing a live survey**: `create_survey.py` only creates new surveys. For small edits (wording, a choice), edit in Qualtrics, mirror the change in `survey-spec.json`, and re-export the QSF; for new questions, add them in Qualtrics and add their `QID`s to the map by hand (check against the QSF). For a redesign, create a new survey with the script: it gets a new survey ID and link, and responses to the old survey are no longer pulled.

## Deploy

1. **API token.** Qualtrics → Account settings → Qualtrics IDs → generate token. (If the button is missing, ask the Qualtrics brand admin to enable API access.) Note the data-center URL shown there (e.g. `https://cornell.ca1.qualtrics.com`).
2. **Create the survey** from `survey-spec.json`, on a branch of this repo:
   - check first: `scripts/create_survey.py --dry-run` (prints every API call, contacts nothing);
   - then: `QUALTRICS_BASE_URL=… QUALTRICS_API_TOKEN=… scripts/create_survey.py`.

   It creates one block per page, the questions with required and display logic, and the `skill_version` embedded-data field; publishes and activates the survey; and writes `feedback/qualtrics-map.json` (survey ID, real question IDs) and `skills/readme-review/FEEDBACK_URL` (anonymous link).
3. **By hand in Qualtrics**, then commit:
   - Survey options → Security → Anonymize responses: on;
   - Preview the survey; check display logic (Q7, Q5a–Q7a, Q11);
   - share the project with co-maintainers (Collaborate);
   - export the QSF to `feedback/survey.qsf` ([Survey definition](#survey-definition-qsf));
   - submit one test response, export it as JSON, and check the map: `scripts/qualtrics_to_prs.py --from-file <export.json> --dry-run --repo-dir /tmp/x`. Do not commit the export;
   - commit map, `FEEDBACK_URL`, and QSF; bump patch version; run `scripts/build.sh`; open a PR.
4. **Private repo settings** (`readme-bot-feedback` → Settings):
   - Secrets and variables → Actions → **secret** `QUALTRICS_API_TOKEN` (from an account that owns or shares the survey); **variable** `QUALTRICS_BASE_URL`. The survey ID comes from `qualtrics-map.json` in this repo. Optional variables: `QUALTRICS_SURVEY_ID` (overrides the map), `README_BOT_REF` (default `main`, pins the script version).
   - Actions → General → Workflow permissions: "Read and write"; tick "Allow GitHub Actions to create and approve pull requests".
   - Or from the command line with `gh` (interactively or from a `.env` file): see "Set them with `gh`" in the `readme-bot-feedback` README.
5. **Test.** Submit a test response. In the private repo: Actions → "Pull feedback from Qualtrics" → Run workflow. Approve the resulting PR; check that it merged. Delete the test file.

The pull workflow does nothing until `QUALTRICS_BASE_URL` is set.

## Notes on the automation

- This repo is public, so the private repo can check it out with the default workflow token. No cross-repo token is needed.
- PRs opened by the workflow token do not trigger other workflows (GitHub rule). Nothing else needs to run on them.
- Approval by someone without write access is ignored (the merge job fails and says why).
- Branch protection requiring one approval on the private repo's `main` is compatible: the same approval satisfies it.
- A response is processed once: the dedup key is the PR branch `feedback/response-<responseId>`.

## Changing the skill (PRs in this repo)

1. Branch from `main`. Edit `skills/readme-review/` (and docs).
2. Bump `skills/readme-review/VERSION`: patch = wording/style rules; minor = new or changed checks; major = changed report format or output file names.
3. Run `scripts/build.sh`; commit the regenerated `prompts/readme-review-prompt.md` (CI fails if stale).
4. Add a `CHANGELOG.md` entry citing response IDs or issues.
5. Merge after review; tag `v<VERSION>`. The release gets `readme-review.zip`.

Template disagreements (as opposed to skill problems) go to `social-science-data-editors/template_README` as issues.

## Measures

Per skill version, from `responses/` (included) and Qualtrics (all):

- number of responses; mean usefulness (Q4);
- share reporting false findings (Q5), missed issues (Q6), invented facts (Q7). Target for Q7: zero.
- share with proposals (Q10), by author (Q11), and share flagged by vetting.
