# Codebase Structure

**Analysis Date:** 2025-02-25

## Directory Layout

```
rag-pinecone-tutorial/
├── .planning/              # GSD planning artifacts
│   ├── PROJECT.md          # Project definition, value, constraints, audience, stack
│   ├── STATE.md            # Current phase, plan, progress
│   ├── ROADMAP.md          # Milestones and phases (TBD)
│   ├── REQUIREMENTS.md     # Phase requirements and traceability (TBD)
│   ├── research/           # Optional research outputs
│   │   └── README.md       # Placeholder for RAG/Pinecone research
│   └── codebase/           # Codebase map (this directory)
│       ├── ARCHITECTURE.md
│       ├── STRUCTURE.md
│       ├── CONVENTIONS.md
│       ├── TESTING.md
│       ├── CONCERNS.md
│       ├── STACK.md
│       └── INTEGRATIONS.md
└── config.json             # GSD workflow configuration
```

**Note:** No `src/`, `app/`, package manifests, or test directories exist yet. Layout reflects planning scaffold only.

## Directory Purposes

**rag-pinecone-tutorial/:**
- Purpose: Root for the RAG + Pinecone-style tutorial project.
- Contains: Single config file and `.planning/` tree.
- Key files: `config.json`, `.planning/PROJECT.md`.

**.planning/:**
- Purpose: GSD project state, roadmap, requirements, and optional research.
- Contains: Markdown docs and `research/`, `codebase/` subfolders.
- Key files: `PROJECT.md`, `STATE.md`, `ROADMAP.md`, `REQUIREMENTS.md`.

**.planning/research/:**
- Purpose: Optional research (RAG, Pinecone-style vector stores, embeddings, LLM integration).
- Contains: `README.md` placeholder.
- Key files: `research/README.md`.

**.planning/codebase/:**
- Purpose: Codebase map for planners and executors (where to add code, conventions, concerns).
- Contains: ARCHITECTURE.md, STRUCTURE.md, CONVENTIONS.md, TESTING.md, CONCERNS.md, STACK.md, INTEGRATIONS.md.

## Key File Locations

**Entry points:**
- None (no application). Planning entry: `.planning/PROJECT.md`.

**Configuration:**
- `config.json`: GSD workflow (mode, depth, parallelization, commit_docs, model_profile, workflow flags).

**Core logic:**
- Not present. Future tutorial code will be added per ROADMAP phases (e.g. ingestion, indexing, retrieval, LLM integration).

**Testing:**
- Not present. Test layout to be defined when phases introduce code.

## Naming Conventions

**Files:**
- GSD planning: UPPERCASE.md (PROJECT.md, STATE.md, ROADMAP.md, REQUIREMENTS.md).
- Config: lowercase with extension (`config.json`).
- Research: README.md in `research/`.
- Codebase map: UPPERCASE.md in `.planning/codebase/`.

**Directories:**
- `.planning/`, `research/`, `codebase/` under it; lowercase.

## Where to Add New Code

**New feature (tutorial phase):**
- Primary code: To be defined in ROADMAP and STRUCTURE when first phase adds a codebase (e.g. `src/`, `notebooks/`, or `examples/`).
- Tests: To be defined in TESTING.md once a test strategy exists.

**New component/module:**
- Implementation: Place under whatever root is chosen (e.g. `src/`, `examples/`) per phase plan and STRUCTURE.md update.

**Utilities:**
- Shared helpers: Location to be defined when codebase root exists.

## Special Directories

**.planning/:**
- Purpose: GSD planning and codebase map only; not application source.
- Generated: Partially (STATE/ROADMAP may be updated by GSD).
- Committed: Yes.

**.planning/codebase/:**
- Purpose: Analysis documents for /gsd:plan-phase and /gsd:execute-phase.
- Generated: By map-codebase (GSD codebase mapper).
- Committed: Yes.

---
*Structure analysis: 2025-02-25*
