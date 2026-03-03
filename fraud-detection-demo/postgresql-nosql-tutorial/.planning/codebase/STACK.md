# Technology Stack

**Analysis Date:** 2025-02-25

## Languages

**Primary:** Not yet chosen for tutorial implementation. PROJECT.md specifies PostgreSQL and NoSQL; tutorial content may use SQL plus one or more of: application language (e.g. Python, Node, Go) for drivers and examples.

**Secondary:** N/A.

## Runtime

**Environment:** Not applicable—no runnable application. Future: depends on phase choices (e.g. Node, Python, or Go for sample apps).

**Package Manager:** None. No lockfile or manifest.

## Frameworks

**Core:** None. Stack is defined at project level as PostgreSQL + NoSQL (e.g. MongoDB, DynamoDB, Redis); standard clients and APIs.

**Testing:** None.

**Build/Dev:** None. GSD workflow only; config in `postgresql-nosql-tutorial/config.json`.

## Key Dependencies

**Critical:** None in repo. PROJECT.md and REQUIREMENTS.md will drive dependency selection when phases are defined (PostgreSQL client, NoSQL client(s)).

**Infrastructure:** Intended: PostgreSQL; one or more NoSQL stores (MongoDB, DynamoDB, Redis mentioned as examples).

## Configuration

**Environment:** No `.env` or env docs yet. When labs are added, document required vars (e.g. DB URL, NoSQL endpoint) and keep secrets out of repo.

**Build:** No build config. Only GSD config: `postgresql-nosql-tutorial/config.json` (mode, depth, parallelization, commit_docs, model_profile, workflow).

## Platform Requirements

**Development:** None until phases add code (then: PostgreSQL and chosen NoSQL runtimes/tools).

**Production:** Tutorial/demo only; deployment target TBD per phase.

---

*Stack analysis: 2025-02-25*
