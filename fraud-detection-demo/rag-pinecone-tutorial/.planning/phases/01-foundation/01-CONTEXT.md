# Phase 1: Foundation — Context

**Gathered:** 2026-02-25
**Status:** Ready for planning

<domain>
## Phase Boundary

Deliver one runnable pipeline: ingest documents, chunk, embed, and index into a Pinecone-style vector store. No retrieval or LLM in this phase. Clear setup (API keys, index creation); engineer-oriented, code-first.

</domain>

<decisions>
## Implementation Decisions

### Pipeline steps
- Ingest (e.g. load a few docs or files), chunk, embed, upsert to vector store.
- Single run end-to-end; no continuous ingestion or scheduling.

### Store and embeddings
- Pinecone or Pinecone-compatible API; embedding model TBD (e.g. OpenAI, local).
- Success = learner runs pipeline and sees index populated (or count/status).

### Scope
- Small document set (e.g. a few markdown or text files); no production scale.
- Clear env/keys setup; no retrieval or query in Phase 1.

### Claude's Discretion
- Exact chunking strategy; embedding provider; sample documents; client library.

</decisions>

<specifics>
## Specific Ideas

No specific requirements — open to standard RAG ingestion patterns.

</specifics>

<deferred>
## Deferred Ideas

- Retrieval, LLM integration, query UI — later phases.

</deferred>

---
*Phase: 01-foundation*
*Context gathered: 2026-02-25*
