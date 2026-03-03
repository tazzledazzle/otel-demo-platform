# Phase 1: Foundation — Context

**Gathered:** 2026-02-25
**Status:** Ready for planning

<domain>
## Phase Boundary

Deliver one runnable example: connect to Redis and perform basic operations (e.g. set/get, maybe one other structure). Client and connection setup clear; no pub/sub or production patterns in Phase 1. Engineer-oriented, code-first.

</domain>

<decisions>
## Implementation Decisions

### Operations covered
- At least: connect, set, get. Optionally one more (e.g. list, hash, or TTL).
- Single runnable script or small app; success = learner runs and sees read/write work.

### Redis instance
- Local Redis or cloud; connection (URL/env) documented. No clustering in Phase 1.

### Language and client
- Language TBD (e.g. Python, Node, or Java); standard client library.
- Prerequisites stated (Redis running, client install).

### Claude's Discretion
- Exact client and language; which extra data structure to show; script vs notebook.

</decisions>

<specifics>
## Specific Ideas

No specific requirements — open to standard Redis client patterns.

</specifics>

<deferred>
## Deferred Ideas

- Pub/sub, sessions, rate limiting, production patterns — later phases.

</deferred>

---
*Phase: 01-foundation*
*Context gathered: 2026-02-25*
