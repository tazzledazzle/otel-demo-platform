# External Integrations

**Analysis Date:** 2025-02-25

## APIs & External Services

- None. Tutorial will likely introduce HTTP clients and possibly external APIs in later phases; specific services TBD in ROADMAP.

## Data Storage

**Databases:**
- None. If phases add persistence: Connection and client TBD (e.g. in-memory H2 for tutorial, or Postgres with testcontainers).

**File Storage:**
- Local filesystem only (planning and config files).

**Caching:**
- None.

## Authentication & Identity

**Auth provider:**
- None. Tutorial may add auth in a later phase (e.g. OAuth2, API keys); approach TBD.

## Monitoring & Observability

**Error tracking:**
- None.

**Logs:**
- None. When app exists: SLF4J/Logback or framework default; observability (Micrometer, OpenTelemetry) per PROJECT.md.

## CI/CD & Deployment

**Hosting:**
- Not defined. Tutorial may add Docker/K8s examples.

**CI pipeline:**
- None. Repo is scaffold-only.

## Environment Configuration

**Required env vars:**
- None for current scaffold. Future app: Document in README or phase docs (e.g. port, DB URL).

**Secrets location:**
- No secrets. Keep out of `config.json` and repo.

## Webhooks & Callbacks

**Incoming:** None.
**Outgoing:** None.

---

*Integration audit: 2025-02-25*
