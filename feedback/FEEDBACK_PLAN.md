# Feedback plan

Users rate the README review skill in a Qualtrics survey. A scheduled GitHub Action pulls new responses and opens **one pull request per response**. A maintainer includes a response by **approving** its PR (it then merges automatically) or rejects it by **closing** the PR. Skill changes based on included responses arrive in separate PRs.

## Flow

1. User runs the skill. The report ends with the survey link, carrying the skill version.
2. User answers the survey ([questions](questions.md)), including consent to publish (Q10).
3. Daily, `feedback-pull.yml` runs `scripts/qualtrics_to_prs.py`:
   - exports all responses through the Qualtrics API;
   - skips unfinished responses and responses without consent;
   - skips responses that already have a PR (open, merged, or closed);
   - drops the email question, replaces any email address in free text with `[email removed]`, truncates long text;
   - opens a PR adding `feedback/responses/<date>-<responseId>.md`, labeled `feedback:response`. Responses reporting invented facts are flagged in the PR body.
4. Maintainer reviews the PR:
   - **include**: approve. `feedback-merge.yml` checks that the approver has write access and that the PR only touches `feedback/responses/`, then squash-merges and deletes the branch;
   - **redact, then include**: edit the file on the branch, then approve;
   - **reject**: close. The branch is deleted.
5. Periodically (suggested: each release), a maintainer reads `feedback/responses/` and opens a PR changing the skill, citing the response files. That PR follows the normal process (below).

## Privacy

This repository is public. **Everything in a feedback PR, including closed (rejected) PRs, stays publicly visible.** Therefore:

- The survey says so up front, and only responses with Q10 = "Yes" are turned into PRs.
- Responses without consent stay in Qualtrics only; count them in aggregate.
- The automatic email scrub is a safety net, not a guarantee. If a response contains confidential details, close the PR and ask a GitHub admin to delete it via GitHub Support if needed.
- If this exposure is not acceptable, point the workflow at a private repository (e.g. `readme-bot-feedback`) instead; nothing else changes.

## Deploy (Qualtrics)

1. **Survey.** In the institutional Qualtrics account, create the survey from [questions.md](questions.md).
   - Survey flow → Embedded Data at the top: field `skill_version` (filled from the URL parameter of the same name).
   - Survey options → Security → Anonymize responses: on.
   - Q7 display logic: show if Q3 = review + edited copy.
   - Share the project with co-maintainers (Collaborate).
2. **Link.** Distributions → Anonymous link. Write `https://<org>.qualtrics.com/jfe/form/SV_<id>?skill_version={VERSION}` into `skills/readme-review/FEEDBACK_URL`.
3. **Field map.** Export one test response as JSON (or use Tools → Auto-number questions) and put the actual question IDs into `feedback/qualtrics-map.json`. Set `consent_yes` to the exact label of the "Yes" choice of Q10. Check with:
   `scripts/qualtrics_to_prs.py --from-file <export.json> --dry-run`
4. **API token.** Account settings → Qualtrics IDs → generate token. Use an account that owns or shares the survey. (API access must be enabled for the account; ask the Qualtrics brand admin if the button is missing.)
5. **GitHub settings** (repository → Settings):
   - Secrets and variables → Actions → **secret** `QUALTRICS_API_TOKEN`; **variables** `QUALTRICS_BASE_URL` (e.g. `https://cornell.ca1.qualtrics.com`, the data-center URL shown in Qualtrics IDs) and `QUALTRICS_SURVEY_ID`.
   - Actions → General → Workflow permissions: "Read and write", and tick "Allow GitHub Actions to create and approve pull requests".
6. **Test.** Actions → "Pull feedback from Qualtrics" → Run workflow. Submit a test response first; approve its PR; check it merged; delete the file afterwards.

The pull workflow does nothing until `QUALTRICS_BASE_URL` is set, so merging this before setup is safe.

## Notes on the automation

- PRs opened by the workflow token do not trigger other workflows (GitHub rule). `build.yml` therefore does not run on feedback PRs; it does not need to.
- Approval by someone without write access is ignored (the merge job fails and says why).
- If you want branch protection that requires an approval on `main`, the same approval satisfies it.
- A response is only ever processed once: the dedup key is the PR branch `feedback/response-<responseId>`.

## Changing the skill (all PRs that are not feedback PRs)

1. Branch from `main`. Edit `skills/readme-review/` (and docs).
2. Bump `skills/readme-review/VERSION`: patch = wording/style rules; minor = new or changed checks; major = changed report format or output file names.
3. Run `scripts/build.sh`; commit the regenerated `prompts/readme-review-prompt.md` (CI fails if stale).
4. Add a `CHANGELOG.md` entry citing the response files or issues that motivated it.
5. Merge after review; tag `v<VERSION>`. The release gets `readme-review.zip`.

Template disagreements (as opposed to skill problems) go to `social-science-data-editors/template_README` as issues.

## Measures

Per skill version, from `feedback/responses/` (included) and Qualtrics (all):

- number of responses; mean usefulness (Q4);
- share reporting false findings (Q5), missed issues (Q6), invented facts (Q7). Target for Q7: zero.
