# Codebase Structure

**Analysis Date:** 2025-02-25

## Directory Layout

```
spark-tutorial/
├── .planning/              # GSD planning and project metadata
│   ├── PROJECT.md          # Project definition, audience, stack, constraints
│   ├── ROADMAP.md          # Milestones and phases (placeholder)
│   ├── REQUIREMENTS.md     # Phase requirements and traceability (placeholder)
│   ├── STATE.md            # Current phase, plan, progress
│   ├── codebase/           # Codebase map (this document and peers)
│   └── research/           # Optional research artifacts
│       └── README.md       # Placeholder for Spark research
└── config.json             # GSD workflow configuration
```

## Directory Purposes

**spark-tutorial/:**
- Purpose: Root of the Spark tutorial scaffold.
- Contains: Single config file and `.planning/` tree. No `src/`, `notebooks/`, or app code yet.

**.planning/:**
- Purpose: GSD project metadata and phase/requirement tracking.
- Contains: PROJECT.md, ROADMAP.md, REQUIREMENTS.md, STATE.md, `codebase/`, `research/`.
- Key files: `spark-tutorial/.planning/PROJECT.md`, `spark-tutorial/.planning/ROADMAP.md`, `spark-tutorial/.planning/STATE.md`.

**.planning/codebase/:**
- Purpose: Codebase analysis for planners and executors (ARCHITECTURE, STRUCTURE, CONVENTIONS, TESTING, CONCERNS).
- Contains: Markdown docs only. No generated code.

**.planning/research/:**
- Purpose: Optional research on Spark APIs, deployment, best practices.
- Contains: `README.md` placeholder only.

## Key File Locations

**Entry Points:**
- None. No application entry points.

**Configuration:**
- `spark-tutorial/config.json`: GSD workflow (mode, depth, parallelization, commit_docs, model_profile, workflow flags).

**Core Logic:**
- None. Tutorial content and sample code to be added per roadmap.

**Planning:**
- `spark-tutorial/.planning/PROJECT.md`: What the tutorial is, audience, stack, constraints.
- `spark-tutorial/.planning/ROADMAP.md`: Phases and progress table.
- `spark-tutorial/.planning/REQUIREMENTS.md`: Phase requirements and traceability.
- `spark-tutorial/.planning/STATE.md`: Current phase and progress.

**Testing:**
- No test directory or files yet.

## Naming Conventions

**Files:**
- Planning docs: UPPERCASE.md (PROJECT.md, ROADMAP.md, REQUIREMENTS.md, STATE.md).
- Config: lowercase with extension (`config.json`).
- Research: README.md in `research/`.

**Directories:**
- `.planning/` — GSD planning; `codebase/` and `research/` are subdirectories under it.

## Where to Add New Code

**New tutorial phase / lesson:**
- Content: To be defined by ROADMAP (e.g. `notebooks/`, `scripts/`, or `lessons/`).
- Planning: Update `spark-tutorial/.planning/ROADMAP.md`, `REQUIREMENTS.md`, `STATE.md`.

**New Spark examples:**
- Location: TBD (e.g. `spark-tutorial/examples/` or per-phase directories).

**Utilities:**
- Shared helpers: TBD once structure is chosen.

## Special Directories

**.planning/:**
- Purpose: GSD artifacts; not application source.
- Generated: Partially (STATE.md, ROADMAP progress updated by workflow).
- Committed: Yes.

**codebase/:**
- Purpose: Codebase map output; not application source.
- Generated: By map-codebase / codebase mapper.
- Committed: Yes.

---

*Structure analysis: 2025-02-25*
