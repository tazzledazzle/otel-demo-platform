# Technology Stack

**Analysis Date:** 2025-02-25

## Languages

**Primary (intended):**
- Java or Kotlin — Tutorial scope per `.planning/PROJECT.md`; exact choice TBD per phase or learner path.

**Secondary:**
- None. Markdown and JSON only in current scaffold.

## Runtime

**Environment:**
- JVM (version TBD when build is introduced; recommend Java 17+ or Kotlin 1.9+).

**Package manager / build:**
- Not present. When added: Gradle (recommended for Kotlin) or Maven; lockfile per tool (e.g. `gradle.lockfile`, `pom.xml` with pinned plugins).

## Frameworks

**Core (intended):**
- Spring Boot or Ktor — Per PROJECT.md for microservices (APIs, resilience, observability, deployment).

**Testing:**
- JUnit 5 (JVM); optionally Kotest for Kotlin. Not yet configured.

**Build/Dev:**
- GSD uses planning docs and `config.json` only; no build or dev server in repo yet.

## Key Dependencies

**Critical:**
- None. Future: Spring Boot BOM or Ktor version; logging (SLF4J/Logback); HTTP client and server as chosen.

**Infrastructure:**
- None. Future: Observability (Micrometer, OpenTelemetry) and deployment (Docker, K8s) as per tutorial phases.

## Configuration

**Environment:**
- No app env yet. `config.json` is GSD-only (mode, depth, parallelization, workflow flags). Do not store app secrets in `config.json`.

**Build:**
- No build config files yet. When added: `build.gradle.kts` or `pom.xml`, optionally `settings.gradle.kts`.

## Platform Requirements

**Development:**
- Git; editor for Markdown/JSON; when code exists: JDK 17+ (or as specified), Gradle or Maven.

**Production:**
- Deployment target TBD by roadmap (e.g. local, Docker, Kubernetes for tutorial).

---

*Stack analysis: 2025-02-25*
