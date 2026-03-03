# Research: RAG for Runbooks and Postmortems

**Domain:** Retrieval-augmented generation; runbook and postmortem knowledge bases; production RAG.  
**Consumed by:** Phase 2 (Knowledge Base), Phase 3 (RAG & Retrieval).

---

## Summary

Production RAG goes beyond “embed → retrieve → generate.” Success depends on chunking strategy, hybrid retrieval (dense + sparse/metadata), metadata filtering, and context assembly within token budgets. Most RAG systems fail in production due to retrieval degradation at scale, embedding drift, citation hallucination, and poor chunking. Runbooks and postmortems benefit from document-type-aware chunking and strong metadata (service, severity, root cause category) for precise filtering.

---

## Key Findings

### Chunking

- **Avoid naive fixed-window chunking** (e.g. 512 tokens) that breaks tables and semantic continuity.
- **Prefer:** Hierarchical or context-aware chunking with configurable overlap and boundary detection; **adaptive chunking by document type** (e.g. runbooks: by section/step; postmortems: by section like timeline, root cause, remediation).
- **Semantic validation:** Chunks should represent single, coherent ideas to improve retrieval relevance.
- **~500-token chunks** (as in your design) are a reasonable default; tune overlap and boundaries per runbook vs postmortem structure.
- Good chunking can reduce retrieval calls by **30–40%** for the same question quality.

### Hybrid Retrieval

- **Hybrid retrieval** (dense vector + sparse/keyword, e.g. BM25) generally **outperforms** dense-only or sparse-only.
- Use **Reciprocal Rank Fusion (RRF)** or similar to combine ranking from semantic and keyword/metadata paths.
- **Metadata filtering** (service name, alert type, severity, root cause category) is critical for runbooks and postmortems so the agent gets the right service and incident type.
- Vector stores should use **approximate nearest-neighbor** (e.g. HNSW) and **consistent embedding models** at index and query time to avoid semantic drift.

### Context Assembly

- **Context assembler** packs selected chunks into the prompt while respecting **token budget** and adding **source citations** to reduce hallucination.
- Dynamic context window management helps control cost and latency while preserving accuracy.

### Production Failure Modes

- **Retrieval degradation** as the knowledge base grows (100K → 10M docs).
- **Embedding drift** when domain language or runbook format changes but indices are not re-indexed.
- **Citation hallucination**: LLM cites sources that do not support the claim—mitigate with citation validation and structured prompts.
- **Chunking issues**: Semantic continuity broken across chunks.
- **Context truncation**: Critical evidence dropped when packing; monitor and set chunk limits accordingly.

### Implications for This Project

- **Re-index on deploy** (e.g. K8s Job) is the right pattern to limit embedding drift and keep runbooks/postmortems current.
- Implement **hybrid retrieval**: semantic search + metadata filter (service, alert type) and optionally keyword/BM25 if runbooks use stable terminology.
- Store **structured metadata** on every postmortem (service, severity, root cause category) and runbook (service, alert type, procedure type).
- **~500-token chunks** with section-aware boundaries for runbooks and postmortems; validate retrieval quality before locking in.
- Plan for **evaluation and monitoring** of retrieval quality (e.g. relevance ratings, hypothesis_accuracy vs postmortem) as in your observability phase.

---

## References (from search)

- Production RAG architecture (Likhon’s Gen AI Blog; QLoop; Nic Chin – 12-component system, 96.8% accuracy).
- “When RAG Fails: Debugging Retrieval Quality Issues” (Swiftorial).
- LangChain + Pinecone production RAG tutorial.
