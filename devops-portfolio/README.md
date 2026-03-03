---
name: DevOps Portfolio Project Suite
overview: "A single monorepo containing four showcase areas: GitHub Actions CI with merge-queue patterns, a minimal REAPI-compatible remote execution service, Nix + Docker for reproducible builds and images at scale, and a CLI that automates GitHub workflows and API usage."
todos: []
isProject: false
---

# DevOps Portfolio Project Suite

A **monorepo** with four distinct but complementary projects that demonstrate CI orchestration, remote build execution, Nix/Docker at scale, and CLI + GitHub automation. Each area lives in its own directory with a clear README and runnable artifacts.

---

## 1. Repository layout

```
devops-portfolio/
├── .github/
│   └── workflows/          # CI orchestration (this repo’s own CI)
├── ci/                     # CI patterns & merge queue docs
├── remote-exec/            # REAPI-compatible service + client demo
├── nix-docker/             # Nix flake + Docker images at scale
├── cli/                    # CLI + GitHub API automation
├── docs/                   # Cross-cutting architecture & “at scale” notes
├── docker-compose.yml      # Optional: run remote-exec + cache locally
└── README.md               # Suite overview and how to run each part
```

---

## 2. CI orchestration and merge queue (Buildkite/Jenkins/GitHub Actions)

**Goal:** Show experience with CI orchestration and merge queue management at scale.

**Deliverables:**

- `**.github/workflows/**` (used as this repo’s real CI):
  - **Build matrix**: multiple OS (ubuntu, macos) and/or runtimes (e.g. Go versions).
  - **Dependent jobs**: build → test → optional deploy; use `needs` and status checks.
  - **Merge-queue–friendly flow**: required status checks, optional “merge queue” workflow that runs full matrix on a temporary merge commit (or document how you’d do it with GitHub’s merge queue / Branch Protection).
  - **Caching**: actions/cache for dependencies; optional Nix store or Docker layer cache.
  - **Artifacts**: upload build outputs and test results; optional report (e.g. JUnit).
- `**ci/` directory:**
  - **README**: explain the workflow design, merge queue semantics, and how the same patterns map to Buildkite (pipeline YAML) and Jenkins (Jenkinsfile).
  - **Optional**: example `buildkite.yml` or `Jenkinsfile` snippets that implement the same logical pipeline (build → test → gate) so you can say “same flow, different orchestrator.”

**Key files:** `[.github/workflows/build.yml](.github/workflows/build.yml)`, `[.github/workflows/merge-queue.yml](.github/workflows/merge-queue.yml)` (or one workflow with a merge-queue job), [ci/README.md](ci/README.md).

---

## 3. Remote build execution (Bazel REAPI / BuildBarn-style)

**Goal:** Show you understand the Remote Execution API (REAPI) and can build or operate such a system.

**Deliverables:**

- `**remote-exec/**`:
  - **REAPI-compatible server** (small but spec-compliant):
    - Implement **Execution**, **ActionCache**, and **CAS** (Content-Addressable Storage) gRPC services.
    - Backend: in-memory or local disk (e.g. a directory per digest); no need for Redis/BuildBarn in the demo.
    - Accept `ExecuteRequest`, look up/blob CAS, run the action (e.g. in a local sandbox or container), write results to CAS and ActionCache.
  - **Client / integration**:
    - Either a **minimal custom client** (e.g. Go) that runs one `Execute` request and shows round-trip, or
    - **Bazel** configured to use this backend as `remote_executor` + `remote_cache` so “bazel build //...” hits your server.
  - **README**: short REAPI concepts (CAS, ActionCache, Execute), link to [official REAPI spec](https://github.com/bazelbuild/remote-apis), and how BuildBarn/BuildBuddy fit in.

**Tech:** Go or Python; gRPC and the [remote-apis](https://github.com/bazelbuild/remote-apis) proto definitions. Keep the server single-binary and runnable with one command.

**Key files:** [remote-exec/server/main.go](remote-exec/server/main.go) (or equivalent), [remote-exec/client/](remote-exec/client/) or [remote-exec/.bazelrc](remote-exec/.bazelrc) + example target, [remote-exec/README.md](remote-exec/README.md).

---

## 4. Nix and Docker at scale

**Goal:** Show experience with Nix/NixOS, Docker, and managing large image/package sets.

**Deliverables:**

- **Nix:**
  - `**nix-docker/flake.nix**`: 
    - Dev shell with project tooling (e.g. Go, Node, Bazel if used).
    - One or more **packages** (e.g. the CLI from `cli/`, or a small service).
    - Optional: **multiple variants** (e.g. same app built with different dependency sets or flags) to illustrate “many derivations” and caching.
  - `**nix-docker/pkgs/` or inline derivations**: example of importing nixpkgs and building a small set of artifacts; document how this scales (many inputs, CI cache of store paths).
- **Docker:**
  - **Multi-stage Dockerfiles**: build stage (Nix or language toolchain) → minimal runtime image.
  - **Optional:** image built **from Nix** using `dockerTools.buildImage` (or `streamLayeredImage`) to show Nix → Docker integration.
  - **“Large set” angle:** script or Make target that builds **multiple images** (e.g. one per service or per variant) and optionally pushes to a registry; document tagging and layer reuse.
- **README:** when to use Nix vs Docker, how you’d manage a large set of images/packages (caching, layers, registries, Nix store paths in CI).

**Key files:** [nix-docker/flake.nix](nix-docker/flake.nix), [nix-docker/Dockerfile](nix-docker/Dockerfile), [nix-docker/scripts/build-images.sh](nix-docker/scripts/build-images.sh) (optional), [nix-docker/README.md](nix-docker/README.md).

---

## 5. CLI and GitHub API automation

**Goal:** Show building CLI tools and GitHub API/automation workflows.

**Deliverables:**

- `**cli/**` – developer-facing CLI (e.g. `portfolio` or `devops-cli`):
  - **Commands (examples):**
    - `pr status [number]`: fetch PR, show status, checks, mergeable state (GitHub REST or GraphQL).
    - `checks run` or `workflow trigger`: trigger a workflow dispatch or re-run checks.
    - `release draft`: create a draft release, upload assets (optional).
    - Optional: `merge-queue status` if you model a queue in this repo or in docs.
  - **Auth:** support `GITHUB_TOKEN` or `GH_TOKEN`; optional `--token` or config file for flexibility.
  - **Output:** human-readable (table or list) and optional JSON for scripting.
- **GitHub automation:**
  - **Workflow(s)** in `.github/workflows/` that call the CLI (e.g. on `workflow_dispatch` or on PR label) to demonstrate “Actions + CLI.”
  - Short doc in `cli/README.md`: which GitHub APIs are used (REST/GraphQL), rate limits, and how you’d extend to a GitHub App (webhooks, installation token).

**Tech:** Go (cobra/urfave) or TypeScript/Node (commander/oclif); `octokit` or `go-github` for API.

**Key files:** [cli/main.go](cli/main.go) or [cli/src/index.ts](cli/src/index.ts), [cli/README.md](cli/README.md), [.github/workflows/cli-demo.yml](.github/workflows/cli-demo.yml).

---

## 6. Documentation and “at scale” narrative

- `**README.md` (root):** one-paragraph description of each of the four areas, how to run them (e.g. `nix develop`, `docker compose up`, `go run ./cli`, Bazel pointing at local REAPI server), and links to each sub-README.
- `**docs/architecture.md`:** optional high-level diagram (e.g. Mermaid) showing: developer → CLI / Git push → GitHub Actions → optional remote-exec and Docker/Nix builds; where merge queue and caches sit.
- `**docs/at-scale.md`:** short notes on what you’d change for “at scale”: distributed cache, persistent REAPI backends (BuildBarn/BuildBuddy), Nix binary cache, image registry and layer strategy, merge queue with many concurrent PRs, and GitHub API usage (tokens, retries, webhooks).

---

## 7. Implementation order and dependencies


| Step | What                                                              | Depends on |
| ---- | ----------------------------------------------------------------- | ---------- |
| 1    | Nix flake + dev shell + one package                               | —          |
| 2    | CLI skeleton + one command (e.g. `pr status`)                     | —          |
| 3    | GitHub Actions: build + test (for this repo), cache               | 1, 2       |
| 4    | REAPI server (CAS + AC + Execute) + minimal client or Bazel       | 1          |
| 5    | Docker multi-stage for CLI or server; optional Nix-built image    | 1          |
| 6    | Merge-queue workflow or doc + optional Buildkite/Jenkins snippets | 3          |
| 7    | Extra CLI commands + workflow that uses CLI                       | 2, 3       |
| 8    | `docs/` and root README                                           | All        |


---

## 8. Tech stack summary


| Area        | Suggested stack                                               |
| ----------- | ------------------------------------------------------------- |
| CI          | GitHub Actions (primary); optional Buildkite/Jenkins examples |
| Remote exec | Go or Python; gRPC; bazelbuild/remote-apis protos             |
| Nix/Docker  | Nix flake, nixpkgs; Docker multi-stage, optional dockerTools  |
| CLI         | Go (cobra) or TypeScript (Node); GitHub REST/GraphQL          |


Use a **single language for CLI + REAPI server** (e.g. Go) to reduce context-switching unless you specifically want to show polyglot (e.g. Go CLI + Python REAPI).

---

## 9. What this demonstrates to reviewers

- **CI:** Real workflows with matrix, dependencies, caching, and merge-queue-aware design; ability to translate to other orchestrators.
- **Remote execution:** Understanding of REAPI (CAS, ActionCache, Execute) and a runnable implementation.
- **Nix/Docker:** Reproducible builds, dev shells, and multi-image/package workflows with a “large set” narrative.
- **CLI + GitHub:** Concrete tooling and automation using GitHub API and Actions.

You can host the monorepo on GitHub and link it as a “DevOps / platform engineering portfolio suite” with each sub-README serving as a short write-up for that topic.