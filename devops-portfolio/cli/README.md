# DevOps Portfolio CLI

Developer-facing CLI for GitHub API and workflow automation (PR status, workflow trigger, release draft).

## Commands

- `portfolio pr status [number]` — Fetch PR, show status, checks, mergeable state (GitHub REST).
- `portfolio checks run` / `workflow trigger` — Trigger workflow dispatch or re-run checks.
- `portfolio release draft` — Create draft release, optional asset upload.

Auth: `GITHUB_TOKEN` or `GH_TOKEN`; override with `--token`. Repo: `--owner` and `--repo`, or `GH_REPO_OWNER` / `GH_REPO_NAME`.

Output: human-readable by default; use `--json` for scripting.

## Build and run

```bash
go build -o portfolio .
./portfolio pr status --owner OWNER --repo REPO 1
```

## APIs used

- **REST**: Pull Requests, Checks (ListCheckRunsForRef), Repos. See [GitHub REST API](https://docs.github.com/en/rest).
- **Rate limits**: 5,000/hr authenticated; use token with appropriate scope (`repo`, `read:org`). For scale, use GitHub App installation tokens and exponential backoff.
- **Extending to a GitHub App**: Use webhooks for events (e.g. `pull_request`), authenticate with installation token via `POST /app/installations/:id/access_tokens`; same REST/GraphQL calls with that token.
