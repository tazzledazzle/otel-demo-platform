# External Integrations

**Analysis Date:** 2025-02-25

## APIs & External Services

**LLM / LangChain:**
- Not integrated. PROJECT.md references “LLM providers (OpenAI, etc.)”; specific providers and SDKs to be chosen with first phase.
- SDK/Client: LangChain + provider SDK (e.g. openai) when code is added.
- Auth: To be via env vars (e.g. OPENAI_API_KEY); never commit.

## Data Storage

**Databases:** None.

**File storage:** Local filesystem only (planning docs).

**Caching:** None.

## Authentication & Identity

**Auth provider:** Not applicable. API keys for LLM providers to be configured via environment.

## Monitoring & Observability

**Error tracking:** None.

**Logs:** None.

## CI/CD & Deployment

**Hosting:** Not defined.

**CI pipeline:** None.

## Environment Configuration

**Required env vars:**
- None currently. When code is added: document provider API keys and any endpoint overrides.

**Secrets location:**
- Do not store in repo. Use `.env` (gitignored) or platform secrets.

## Webhooks & Callbacks

**Incoming:** None.

**Outgoing:** None.

---

*Integration audit: 2025-02-25*
