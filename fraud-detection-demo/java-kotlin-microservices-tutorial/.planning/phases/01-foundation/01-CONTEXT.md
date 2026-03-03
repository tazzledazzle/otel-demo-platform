# Phase 1: Foundation — Context

**Gathered:** 2026-02-25
**Status:** Ready for planning

<domain>
## Phase Boundary

Deliver one runnable JVM service (Java or Kotlin) with a single HTTP endpoint. Build and run steps clear; no persistence, resilience, or observability yet. Framework (Spring Boot, Ktor, or similar) TBD by research/planner.

</domain>

<decisions>
## Implementation Decisions

### Service shape
- One HTTP endpoint (e.g. GET /health or GET /api/example); returns simple response.
- No database or external calls in Phase 1.

### Language and framework
- Java or Kotlin (single choice for the tutorial); framework TBD (Spring Boot, Ktor, or other).
- Engineer-oriented: minimal boilerplate, clear project layout.

### Run experience
- Single-command or minimal-step build and run (e.g. `./gradlew run` or `mvn spring-boot:run`).
- Success = learner runs the service and gets a response (e.g. curl or browser).

### Claude's Discretion
- Exact framework and language; endpoint path and response body; build tool (Maven vs Gradle).

</decisions>

<specifics>
## Specific Ideas

No specific requirements — open to standard JVM microservice starters.

</specifics>

<deferred>
## Deferred Ideas

- Persistence, resilience, observability, multi-service — later phases.

</deferred>

---
*Phase: 01-foundation*
*Context gathered: 2026-02-25*
