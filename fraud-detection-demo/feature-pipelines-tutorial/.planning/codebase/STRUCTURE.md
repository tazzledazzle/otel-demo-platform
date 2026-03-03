# Codebase Structure

**Analysis Date:** 2025-02-25

## Directory Layout

```
feature-pipelines-tutorial/
├── .planning/              # GSD planning and state
│   ├── PROJECT.md          # Scope, value, constraints, decisions
│   ├── REQUIREMENTS.md     # Phase requirements and traceability
│   ├── ROADMAP.md          # Milestones, phases, progress table
│   ├── STATE.md            # Current phase/plan and session continuity
│   ├── research/           # Optional research outputs
│   │   └── README.md       # Placeholder for feature-pipeline research
│   └── codebase/           # Codebase analysis (this directory)
│       ├── ARCHITECTURE.md
│       ├── STRUCTURE.md
│       ├── CONVENTIONS.md
│       ├── TESTING.md
│       └── CONCERNS.md
└── config.json             # GSD workflow configuration
```

**Note:** No `src/`, `app/`, or other application directories exist. The codebase is minimal (tutorial scaffold only).

## Directory Purposes

**.planning:**
- Purpose: GSD project state, roadmap, requirements, and optional research.
- Contains: Markdown docs, research placeholder.
- Key files: `PROJECT.md`, `ROADMAP.md`, `STATE.md`, `REQUIREMENTS.md`.

**.planning/research:**
- Purpose: Optional research on feature pipelines (e.g. feature stores, tooling, patterns).
- Contains: `README.md` placeholder.
- Key files: `research/README.md`.

**.planning/codebase:**
- Purpose: Codebase analysis produced by map-codebase; consumed by plan-phase and execute-phase.
- Contains: ARCHITECTURE.md, STRUCTURE.md, CONVENTIONS.md, TESTING.md, CONCERNS.md.

**Project root (feature-pipelines-tutorial):**
- Purpose: Tutorial root; only `config.json` and `.planning/` at present.
- Contains: No application source; config and planning only.

## Key File Locations

**Entry Points:** None.

**Configuration:**
- `feature-pipelines-tutorial/config.json`: GSD workflow (mode, depth, parallelization, commit_docs, model_profile, workflow flags).

**Core Logic:** None (scaffold only).

**Planning:**
- `feature-pipelines-tutorial/.planning/PROJECT.md`: Project definition.
- `feature-pipelines-tutorial/.planning/ROADMAP.md`: Phases and progress.
- `feature-pipelines-tutorial/.planning/STATE.md`: Current position.
- `feature-pipelines-tutorial/.planning/REQUIREMENTS.md`: Requirements and traceability.

**Testing:** None.

## Naming Conventions

**Files:**
- Planning docs: UPPERCASE.md (PROJECT.md, REQUIREMENTS.md, ROADMAP.md, STATE.md).
- Config: lowercase with extension (`config.json`).
- Research: README.md in `research/`.

**Directories:**
- `.planning/` — GSD planning; subdirs `research/`, `codebase/`.
- No convention yet for future app code (e.g. `src/`, `lib/`, or phase-named dirs).

## Where to Add New Code

**New feature / phase implementation:**
- Primary code: To be defined in phase plans (e.g. `src/`, or a phase-specific directory under the tutorial root).
- Tests: To be defined with the chosen structure (e.g. `tests/`, or co-located).

**New planning artifact:**
- Under `feature-pipelines-tutorial/.planning/` (e.g. phase plans, VERIFICATION.md).

**Research:**
- Under `feature-pipelines-tutorial/.planning/research/`.

## Special Directories

**.planning:**
- Purpose: GSD state and planning only; not generated at runtime.
- Generated: No.
- Committed: Yes (planning is versioned).

**research:**
- Purpose: Optional research outputs; placeholder only.
- Generated: No.
- Committed: Yes.

---

*Structure analysis: 2025-02-25*
