# External Integrations

**Analysis Date:** 2025-02-25

## APIs & External Services

**Vector store (planned):**
- Pinecone-style vector DB — index and query embeddings for RAG retrieval.
- SDK/Client: To be chosen (e.g. pinecone-client, or compatible API).
- Auth: To be documented (e.g. API key env var).

**Embeddings (planned):**
- Provider TBD (e.g. OpenAI, Cohere, or local model) for document and query embeddings.
- Auth: API key or similar; env-based.

**LLM (planned):**
- Provider for question-answering and search completion.
- Auth: API key; env-based.

## Data Storage

**Databases:**
- Vector index only (Pinecone-style). No relational DB implied by PROJECT.md.

**File storage:**
- Tutorial may use local files or sample docs for ingestion; no external object store specified yet.

**Caching:**
- None specified.

## Authentication & Identity

**Auth provider:**
- Not applicable for end-user auth. API keys for vector DB and LLM to be configured via env.

## Monitoring & Observability

**Error tracking / Logs:**
- Not present. To be defined when pipeline code exists.

## CI/CD & Deployment

**Hosting / CI:**
- Not specified (tutorial scaffold).

## Environment Configuration

**Required env vars (when code exists):**
- Vector DB API key / endpoint (name TBD).
- Embeddings API key (if cloud).
- LLM API key.
- Document in README or INTEGRATIONS.md; never commit secrets.

**Secrets location:**
- Use `.env` (or equivalent) and keep it out of version control.

## Webhooks & Callbacks

**Incoming / Outgoing:**
- None (RAG pipeline is request/response oriented as described).

---
*Integration audit: 2025-02-25*
