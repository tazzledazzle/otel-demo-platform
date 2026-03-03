# Phase 1: Foundation — Research

**Researched:** 2026-02-25
**Domain:** RAG ingestion pipeline — document load, chunking, embeddings, Pinecone indexing
**Confidence:** HIGH

## Summary

Phase 1 delivers a single runnable pipeline: ingest documents → chunk → embed → upsert into a Pinecone index, with clear API/key setup and no retrieval or LLM. Pinecone is the right choice for this tutorial: managed, minimal ops, simple Python SDK, and the pipeline teaches each step explicitly. Use **bring-your-own vectors** (create index with `dimension`, then upsert precomputed vectors) so learners see ingest → chunk → embed → upsert; avoid Pinecone’s integrated embedding for Phase 1 so the embed step is visible. Standard stack: **Python 3.10+**, **pinecone** (official SDK), **openai** (embeddings), **langchain-text-splitters** (chunking only), and optional **sentence-transformers** for a local embedding path. Chunking: **RecursiveCharacterTextSplitter** with ~500–1000 character chunks and overlap; embedding dimension must match index (e.g. 1536 for text-embedding-3-small, 384 for all-MiniLM-L6-v2). Success = run script, then confirm index populated via `describe_index_stats()` or console.

**Primary recommendation:** Use Pinecone with bring-your-own vectors; OpenAI text-embedding-3-small for cloud path and sentence-transformers all-MiniLM-L6-v2 for local; RecursiveCharacterTextSplitter; single Python script and .env for keys.

<user_constraints>

## User Constraints (from CONTEXT.md)

### Locked Decisions
- Pipeline steps: Ingest (e.g. load a few docs or files), chunk, embed, upsert to vector store. Single run end-to-end; no continuous ingestion or scheduling.
- Store and embeddings: Pinecone or Pinecone-compatible API; embedding model TBD (e.g. OpenAI, local). Success = learner runs pipeline and sees index populated (or count/status).
- Scope: Small document set (e.g. a few markdown or text files); no production scale. Clear env/keys setup; no retrieval or query in Phase 1.

### Claude's Discretion
- Exact chunking strategy; embedding provider; sample documents; client library.

### Deferred Ideas (OUT OF SCOPE)
- Retrieval, LLM integration, query UI — later phases.

</user_constraints>

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| pinecone | ≥5.x (current) | Vector index create, upsert, describe_index_stats | Official SDK; serverless index create with dimension; simple upsert(vectors=[...]). |
| openai | ≥1.x | Embeddings (text-embedding-3-small) | De facto cloud embedding API; 1536 dims; batch input; well documented. |
| langchain-text-splitters | ≥0.3.x | RecursiveCharacterTextSplitter | Standalone package (no full LangChain); recursive split by paragraph/line/space; chunk_size/chunk_overlap. |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| sentence-transformers | ≥3.x | Local embeddings (all-MiniLM-L6-v2, 384 dims) | No API key; offline; tutorial “local” path. |
| python-dotenv | ≥1.x | Load .env for PINECONE_API_KEY, OPENAI_API_KEY | Standard env handling; keep keys out of code. |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Pinecone | Qdrant, Weaviate, pgvector | Pinecone: zero ops, fastest setup. Qdrant/Weaviate: self-host, more config. pgvector: good if already on Postgres. |
| OpenAI embeddings | Cohere, Voyage, local (sentence-transformers) | OpenAI: most common, 1536 dims. Local: no key, 384 dims, different index dimension. |
| langchain-text-splitters | Custom split on \n\n | Hand-rolling loses recursive fallback and overlap; use library. |

**Installation:**
```bash
pip install pinecone openai langchain-text-splitters python-dotenv
# Optional local embeddings:
pip install sentence-transformers
```

## Architecture Patterns

### Recommended Project Structure
```
rag-pinecone-tutorial/
├── .env.example          # PINECONE_API_KEY=, OPENAI_API_KEY= (optional)
├── .env                  # gitignored; actual keys
├── requirements.txt     # pinecone, openai, langchain-text-splitters, python-dotenv
├── docs/                 # or sample_docs/ — 2–5 small .md or .txt files
│   └── *.md
├── src/
│   └── ingest.py        # or run.py: load_docs → chunk → embed → create_index (if needed) → upsert
└── README.md            # setup (keys, index creation), how to run, success = index populated
```

### Pattern 1: Single-run pipeline
**What:** One script that loads files, chunks, embeds, ensures index exists, upserts in batches (e.g. up to 1000 vectors per upsert), then prints index stats.
**When to use:** Phase 1 success criteria — learner runs once and sees index populated.
**Example flow:**
1. Load env (e.g. `python-dotenv`).
2. Ingest: read a few files from `docs/` (Path.glob or list of paths).
3. Chunk: `RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50).split_text(text)` per doc; assign stable IDs (e.g. `doc_id + "_" + str(i)`).
4. Embed: call OpenAI or sentence-transformers for list of chunk strings; get list of vectors.
5. Index: `pc = Pinecone(api_key=...)`; if not `pc.has_index(name)`: `pc.create_index(name=..., dimension=..., metric=Metric.COSINE, spec=ServerlessSpec(...))`; wait if needed; `index = pc.Index(host=...)` or get host from `describe_index`; `index.upsert(vectors=[{"id": id, "values": vec, "metadata": {"text": chunk}}], namespace=...)` in batches of ≤1000.
6. Verify: `index.describe_index_stats()` and print total_vector_count or namespace counts.

### Pattern 2: Index creation (bring-your-own vectors)
**What:** Create serverless index with fixed dimension matching embedding model; no integrated embedding.
**When to use:** Phase 1 so embed step is explicit.
**Example:**
```python
# Source: https://sdk.pinecone.io/python/db_control/serverless-indexes.html
from pinecone import Pinecone, ServerlessSpec, CloudProvider, AwsRegion, Metric

pc = Pinecone(api_key='<<PINECONE_API_KEY>>')
pc.create_index(
    name='my-index',
    dimension=1536,  # must match embedding model (e.g. text-embedding-3-small)
    metric=Metric.COSINE,
    spec=ServerlessSpec(
        cloud=CloudProvider.AWS,
        region=AwsRegion.US_WEST_2
    ),
)
```
After create, use `pc.describe_index("my-index")` to get `host`; then `pc.Index(host=host).upsert(...)`.

### Anti-Patterns to Avoid
- **Skipping chunking:** Upserting whole documents loses granular retrieval later; always chunk.
- **Dimension mismatch:** Index `dimension` must exactly match embedding size (1536 for text-embedding-3-small, 384 for all-MiniLM-L6-v2).
- **Hardcoding keys:** Use .env and document in README; never commit .env.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Chunking | Custom split by size or regex | RecursiveCharacterTextSplitter (langchain-text-splitters) | Recursive separators (\n\n, \n, space) and overlap are standard; edge cases handled. |
| Embeddings | Own model or API client | OpenAI API or sentence-transformers | Token limits, batching, normalization; well tested. |
| Vector store | In-memory or file-based index | Pinecone | Scaling, persistence, and API are non-trivial. |

**Key insight:** Chunking and embedding have subtle failure modes (splitting mid-sentence, rate limits, dimension consistency). Use established libraries and Pinecone so the tutorial focuses on pipeline structure and keys.

## Common Pitfalls

### Pitfall 1: Index dimension vs embedding dimension mismatch
**What goes wrong:** Upsert fails or wrong index type; queries meaningless.
**Why it happens:** Index created with one dimension (e.g. 1536) but embeddings from another model (e.g. 384).
**How to avoid:** Single constant or config for embedding dimension; use same value in `create_index(dimension=...)` and when choosing model (OpenAI 1536 vs sentence-transformers 384).
**Warning signs:** Error on upsert about dimension; or no error but retrieval nonsense.

### Pitfall 2: Index not ready before upsert
**What goes wrong:** Upsert to missing index or too soon after create.
**Why it happens:** Serverless index creation is async; need host before data operations.
**How to avoid:** Use `pc.has_index(name)` before create; after `create_index`, wait (e.g. poll `describe_index` until ready) then get host and use `pc.Index(host=...)`.
**Warning signs:** Connection errors or "index not found" when calling upsert.

### Pitfall 3: API keys not loaded
**What goes wrong:** Runtime error or 401 from Pinecone/OpenAI.
**Why it happens:** Keys in .env but script doesn’t load .env, or .env not created.
**How to avoid:** `from dotenv import load_dotenv; load_dotenv()` at entry; README: copy .env.example to .env and fill keys; validate key presence before create_index/embed.
**Warning signs:** Missing environment variable or authentication errors.

### Pitfall 4: Upsert batch too large
**What goes wrong:** Request rejected or timeouts.
**Why it happens:** API recommends up to 1000 vectors per upsert (Pinecone data plane).
**How to avoid:** Batch chunks into lists of ≤1000; loop over batches and call `index.upsert(vectors=batch, namespace=...)`.
**Warning signs:** 400 or 413 from Pinecone.

## Code Examples

Verified patterns from official sources:

### Create serverless index (dense, bring-your-own vectors)
```python
# Source: https://sdk.pinecone.io/python/db_control/serverless-indexes.html
from pinecone import Pinecone, ServerlessSpec, CloudProvider, AwsRegion, Metric

pc = Pinecone(api_key='<<PINECONE_API_KEY>>')
pc.create_index(
    name='my-index',
    dimension=1536,
    metric=Metric.COSINE,
    spec=ServerlessSpec(
        cloud=CloudProvider.AWS,
        region=AwsRegion.US_WEST_2
    ),
)
```

### Upsert vectors (Python SDK)
```python
# Source: Pinecone docs quickstart / upsert reference
index = pc.Index(host=index_host)
index.upsert(
    vectors=[
        {"id": "vec1", "values": [0.1, 0.1, ...], "metadata": {"text": "chunk content"}},
        {"id": "vec2", "values": [0.2, 0.2, ...], "metadata": {"text": "another chunk"}},
    ],
    namespace="example-namespace",
)
# Batch limit: up to 1000 vectors per request (docs.pinecone.io reference).
```

### Verify index populated
```python
# Source: Pinecone describe_index_stats reference
stats = index.describe_index_stats()
# e.g. {'dimension': 1536, 'total_vector_count': N, 'namespaces': {...}}
print("Vector count:", stats.get("total_vector_count"))
```

### OpenAI embeddings
```python
# Source: https://platform.openai.com/docs/api-reference/embeddings
from openai import OpenAI
client = OpenAI()
response = client.embeddings.create(
    input=["first chunk", "second chunk"],
    model="text-embedding-3-small",
)
vectors = [d.embedding for d in response.data]
# len(vectors[0]) == 1536
```

### RecursiveCharacterTextSplitter
```python
# Source: LangChain text splitters docs
from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
)
chunks = splitter.split_text(your_text)
```

### Local embeddings (sentence-transformers)
```python
# Source: sentence-transformers usage (PyPI / common docs)
from sentence_transformers import SentenceTransformer
model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(chunks, normalize_embeddings=True)
# shape (n_chunks, 384); use dimension=384 for Pinecone index.
```

## Pinecone vs Alternatives

| Option | Best for | Phase 1 fit |
|--------|----------|-------------|
| **Pinecone** | Managed, minimal ops, fast setup, simple SDK | **Use.** Aligns with “clear setup, engineer-oriented”; free tier; create_index + upsert + describe_index_stats sufficient. |
| Qdrant | Self-hosted or cloud, advanced filters | More setup; good later if tutorial adds filtering. |
| Weaviate | Self-hosted, hybrid search, GraphQL | Heavier; overkill for “ingest → index” only. |
| pgvector | Already using Postgres | Not Pinecone-style; different API; skip for Phase 1. |

**Recommendation:** Use **Pinecone** for Phase 1. Stay with bring-your-own vectors (create_index with dimension + upsert) so the pipeline clearly shows ingest → chunk → embed → upsert. Do not use Pinecone’s integrated embedding (create_index_for_model) in this phase so the embed step remains explicit.

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Pod-based indexes | Serverless by default | Pinecone serverless general availability | Simpler: no pod size; create_index with spec=ServerlessSpec. |
| text-embedding-ada-002 | text-embedding-3-small / 3-large | Jan 2024 | Better quality and cost; 1536/3072 dims; dimensions param optional. |
| Full LangChain for chunking | langchain-text-splitters only | Package split | Lighter dependency for chunking only. |

**Deprecated/outdated:**
- Relying on pod-based index creation for new projects — use serverless unless specific need.
- text-embedding-ada-002 for new work — use text-embedding-3-small or 3-large.

## Open Questions

1. **Sample documents**
   - What we know: Small set of .md or .txt in a single folder is sufficient.
   - What’s unclear: Exact number and topics (e.g. 3–5 project READMEs vs generic paragraphs).
   - Recommendation: Planner can add 3–5 small markdown files under `docs/` or `sample_docs/` with clear, short paragraphs so chunk count is predictable.

2. **Namespace**
   - What we know: Upsert accepts optional namespace; describe_index_stats returns per-namespace counts.
   - What’s unclear: Whether to use default namespace or one named (e.g. "tutorial").
   - Recommendation: Use a single namespace (e.g. "default" or "tutorial") for Phase 1; document in README.

## Sources

### Primary (HIGH confidence)
- Pinecone Python SDK — Serverless Indexes: https://sdk.pinecone.io/python/db_control/serverless-indexes.html (create_index, dimension, ServerlessSpec)
- Pinecone Data Plane API — Upsert: https://docs.pinecone.io/reference/api/latest/data-plane/upsert (vectors, batch limit 1000, namespace)
- Pinecone quickstart: https://docs.pinecone.io/guides/get-started/quickstart (SDK install, create_index_for_model vs bring-your-own)
- OpenAI Embeddings API: https://platform.openai.com/docs/api-reference/embeddings (input, model text-embedding-3-small)
- LangChain RecursiveCharacterTextSplitter: https://python.langchain.com/docs/concepts/text_splitters/ (chunk_size, chunk_overlap, standalone package)

### Secondary (MEDIUM confidence)
- WebSearch: Pinecone vs Qdrant/Weaviate (tutorial context); sentence-transformers local embeddings; chunking strategies (recursive, token limits); describe_index_stats

### Tertiary (LOW confidence)
- Exact Pinecone SDK minor version (5.x) — PyPI / release notes for current preferred version to pin in requirements.txt

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — official Pinecone, OpenAI, and LangChain splitter docs and SDK pages.
- Architecture: HIGH — single-run pipeline and bring-your-own index flow are standard and documented.
- Pitfalls: HIGH — dimension mismatch, index readiness, and batch limits come from official docs and common RAG guidance.

**Research date:** 2026-02-25
**Valid until:** ~30 days (Pinecone and OpenAI APIs stable; re-check SDK versions if pinning).

---

## RESEARCH COMPLETE
