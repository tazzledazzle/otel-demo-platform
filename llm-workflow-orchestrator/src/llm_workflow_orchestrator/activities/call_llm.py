"""Activity: call LLM (OpenAI-compatible API)."""

from __future__ import annotations

from typing import Any

from llm_workflow_orchestrator.config import (
    get_llm_api_key,
    get_llm_base_url,
    get_llm_model,
)
from llm_workflow_orchestrator.llm.client import LLMClient


def _get_client() -> LLMClient:
    return LLMClient(
        base_url=get_llm_base_url(),
        api_key=get_llm_api_key(),
        model=get_llm_model(),
    )


async def call_llm(
    prompt: str,
    *,
    system_message: str | None = None,
    tools: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Call the LLM and return content and optional tool_calls (serializable)."""
    client = _get_client()
    response = await client.complete(
        prompt,
        system_message=system_message,
        tools=tools,
    )
    return {
        "content": response.content,
        "tool_calls": response.tool_calls,
    }
