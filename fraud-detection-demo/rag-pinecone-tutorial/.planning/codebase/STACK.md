# Technology Stack

**Analysis Date:** 2025-02-25

## Languages

**Primary:**
- Not yet chosen. PROJECT.md implies a stack suitable for RAG + vector store + LLM (e.g. Python or Node).

**Secondary:**
- Not applicable.

## Runtime

**Environment:**
- None (no application).

**Package manager:**
- None. To be added with first phase (e.g. pip/poetry, npm/yarn).

**Lockfile:**
- Not present.

## Frameworks

**Core:**
- Intended: Vector DB (Pinecone-style), embeddings, LLM; optional LangChain (from `rag-pinecone-tutorial/.planning/PROJECT.md`).

**Testing:**
- Not selected.

**Build/Dev:**
- GSD uses `config.json` for workflow only; no app build tool yet.

## Key Dependencies

**Critical (planned):**
- Vector DB client (Pinecone or compatible).
- Embeddings provider (e.g. OpenAI, local model).
- LLM provider for question-answering/search.
- Optional: LangChain (or similar) for orchestration.

**Infrastructure:**
- To be defined (e.g. local Pinecone or cloud index).

## Configuration

**Environment:**
- Not configured. Future: env vars for API keys and endpoints (see INTEGRATIONS.md).

**Build:**
- No build config (no app).

## Platform Requirements

**Development:**
- To be defined with first phase (e.g. Python 3.x, Node LTS).

**Production:**
- Tutorial focus; production deployment optional.

---
*Stack analysis: 2025-02-25*
