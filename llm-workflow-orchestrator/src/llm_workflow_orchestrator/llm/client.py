"""OpenAI-compatible LLM client."""

from dataclasses import dataclass
from typing import Any

from openai import AsyncOpenAI


@dataclass
class LLMResponse:
    """Response from a completion call."""

    content: str | None
    tool_calls: list[dict[str, Any]] | None  # [{"id": str, "name": str, "arguments": str}, ...]


class LLMClient:
    """Thin wrapper over OpenAI-compatible API (OpenAI, Anthropic compat, Ollama, etc.)."""

    def __init__(self, *, base_url: str, api_key: str, model: str) -> None:
        self._client = AsyncOpenAI(base_url=base_url, api_key=api_key)
        self._model = model

    async def complete(
        self,
        user_message: str,
        *,
        system_message: str | None = None,
        tools: list[dict[str, Any]] | None = None,
    ) -> LLMResponse:
        """Send messages and return assistant content and optional tool calls."""
        messages: list[dict[str, Any]] = []
        if system_message:
            messages.append({"role": "system", "content": system_message})
        messages.append({"role": "user", "content": user_message})

        kwargs: dict[str, Any] = {"model": self._model, "messages": messages}
        if tools:
            kwargs["tools"] = tools

        response = await self._client.chat.completions.create(**kwargs)
        choice = response.choices[0]
        msg = choice.message

        tool_calls_list: list[dict[str, Any]] | None = None
        if getattr(msg, "tool_calls", None):
            tool_calls_list = [
                {
                    "id": tc.id,
                    "name": tc.function.name,
                    "arguments": tc.function.arguments or "",
                }
                for tc in msg.tool_calls
            ]

        return LLMResponse(
            content=msg.content if msg.content else None,
            tool_calls=tool_calls_list,
        )
