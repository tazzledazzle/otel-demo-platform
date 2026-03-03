# Phase 1: Foundation — Context

**Gathered:** 2026-02-25
**Status:** Ready for planning

<domain>
## Phase Boundary

Deliver one runnable example each for PostgreSQL and one NoSQL store: run queries/operations against both. Setup (local or cloud) and client usage clear. No hybrid or multi-store workflow in Phase 1; two separate, minimal examples. Engineer-oriented, code-first.

</domain>

<decisions>
## Implementation Decisions

### PostgreSQL example
- Connect, run at least one query (e.g. SELECT or simple CRUD); small schema or no schema.
- Single script or notebook; success = learner runs and sees result.

### NoSQL example
- One store (e.g. MongoDB, Redis, or DynamoDB-style); connect and one or two operations (e.g. insert, get).
- Same runnable unit; clear setup and client.

### Scope
- No hybrid pattern (e.g. "use Postgres for X and NoSQL for Y") in Phase 1; just "here’s Postgres, here’s NoSQL."
- Prerequisites and run steps documented.

### Claude's Discretion
- Which NoSQL store; language and clients; exact query/operation examples.

</decisions>

<specifics>
## Specific Ideas

No specific requirements — open to standard DB tutorial patterns.

</specifics>

<deferred>
## Deferred Ideas

- Hybrid patterns, when to use which, production patterns — later phases.

</deferred>

---
*Phase: 01-foundation*
*Context gathered: 2026-02-25*
