# Codebase Structure

**Analysis Date:** 2025-02-25

## Directory Layout

```
java-kotlin-microservices-tutorial/
├── .planning/                 # GSD planning and state
│   ├── PROJECT.md             # What the tutorial is, audience, stack, constraints
│   ├── ROADMAP.md             # Milestones and phases (TBD)
│   ├── REQUIREMENTS.md        # Phase requirements and traceability (TBD)
│   ├── STATE.md               # Current phase, plan, status, progress
│   ├── research/              # Optional research outputs
│   │   └── README.md          # Placeholder for Java/Kotlin microservices research
│   └── codebase/              # Codebase map (this document set)
│       ├── ARCHITECTURE.md
│       ├── STRUCTURE.md
│       ├── CONVENTIONS.md
│       ├── TESTING.md
│       └── CONCERNS.md
└── config.json                # GSD workflow configuration
```

No `src/`, build files, or application code present.

## Directory Purposes

**java-kotlin-microservices-tutorial/:**
- Purpose: Root of the tutorial scaffold; contains only planning and GSD config.
- Contains: `config.json`, `.planning/`.
- Key files: `config.json`, `.planning/PROJECT.md`, `.planning/ROADMAP.md`, `.planning/STATE.md`.

**.planning/:**
- Purpose: GSD project definition, roadmap, requirements, state, and optional research.
- Contains: PROJECT.md, ROADMAP.md, REQUIREMENTS.md, STATE.md, `research/`, `codebase/`.
- Key files: All listed above; `codebase/` holds this map.

**.planning/research/:**
- Purpose: Optional research (frameworks, patterns, tooling) for Java/Kotlin microservices.
- Contains: README.md placeholder.
- Generated: No. Committed: Yes.

**.planning/codebase/:**
- Purpose: Codebase analysis for GSD (architecture, structure, conventions, testing, concerns).
- Contains: ARCHITECTURE.md, STRUCTURE.md, CONVENTIONS.md, TESTING.md, CONCERNS.md.
- Generated: By GSD map-codebase. Committed: Per workflow (commit_docs in config.json).

## Key File Locations

**Entry points:**
- `java-kotlin-microservices-tutorial/.planning/PROJECT.md`: Tutorial scope, audience, stack (Java/Kotlin, Spring Boot/Ktor).
- `java-kotlin-microservices-tutorial/config.json`: GSD mode, depth, parallelization, workflow flags.

**Configuration:**
- `java-kotlin-microservices-tutorial/config.json`: Only config file at root.

**Core logic:**
- None. Application code to be added in future phases.

**Testing:**
- None. Test layout TBD with first implementation phase.

## Naming Conventions

**Files:**
- GSD planning: UPPERCASE markdown in `.planning/` (PROJECT.md, ROADMAP.md, REQUIREMENTS.md, STATE.md).
- Config: lowercase `config.json` at project root.
- Research: `research/README.md` or other research outputs in `research/`.

**Directories:**
- `.planning/`: GSD planning root; subdirs `research/`, `codebase/`.
- No `src/` or service-named dirs yet.

## Where to Add New Code

**New feature (when phases exist):**
- Primary code: Under a new application layout (e.g. `src/` or `services/<name>/`); follow phase plan.
- Tests: Alongside or in `src/test/` (or per-module test dir) per TESTING.md once defined.

**New component/module:**
- Implementation: To be defined by ROADMAP phases (e.g. one directory per microservice or shared lib).

**Utilities:**
- Shared helpers: To be placed in a common module or package when application structure is created.

**Planning/research:**
- Research outputs: `.planning/research/`.
- New GSD docs: `.planning/` (keep UPPERCASE naming for core docs).

## Special Directories

**.planning/:**
- Purpose: GSD planning and codebase map only.
- Generated: Partially (codebase/* by map-codebase; STATE/ROADMAP updated by workflows).
- Committed: Yes (and commit_docs in config.json controls whether docs are committed by GSD).

**research/:**
- Purpose: Optional pre-phase research.
- Generated: No.
- Committed: Yes.

---

*Structure analysis: 2025-02-25*
