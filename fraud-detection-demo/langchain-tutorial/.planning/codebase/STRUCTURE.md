# Codebase Structure

**Analysis Date:** 2025-02-25

## Directory Layout

```
langchain-tutorial/
├── .planning/              # GSD planning artifacts
│   ├── PROJECT.md          # Project definition, value, constraints
│   ├── STATE.md            # Current phase, plan, progress
│   ├── ROADMAP.md          # Milestones and phases (TBD)
│   ├── REQUIREMENTS.md     # Phase requirements and traceability (TBD)
│   ├── research/           # Optional research outputs
│   │   └── README.md       # Placeholder for LangChain research
│   └── codebase/           # Codebase map (this directory)
│       ├── ARCHITECTURE.md
│       ├── STRUCTURE.md
│       ├── CONVENTIONS.md
│       ├── TESTING.md
│       └── CONCERNS.md
└── config.json             # GSD workflow configuration
```

**Note:** No `src/`, `app/`, package manifests, or test directories exist yet. Layout reflects planning scaffold only.

## Directory Purposes

**langchain-tutorial/:**
- Purpose: Root for the LangChain tutorial project.
- Contains: Single config file and `.planning/` tree.
- Key files: `config.json`, `.planning/PROJECT.md`.

**.planning/:**
- Purpose: GSD project state, roadmap, requirements, and optional research.
- Contains: Markdown docs and `research/` subfolder.
- Key files: `PROJECT.md`, `STATE.md`, `ROADMAP.md`, `REQUIREMENTS.md`.

**.planning/research/:**
- Purpose: Optional research (ecosystem, patterns, tooling) for LangChain.
- Contains: `README.md` placeholder.
- Key files: `research/README.md`.

**.planning/codebase/:**
- Purpose: Codebase map for planners and executors (where to add code, conventions, concerns).
- Contains: ARCHITECTURE.md, STRUCTURE.md, CONVENTIONS.md, TESTING.md, CONCERNS.md.

## Key File Locations

**Entry points:**
- None (no application). Planning entry: `.planning/PROJECT.md`.

**Configuration:**
- `config.json`: GSD workflow (mode, depth, parallelization, commit_docs, model_profile, workflow flags).

**Core logic:**
- Not present. Future tutorial code will be added per ROADMAP phases.

**Testing:**
- Not present. Test layout to be defined when phases introduce code.

## Naming Conventions

**Files:**
- GSD planning: UPPERCASE.md (PROJECT.md, STATE.md, ROADMAP.md, REQUIREMENTS.md).
- Config: lowercase with extension (`config.json`).
- Research: README.md in `research/`.

**Directories:**
- `.planning/` and `research/`, `codebase/` under it; lowercase.

## Where to Add New Code

**New feature (tutorial phase):**
- Primary code: To be defined in ROADMAP/STRUCTURE when first phase adds a codebase (e.g. `src/` or `notebooks/`).
- Tests: To be defined in TESTING.md once a test strategy exists.

**New component/module:**
- Implementation: Place under whatever root is chosen (e.g. `src/`, `examples/`) per phase plan.

**Utilities:**
- Shared helpers: To be placed in a dedicated module or `utils/` once structure is established.

## Special Directories

**.planning/:**
- Purpose: GSD artifacts only; not application source.
- Generated: Partially (STATE/ROADMAP/REQUIREMENTS updated by GSD; PROJECT and research hand-edited).
- Committed: Yes.

**research/:**
- Purpose: Optional research outputs for roadmap/requirements.
- Generated: No; populated by research workflows or manually.
- Committed: Yes.

---

*Structure analysis: 2025-02-25*
