"""RAG service: ingest docs into Chroma, retrieve top-k, build prompt, call LLM."""

from pathlib import Path

import chromadb
from chromadb.config import Settings as ChromaSettings

from ai_app.llm.base import BaseLLMClient, Message
from ai_app.llm.embeddings import get_embeddings
from ai_app.llm.openai_compat import OpenAICompatClient
from ai_app.prompts.loader import get_prompt


def _default_embedding_model() -> str:
    return "nomic-embed-text"


class RAGService:
    """Ingest documents into in-process Chroma; query with retrieval + LLM."""

    def __init__(
        self,
        llm: BaseLLMClient,
        prompts_dir: Path,
        *,
        embedding_client: OpenAICompatClient | None = None,
        embedding_model: str | None = None,
        persist_directory: str | None = None,
        collection_name: str = "rag_docs",
        top_k: int = 3,
    ) -> None:
        self._llm = llm
        self._prompts_dir = prompts_dir
        self._embedding_client = embedding_client
        self._embedding_model = embedding_model or _default_embedding_model()
        self._top_k = top_k
        self._persist_directory = persist_directory or "./chroma_data"
        self._collection_name = collection_name
        self._client = chromadb.PersistentClient(
            path=self._persist_directory,
            settings=ChromaSettings(anonymized_telemetry=False),
        )
        self._collection = self._client.get_or_create_collection(
            name=self._collection_name,
            metadata={"description": "RAG documents"},
        )

    def _embed(self, texts: list[str]) -> list[list[float]]:
        if not self._embedding_client:
            raise RuntimeError("RAGService requires embedding_client for ingest/query")
        # OpenAICompatClient has _client (OpenAI)
        return get_embeddings(
            self._embedding_client._client,
            self._embedding_model,
            texts,
        )

    def ingest(self, documents: list[str], ids: list[str] | None = None) -> None:
        """Ingest documents into the vector store."""
        if not documents:
            return
        if ids is None:
            ids = [f"doc_{i}" for i in range(len(documents))]
        embeddings = self._embed(documents)
        self._collection.upsert(ids=ids, documents=documents, embeddings=embeddings)

    def _retrieve(self, query: str, top_k: int | None = None) -> list[str]:
        k = top_k or self._top_k
        q_emb = self._embed([query])
        results = self._collection.query(query_embeddings=q_emb, n_results=k, include=["documents"])
        docs = results.get("documents") or []
        if not docs or not docs[0]:
            return []
        return list(docs[0])

    async def query(self, question: str, top_k: int | None = None) -> str:
        """Retrieve top-k chunks, build prompt with context, call LLM, return answer."""
        context_chunks = self._retrieve(question, top_k=top_k)
        context = "\n\n".join(context_chunks) if context_chunks else "(No relevant context found.)"
        prompt_text = get_prompt(
            "rag_qa",
            self._prompts_dir,
            context=context,
            question=question,
        )
        messages = [Message(role="user", content=prompt_text)]
        return await self._llm.generate(messages)
