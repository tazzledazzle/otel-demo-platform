# External Integrations

**Analysis Date:** 2025-02-25

## APIs & External Services

**Databases (intended, not yet integrated):**
- PostgreSQL — Relational store; schema design, queries, hybrid use (e.g. JSONB). No SDK or connection in repo yet.
- NoSQL (e.g. MongoDB, DynamoDB, Redis) — Document/key-value stores; when to use which, hybrid patterns. No client or connection in repo yet.

## Data Storage

**Databases:** PostgreSQL and one or more NoSQL stores are specified in PROJECT.md; no connection config, ORM, or client code present.

**File Storage:** Local filesystem only (planning docs).

**Caching:** None. Redis mentioned as example NoSQL option; not integrated.

## Authentication & Identity

Not applicable. No application or API.

## Monitoring & Observability

None.

## CI/CD & Deployment

**Hosting:** Not defined.
**CI Pipeline:** None.

## Environment Configuration

**Required env vars:** None currently. When labs are added: document DB URLs and NoSQL endpoints; do not commit secrets.

**Secrets location:** No secrets in repo. Use `.env` or similar and exclude from version control when adding labs.

## Webhooks & Callbacks

**Incoming:** None.
**Outgoing:** None.

---

*Integration audit: 2025-02-25*
