# Codebase Structure

**Analysis Date:** 2025-02-25

## Directory Layout

```
redis-tutorial/
├── .planning/              # GSD planning artifacts
│   ├── codebase/           # Codebase map (this document set)
│   ├── research/           # Optional research (Redis patterns, clients, deployment)
│   │   └── README.md
│   ├── PROJECT.md          # Project definition, value, audience, stack, constraints
│   ├── REQUIREMENTS.md     # Phase requirements (placeholder)
│   ├── ROADMAP.md          # Milestones, phases, progress table
│   └── STATE.md            # Current phase, plan, status, progress %
└── config.json             # GSD workflow configuration
```

No `src/`, `examples/`, `tests/`, or package manifests exist yet.

## Directory Purposes

**.planning:**
- Purpose: GSD project metadata and planning.
- Contains: Markdown docs and optional research.
- Key files: `PROJECT.md`, `ROADMAP.md`, `STATE.md`, `REQUIREMENTS.md`.

**.planning/codebase:**
- Purpose: Codebase analysis written by map-codebase (ARCHITECTURE, STRUCTURE, CONVENTIONS, TESTING, CONCERNS, optionally STACK, INTEGRATIONS).
- Contains: `.md` analysis documents only.

**.planning/research:**
- Purpose: Optional research (e.g. Redis patterns, client libs, deployment); placeholder README only.
- Contains: `README.md`.

**Project root (redis-tutorial/):**
- Purpose: Tutorial root; only `config.json` and `.planning/` present. Application and examples to be added per roadmap.

## Key File Locations

**Entry points:**
- `config.json`: GSD workflow config (mode, depth, parallelization, commit_docs, model_profile, workflow flags).

**Configuration:**
- `config.json`: Only config file in repo.

**Core logic:**
- Not present. Future: place under a chosen layout (e.g. `src/`, `examples/`, or phase-named dirs).

**Planning:**
- `.planning/PROJECT.md`: What the tutorial is, audience, stack, constraints.
- `.planning/ROADMAP.md`: Phases and progress.
- `.planning/STATE.md`: Current focus and progress.
- `.planning/REQUIREMENTS.md`: Phase requirements (to be filled).

**Testing:**
- No test directory or files yet.

## Naming Conventions

**Files:**
- Planning: UPPERCASE.md for main artifacts (PROJECT.md, ROADMAP.md, STATE.md, REQUIREMENTS.md).
- Config: lowercase `config.json`.
- Research: README.md in `research/`.

**Directories:**
- `.planning/` and subdirs lowercase; `codebase/` and `research/` under `.planning/`.

**Future application code:** Not defined; follow phase plans and CONVENTIONS.md once established.

## Where to Add New Code

**New feature / phase implementation:**
- Primary code: To be defined in ROADMAP/phase plans (e.g. `src/`, `examples/`, or `phase-N-name/`).
- Tests: To be defined (e.g. `tests/` or co-located).

**New planning artifact:**
- GSD-related: `.planning/` or subdirs as per GSD conventions.
- Research: `.planning/research/`.

**Utilities / shared helpers:**
- Not applicable until a code layout exists.

## Special Directories

**.planning:**
- Purpose: GSD planning and codebase maps.
- Generated: Partially (codebase/* by map-codebase; others by GSD workflows).
- Committed: Yes.

**.planning/codebase:**
- Purpose: Codebase map output.
- Generated: By map-codebase workflow.
- Committed: Yes.

---

*Structure analysis: 2025-02-25*
