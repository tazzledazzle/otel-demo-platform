"""
Single-run RAG ingestion pipeline: read docs from docs/ → chunk → embed → upsert to Pinecone.
Run from repo root: python src/ingest.py
"""
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from openai import OpenAI
from pinecone import Pinecone, ServerlessSpec, CloudProvider, AwsRegion, Metric

load_dotenv()

INDEX_NAME = "rag-tutorial"
NAMESPACE = "tutorial"
EMBEDDING_DIM = 1536
BATCH_SIZE = 1000
DOCS_DIR = Path(__file__).resolve().parent.parent / "docs"


def require_env(*names: str) -> None:
    missing = [n for n in names if not os.getenv(n)]
    if missing:
        print("Missing required environment variables:", ", ".join(missing), file=sys.stderr)
        print("Copy .env.example to .env and set PINECONE_API_KEY and OPENAI_API_KEY.", file=sys.stderr)
        sys.exit(1)


def load_documents() -> list[tuple[str, str]]:
    """Load .md and .txt files from docs/; return list of (source_id, text)."""
    if not DOCS_DIR.exists():
        raise FileNotFoundError(f"Docs directory not found: {DOCS_DIR}")
    pairs = []
    for path in sorted(DOCS_DIR.glob("*.md")) + sorted(DOCS_DIR.glob("*.txt")):
        text = path.read_text(encoding="utf-8").strip()
        if text:
            pairs.append((path.stem, text))
    return pairs


def chunk_documents(pairs: list[tuple[str, str]]) -> list[tuple[str, str]]:
    """Split each document with RecursiveCharacterTextSplitter; return (id, text) per chunk."""
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = []
    for source_id, text in pairs:
        parts = splitter.split_text(text)
        for i, part in enumerate(parts):
            chunk_id = f"{source_id}_{i}"
            chunks.append((chunk_id, part))
    return chunks


def embed_chunks(client: OpenAI, chunks: list[tuple[str, str]]) -> list[tuple[str, list[float], str]]:
    """Return list of (id, values, text) for each chunk."""
    texts = [t for _, t in chunks]
    response = client.embeddings.create(
        input=texts,
        model="text-embedding-3-small",
    )
    vectors = [d.embedding for d in response.data]
    return [(chunk_id, vec, text) for (chunk_id, text), vec in zip(chunks, vectors)]


def ensure_index(pc: Pinecone):
    """Create serverless index if missing; wait until ready; return Index(host)."""
    if not pc.has_index(INDEX_NAME):
        pc.create_index(
            name=INDEX_NAME,
            dimension=EMBEDDING_DIM,
            metric=Metric.COSINE,
            spec=ServerlessSpec(cloud=CloudProvider.AWS, region=AwsRegion.US_WEST_2),
        )
    # Wait for index to be ready
    while True:
        desc = pc.describe_index(INDEX_NAME)
        if getattr(desc, "status", None) and getattr(desc.status, "ready", False):
            break
        import time
        time.sleep(2)
    host = desc.host
    return pc.Index(host=host)


def main() -> None:
    require_env("PINECONE_API_KEY", "OPENAI_API_KEY")

    pairs = load_documents()
    if not pairs:
        print("No documents found in docs/ (expected .md or .txt).", file=sys.stderr)
        sys.exit(1)

    chunks = chunk_documents(pairs)
    print(f"Loaded {len(pairs)} doc(s), {len(chunks)} chunk(s).")

    client = OpenAI()
    triples = embed_chunks(client, chunks)
    print("Embeddings created.")

    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    index = ensure_index(pc)
    print("Index ready.")

    for i in range(0, len(triples), BATCH_SIZE):
        batch = triples[i : i + BATCH_SIZE]
        vectors = [
            {"id": cid, "values": vec, "metadata": {"text": text}}
            for cid, vec, text in batch
        ]
        index.upsert(vectors=vectors, namespace=NAMESPACE)
    print(f"Upserted {len(triples)} vectors to namespace '{NAMESPACE}'.")

    stats = index.describe_index_stats()
    total = stats.get("total_vector_count", 0)
    namespaces = stats.get("namespaces") or {}
    print("Index stats:", "total_vector_count =", total)
    if namespaces:
        print("Namespaces:", namespaces)


if __name__ == "__main__":
    main()
