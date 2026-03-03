# External Integrations

**Analysis Date:** 2025-02-25

## APIs & External Services

- **None.** No application code or external API calls. Tutorial may later reference cloud or cluster APIs (e.g. for deployment); document in this section when added.

## Data Storage

**Databases:**
- None. Tutorial will use in-memory or local sample data unless a phase adds external storage.

**File Storage:**
- Local filesystem only (e.g. sample data files). No object store or remote storage configured.

**Caching:**
- None.

## Authentication & Identity

- Not applicable for tutorial scope. Cluster or cloud auth to be documented here if a phase adds it.

## Monitoring & Observability

- None. Spark UI may be referenced in lessons; no custom monitoring.

## CI/CD & Deployment

**Hosting:**
- Not defined. Possible targets from PROJECT.md: standalone, YARN, or managed Spark.

**CI Pipeline:**
- None.

## Environment Configuration

**Required env vars:**
- None currently. Future: e.g. `SPARK_MASTER`, Java/Python paths if documented in a phase.

**Secrets location:**
- No secrets. Do not commit credentials; use env or secrets manager when needed.

## Webhooks & Callbacks

**Incoming:** None.  
**Outgoing:** None.

---

*Integration audit: 2025-02-25*
