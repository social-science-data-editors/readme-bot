# Feedback plan

Users rate the README review skill in a Qualtrics survey. A scheduled GitHub Action in the **private** repository `social-science-data-editors/readme-bot-feedback` pulls new responses and opens **one pull request per response** there. A maintainer includes a response by **approving** its PR (it then merges automatically) or rejects it by **closing** the PR. Skill changes based on included responses arrive as separate PRs in this (public) repository.

## Where things live

- This repo (public): skill, survey questions ([questions.md](questions.md)), field map (`qualtrics-map.json`), script (`scripts/qualtrics_to_prs.py`).
- `readme-bot-feedback` (private): the two workflows, the response PRs, and the included responses (`responses/`).

The private repo's workflow checks out this repo to get the script and field map, so code is reviewed in public and data stays private.

## Flow

1. User runs the skill. The report ends with the survey link, carrying the skill version.
2. User answers the survey.
3. Daily, `feedback-pull.yml` in the private repo runs the script:
   - exports all responses through the Qualtrics API;
   - skips unfinished responses and responses that already have a PR (open, merged, or closed);
   - drops the email question, replaces any email address in free text with `[email removed]`, truncates long text;
   - records whether the respondent allows public quoting (Q10) as `public_quote_ok`;
   - opens a PR adding `responses/<date>-<responseId>.md`, labeled `feedback:response`. Responses reporting invented facts are flagged in the PR body.
4. Maintainer reviews the PR:
   - **include**: approve. `feedback-merge.yml` checks that the approver has write access and that the PR only touches `responses/`, then squash-merges and deletes the branch;
   - **redact, then include**: edit the file on the branch, then approve;
   - **reject**: close. The branch is deleted.
5. Periodically (suggested: each release), a maintainer reads `responses/` and opens a PR in this repo changing the skill. Cite response IDs. Quote or closely paraphrase only responses with `public_quote_ok: true`.

## Deploy

1. **Survey.** In the institutional Qualtrics account, create the survey from [questions.md](questions.md).
   - Survey flow → Embedded Data at the top: field `skill_version` (filled from the URL parameter of the same name).
   - Survey options → Security → Anonymize responses: on.
   - Q7 display logic: show if Q3 = review + edited copy.
   - Share the project with co-maintainers (Collaborate).
2. **Link.** Distributions → Anonymous link. Write `https://<org>.qualtrics.com/jfe/form/SV_<id>?skill_version={VERSION}` into `skills/readme-review/FEEDBACK_URL` (PR in this repo; bump patch version, run `scripts/build.sh`).
3. **Field map.** Export one test response as JSON (or use Tools → Auto-number questions) and put the real question IDs into `feedback/qualtrics-map.json`. Set `consent_yes` to the exact label of the "Yes" choice of Q10. Check with:
   `scripts/qualtrics_to_prs.py --from-file <export.json> --dry-run --repo-dir /tmp/x`
   Do not commit the export.
4. **API token.** Qualtrics → Account settings → Qualtrics IDs → generate token, from an account that owns or shares the survey. (If the button is missing, ask the Qualtrics brand admin to enable API access.)
5. **Private repo settings** (`readme-bot-feedback` → Settings):
   - Secrets and variables → Actions → **secret** `QUALTRICS_API_TOKEN`; **variables** `QUALTRICS_BASE_URL` (data-center URL shown under Qualtrics IDs, e.g. `https://cornell.ca1.qualtrics.com`) and `QUALTRICS_SURVEY_ID`. Optional variable `README_BOT_REF` (default `main`) to pin the script version.
   - Actions → General → Workflow permissions: "Read and write"; tick "Allow GitHub Actions to create and approve pull requests".
6. **Test.** Submit a test response. In the private repo: Actions → "Pull feedback from Qualtrics" → Run workflow. Approve the resulting PR; check that it merged. Delete the test file.

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
