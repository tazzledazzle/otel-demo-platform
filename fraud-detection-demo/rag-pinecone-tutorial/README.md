# RAG Pinecone Tutorial

A single-run pipeline that ingests documents from a folder, chunks them, embeds with OpenAI, and upserts into a Pinecone index.

## What this is

Ingest → chunk → embed → index. You run one command; the script reads files from `docs/`, splits them into chunks, creates embeddings, and populates a Pinecone vector index. No retrieval or LLM in this phase—just the foundation.

## Setup

1. Copy the env template and add your API keys:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and set:
   - `PINECONE_API_KEY` — from [Pinecone console](https://app.pinecone.io) → API Keys
   - `OPENAI_API_KEY` — from OpenAI platform → API keys

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Run

From the repo root (`rag-pinecone-tutorial`):

```bash
python src/ingest.py
```

## Success

The script creates the index if needed, upserts all chunk vectors, then prints index statistics. You should see `total_vector_count` (and optionally namespace counts) in the output, confirming the index is populated.
