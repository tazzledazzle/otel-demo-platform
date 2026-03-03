"""Minimal FastAPI app: POST /chat and POST /rag delegating to services."""

import sys
from pathlib import Path

# Allow running as module from project root (src/ai_app/api/app.py -> repo root)
_root = Path(__file__).resolve().parents[3]
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from fastapi import FastAPI
from pydantic import BaseModel

from config.settings import Settings
from ai_app.llm.openai_compat import OpenAICompatClient
from ai_app.services.chat import ChatService
from ai_app.services.rag import RAGService

app = FastAPI(title="AI App API", version="0.1.0")

_settings: Settings | None = None
_chat_service: ChatService | None = None
_rag_service: RAGService | None = None


def _get_settings() -> Settings:
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings


def _get_chat_service() -> ChatService:
    global _chat_service
    if _chat_service is None:
        s = _get_settings()
        client = OpenAICompatClient(
            base_url=s.llm_base_url,
            api_key=s.openai_api_key,
            model=s.llm_model,
            default_temperature=s.temperature,
            default_max_tokens=s.max_tokens,
        )
        _chat_service = ChatService(client, s.prompts_dir)
    return _chat_service


def _get_rag_service() -> RAGService:
    global _rag_service
    if _rag_service is None:
        s = _get_settings()
        llm = OpenAICompatClient(
            base_url=s.llm_base_url,
            api_key=s.openai_api_key,
            model=s.llm_model,
            default_temperature=0.3,
            default_max_tokens=s.max_tokens,
        )
        emb = OpenAICompatClient(
            base_url=s.llm_base_url,
            api_key=s.openai_api_key,
            model="nomic-embed-text",
            default_temperature=0,
            default_max_tokens=0,
        )
        _rag_service = RAGService(llm=llm, prompts_dir=s.prompts_dir, embedding_client=emb)
    return _rag_service


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str


class RAGRequest(BaseModel):
    question: str


class RAGResponse(BaseModel):
    answer: str


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest) -> ChatResponse:
    service = _get_chat_service()
    reply = await service.chat(req.message)
    return ChatResponse(reply=reply)


@app.post("/rag", response_model=RAGResponse)
async def rag(req: RAGRequest) -> RAGResponse:
    service = _get_rag_service()
    answer = await service.query(req.question)
    return RAGResponse(answer=answer)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
