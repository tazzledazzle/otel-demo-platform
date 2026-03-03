# Technical Prep — Pearl Health Senior SWE (Applied AI)

Use this for the technical exercise and panel. Refresh RAG, vector DBs, and LLM observability/evaluation so you can discuss tradeoffs and design clearly.

---

## 1. RAG (Retrieval-Augmented Generation) — flow and talking points

**High-level flow**

1. **Ingest** — Source documents (e.g. clinical guidelines, policies).
2. **Chunking** — Split into segments (by paragraph, section, token limit, or semantic boundaries). Overlap can improve context at boundaries.
3. **Embedding** — Encode chunks with an embedding model (e.g. OpenAI, Cohere, open-source) → vectors.
4. **Indexing** — Store vectors in a vector DB; optionally store metadata (source, date, type).
5. **Retrieval** — At query time: embed the query, run similarity search (e.g. k-NN, approximate nearest neighbor), return top-k chunks.
6. **Generation** — Pass retrieved chunks + query to an LLM with a prompt; get answer. Optionally cite sources.

**Design topics you should be able to discuss**

- **Chunking**: Fixed size vs semantic (sentence/section). Tradeoffs: consistency vs context preservation. Overlap to reduce boundary issues.
- **Embeddings**: Model choice (quality, cost, latency), dimension size, normalization.
- **Retrieval**: k and thresholds; hybrid search (keyword + semantic) for better recall; reranking (e.g. cross-encoder) for precision.
- **Security and compliance**: Access control on indexed data; audit logging; PHI handling and HIPAA (encryption, access logs, BAA if using third-party APIs).
- **Scale**: Batch indexing vs real-time; caching; scaling the vector store and embedding API.

---

## 2. Vector databases — concepts

- **What**: Store high-dimensional vectors and support similarity search (e.g. cosine, dot product). Used for semantic search over embeddings.
- **Options**: Pinecone, Weaviate, pgvector (Postgres), Chroma, OpenSearch with k-NN, etc. Tradeoffs: managed vs self-hosted, scale, filter support, cost.
- **Index types**: Approximate Nearest Neighbor (ANN) for scale (e.g. HNSW, IVF) vs exact search for small datasets.
- **Metadata filters**: Filter by source, date, or other fields before or after vector search to support “retrieve from this doc set only” or compliance.

**Healthcare angle**: Access control, auditability, and where PHI is stored (encryption at rest/transit, BAAs with vendors).

---

## 3. Observability and evaluation for production LLM systems

**Observability**

- **Prompt and response logging**: Log prompts (sanitized), model, params, latency, token counts. Avoid logging raw PHI in plain text; use hashing or redaction.
- **Tracing**: Trace ID across retrieval → LLM → response for debugging and latency analysis.
- **Metrics**: Latency (p50, p99), token usage, error rate, cost per request or per feature.
- **Alerts**: Latency SLOs, error spikes, cost anomalies, or quality regressions (if you have quality signals).

**Evaluation**

- **Quality**: Human eval (sample review), LLM-as-judge (e.g. relevance, faithfulness to sources), or task-specific metrics (e.g. accuracy on closed Q&A).
- **Retrieval**: Precision/recall of retrieved chunks, relevance scores, diversity.
- **Safety and compliance**: PII/PHI leakage checks, refusal on out-of-scope requests, alignment with policy.
- **Cost and latency**: Track per model/feature; set budgets and SLOs.

**Talking points for interviews**

- “We logged prompts and responses with trace IDs and tracked latency and token usage per feature.”
- “We evaluated retrieval with relevance labels and used [human review / LLM-as-judge] for generation quality.”
- “We had alerts on latency and errors and reviewed cost weekly to stay within budget.”

---

## 4. System design — “Design a service that uses LLMs to summarize patient data”

Use this as a mental outline; adapt to the exact question.

- **Scope**: Clarify: real-time vs batch, which data (notes, claims, labs), who uses it (providers, care managers), and compliance (HIPAA, audit).
- **Data pipeline**: Ingest from [EHR/API/warehouse]; sanitize/redact if needed; chunk or segment for context limits.
- **RAG vs summarization**: If “summarize given documents” → direct summarization with citation. If “answer over a large corpus” → RAG (chunk, embed, retrieve, then summarize).
- **LLM layer**: Model choice (quality vs cost/latency); prompt design; handling long context (chunking, map-reduce, or long-context model).
- **APIs**: REST or internal events; auth and scope (per user/org); rate limits and timeouts.
- **Observability**: Logging (no PHI in logs), tracing, latency and cost metrics, quality sampling.
- **Security and compliance**: Encryption, access control, audit logs, BAA with LLM/embedding providers; PHI minimization.

---

## 5. Coding prep (technical exercise)

- **LeetCode-style**: Practice medium-level problems (arrays, strings, hash maps, trees, graphs). Focus on clear code, edge cases, and a short complexity comment.
- **Discussion**: Be ready to explain tradeoffs, test cases, and how you’d extend or harden the solution (e.g. scale, errors, validation).

---

## Quick reference

| Topic | One-line summary |
|-------|------------------|
| RAG flow | Chunk → embed → index → retrieve (similarity) → LLM with context → response. |
| Vector DB | Store embeddings; support similarity search and optional metadata filters. |
| Observability | Log prompts/responses (no PHI), trace IDs, latency, tokens, cost; alert on SLOs. |
| Evaluation | Retrieval quality (precision/recall), generation quality (human or LLM judge), cost/latency, safety/compliance. |
