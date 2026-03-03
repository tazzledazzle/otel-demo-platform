# External Integrations

**Analysis Date:** 2025-02-25

## APIs & External Services

**Redis:**
- Redis (standalone or cluster) — target backend for all tutorial content (data structures, caching, pub/sub, sessions, rate limiting, real-time).
- SDK/Client: To be chosen per phase (e.g. redis-py, Jedis).
- Auth: Typically REDIS_PASSWORD or equivalent; not yet documented in repo.

No other external APIs.

## Data Storage

**Databases:**
- Redis only. Connection: to be configured via env (e.g. REDIS_URL or REDIS_HOST/PORT/PASSWORD).
- Client: Whatever the phase specifies (e.g. redis-py, Jedis).

**File Storage:**
- Local filesystem only (planning artifacts and future example code).

**Caching:**
- Redis is the cache/store taught in the tutorial; no separate cache layer.

## Authentication & Identity

**Auth Provider:**
- Not applicable. Redis AUTH (password) when required; no user identity in tutorial scope.

## Monitoring & Observability

**Error tracking:** None.
**Logs:** Not defined. Tutorial code can use print or minimal logging.

## CI/CD & Deployment

**Hosting:** Not applicable; tutorial repo, not a deployed service.
**CI pipeline:** Not detected. Optional: add CI to run tests/examples against Redis when code exists.

## Environment Configuration

**Required env vars (future):**
- Redis connection (e.g. REDIS_URL or REDIS_HOST, REDIS_PORT, REDIS_PASSWORD).

**Secrets location:**
- Do not commit secrets. Use .env (gitignored) or CI secrets when needed.

## Webhooks & Callbacks

**Incoming:** None.
**Outgoing:** None. Pub/sub is Redis-internal.

---

*Integration audit: 2025-02-25*
