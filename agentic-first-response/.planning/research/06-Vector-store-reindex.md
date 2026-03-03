# Research: Vector Store Choice and Re-index Pipeline (Chroma, pgvector)

**Domain:** Vector databases; RAG indexing; production pipelines.  
**Consumed by:** Phase 2 (Knowledge Base & Ingestion).

---

## Summary

**Chroma** is an AI-native embedding store with simple APIs and good fit for LLM apps; **pgvector** is a PostgreSQL extension that keeps vectors in the same database as metadata and application data. Both support production RAG. Choice depends on existing stack (e.g. already on Postgres → pgvector) and operational preference (managed vs self-hosted). Re-indexing on deploy (e.g. K8s Job) keeps runbooks and postmortems current and limits embedding drift.

---

## Key Findings

### Chroma

- **Pros:** Purpose-built for embeddings; simple Python/JS SDKs; fast to prototype; good for LLM-centric pipelines.
- **Cons:** Separate store from application DB; operational story (backup, HA) is less standardized than Postgres.
- **Use when:** Greenfield RAG, no strong need to query vectors and application data in one place; team prefers a dedicated vector DB.

### pgvector

- **Pros:** PostgreSQL extension; vectors and metadata in one DB; ACID, backups, and HA follow existing Postgres practices; strong scaling with ANN indexes (e.g. HNSW, IVFFlat).
- **Cons:** Slightly more setup (extension, indexes); query patterns need to be understood for performance.
- **Use when:** Already using Postgres; want unified storage for metadata (service, severity, root cause) and vectors; need transactional consistency (e.g. “add postmortem and its chunks” in one transaction).

### RAG Pipeline Stages (generic)

1. **Load** – Runbooks (markdown from repo), postmortems (from store or export).
2. **Chunk** – Section-aware, ~500 tokens, with overlap as needed.
3. **Embed** – One embedding model at index and query time.
4. **Store** – Upsert into Chroma or pgvector with metadata (service, alert_type, severity, root_cause_category, source doc ID).
5. **Query** – Hybrid retrieval (vector + metadata filter) at triage time.
6. **Re-index** – On deploy or on a schedule; full or incremental by source/doc ID.

### Re-index on Deploy

- **Pattern:** CI/CD or deploy pipeline runs a **K8s Job** (or similar) that (1) loads current runbooks from repo and postmortems from DB/export, (2) chunks and embeds, (3) upserts into the vector store (replace collection or upsert by ID).
- **Benefits:** Runbook changes and new postmortems are reflected without a separate “ingest service”; same pattern as described for “Code Helper ingest.”
- **Idempotency:** Use stable doc/chunk IDs (e.g. path + section, or postmortem_id + chunk index) so re-runs do not duplicate; delete-and-recreate or upsert by ID.

### Implications for This Project

- **Choice:** pgvector if you already use Postgres for app data and want metadata (service, severity, root cause) co-located; Chroma if you want a dedicated, simple vector store and will store metadata in the same store’s document metadata.
- **Re-index Job:** Implement a batch job (K8s Job or equivalent) that runs on deploy (or on a schedule): read runbooks from repo, read postmortems from source, chunk, embed, write to vector store with metadata; use stable IDs for upsert/delete.
- **Metadata schema:** Align with RAG phase: at least `service`, `alert_type`, `severity`, `root_cause_category`, `source` (runbook vs postmortem), `doc_id` for filtering and citation.

---

## References (from search)

- “Implementing a Vector Database in a RAG System for a Helpdesk Chatbot with pgvector” (Dev.to).
- Chroma indexing and RAG examples (Haystack).
- “Production RAG with a Postgres Vector Store and Open-Source Models” (christophergs.com).
- LangChain + Chroma RAG tutorials.
