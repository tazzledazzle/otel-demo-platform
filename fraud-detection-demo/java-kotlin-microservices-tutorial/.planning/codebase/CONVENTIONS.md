# Coding Conventions

**Analysis Date:** 2025-02-25

## Naming Patterns

**Files (current):**
- GSD planning: UPPERCASE with `.md` in `.planning/` (e.g. PROJECT.md, ROADMAP.md, REQUIREMENTS.md, STATE.md).
- Config: `config.json` at project root (lowercase).
- Research: `README.md` or descriptive names in `.planning/research/`.

**Files (when adding application code):**
- Use Java/Kotlin norms: PascalCase for type files, lowercase for package dirs; build files per tool (e.g. `build.gradle.kts`, `pom.xml`).

**Functions / Variables / Types:**
- No application code yet. When adding: Kotlin use camelCase for functions/variables, PascalCase for types; Java use camelCase for methods/fields, PascalCase for types.

## Code Style

**Formatting:**
- Markdown: Any consistent style; GSD docs use headers, tables, lists.
- Future Java: Prefer Google Java Style or project-standard formatter (e.g. Spotless).
- Future Kotlin: Prefer official Kotlin style; use ktlint or kotlinter.

**Linting:**
- Not configured. When adding code: Use Checkstyle/Spotless for Java, ktlint/detekt for Kotlin.

## Import Organization

- Not applicable (no source files). When adding: Group stdlib, then third-party, then project; alphabetical within groups; no wildcards in Kotlin/Java.

## Error Handling

- Not applicable. When adding services: Use consistent patterns (e.g. Spring `@ControllerAdvice`, Ktor status pages); avoid empty catch; document expected failures.

## Logging

- Not applicable. When adding: Use SLF4J with Logback or framework default; structured logging for production.

## Comments

**When to comment (planning):**
- PROJECT.md: Clear “What This Is”, “Core Value”, “Context”, “Constraints”.
- ROADMAP/REQUIREMENTS: Tables and traceability; avoid redundant prose.

**JSDoc/TSDoc:** Not applicable. For future Java/Kotlin: Use KDoc/Javadoc for public APIs.

## Function Design

- Not applicable. When adding: Keep functions small; single responsibility; document contract for public API.

## Module Design

**Exports:** Not applicable. GSD docs do not “export” symbols; they are consumed by reference.

**Barrel files:** Not applicable. For multi-module JVM: Prefer explicit module boundaries (Gradle subprojects or Maven modules).

## GSD Artifact Conventions (Implied)

- **PROJECT.md:** Contains “What This Is”, “Core Value”, “Requirements”, “Context”, “Constraints”, “Key Decisions” table; footer `*Initialized by GSD new-project workflow*`.
- **ROADMAP.md:** Contains “Overview”, “Milestones”, “Phases”, “Progress” table; phases TBD after roadmapper.
- **REQUIREMENTS.md:** “Core Value”, “Phase Requirements”, “Traceability”; filled when phases exist.
- **STATE.md:** “Core value”, “Current focus”, “Current Position” (Phase, Plan, Status), “Progress” bar.
- **config.json:** JSON object with `mode`, `depth`, `parallelization`, `commit_docs`, `model_profile`, `workflow` (research, plan_check, verifier). Do not add secrets here.

---

*Convention analysis: 2025-02-25*
