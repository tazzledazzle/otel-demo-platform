# Phase 1: Foundation — Context

**Gathered:** 2026-02-25
**Status:** Ready for planning

<domain>
## Phase Boundary

Deliver one runnable API: either REST or GraphQL (single choice for Phase 1), with a minimal schema and one or two operations. Framework and language TBD by research/planner. Engineer-oriented, code-first.

</domain>

<decisions>
## Implementation Decisions

### API type
- Either REST or GraphQL for Phase 1 (not both); choice TBD by research/planner based on tutorial focus.
- One or two operations (e.g. GET resource, or query + mutation).

### Run experience
- Single-command or minimal-step run; learner can call the API (curl, browser, or simple client) and see a response.
- Success = request in, response back; no auth or versioning in Phase 1.

### Format
- Code-first; minimal theory. Prerequisites and project layout clear.

### Claude's Discretion
- REST vs GraphQL; framework and language; example resource/query shape.

</decisions>

<specifics>
## Specific Ideas

No specific requirements — open to standard API tutorial patterns.

</specifics>

<deferred>
## Deferred Ideas

- The other API style (GraphQL if REST first, or vice versa), auth, versioning — later phases.

</deferred>

---
*Phase: 01-foundation*
*Context gathered: 2026-02-25*
