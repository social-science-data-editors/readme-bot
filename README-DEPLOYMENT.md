# Deployment & PR previews

The site is written in Markdown in `docs/` and built with
[Jupyter Book 2](https://jupyterbook.org/) (mystmd); see `docs/myst.yml`.
`index.md` is the menu-less front page; the other pages get the sidebar.
`scripts/build.sh` stamps the skill version, approvers and feedback link into
`docs/index.md`, `expect.md` and `feedback.md`; edit `skills/readme-review/VERSION` and
`FEEDBACK_URL`, not those lines.

Two workflows:

- [build.yml](.github/workflows/build.yml) — every push and pull request.
  Builds the prompt and skill zip and fails if the committed `prompts/` or the
  stamps in `docs/` are stale.
- [site.yml](.github/workflows/site.yml) — builds the site (`jupyter-book build
  --html --strict`).
  - On `main`: deploys to GitHub Pages (Settings → Pages → Source: **GitHub
    Actions**; switched from "Deploy from branch" on 2026-11-26).
  - On pull requests opened from a branch of this repository (not a fork):
    deploys to [Cloudflare Pages](https://pages.cloudflare.com/) as a per-PR
    preview and posts (or updates) a PR comment with the link, e.g.
    `https://pr-<PR number>.readme-bot.pages.dev`.

Forked PRs skip the preview, since forks can't read repository secrets.

## Local preview

```bash
docs/_setup.sh                                   # creates docs/.venv (idempotent)
cd docs && .venv/bin/jupyter-book start          # live preview at http://localhost:3000
```

## One-time setup

The Cloudflare account and API token are the same ones used by
[guidance](https://github.com/social-science-data-editors/guidance) (see its
`README-DEPLOYMENT.md` for how the token was created). The token needs
`Account → Cloudflare Pages: Edit`.

1. **Set the repository secrets** from 1Password, reusing the `ssde-guidance`
   token:

   ```bash
   op item get "cloudflare.com" --fields "API token: ssde-guidance" | gh secret set CLOUDFLARE_API_TOKEN
   op item get "cloudflare.com" --fields "Account ID" | gh secret set CLOUDFLARE_ACCOUNT_ID
   gh secret list
   ```

2. **Create the Cloudflare Pages project** (Direct Upload, not connected to
   Git), named like the GitHub repository:

   ```bash
   npx wrangler pages project list
   npx wrangler pages project create "$(gh repo view --json name -q .name)" --production-branch main --force
   ```

   Recent Wrangler versions (4.16x) try to send `pages project create` to
   Cloudflare Workers and fail with "Missing entry-point"; `--force` creates a
   classic Pages project instead, which is what CI deploys to. It's only
   needed once. (Done for `readme-bot` on 2026-11-26.)

   If the name is taken on Cloudflare, create another one and hard-code it as
   `CF_PAGES_PROJECT` in the `preview` job.

## Notes

- `pages.dev` previews are public by default.
- Each PR leaves a deployment (alias `pr-<number>`) in Cloudflare; harmless,
  deletable under the project's **Deployments** tab.
- Dependabot PRs get no preview unless the secrets are also added as
  Dependabot secrets.
- `Project not found` = project name/account mismatch; `Authentication error`
  = wrong account ID or token lacking *Cloudflare Pages: Edit*.
