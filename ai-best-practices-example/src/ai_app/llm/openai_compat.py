"""OpenAI-compatible LLM client (works with OpenAI and Ollama via base_url)."""

import asyncio
import logging
import time
from typing import Any

from openai import OpenAI
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from ai_app.llm.base import BaseLLMClient, Message

logger = logging.getLogger(__name__)


def _sync_create(
    client: OpenAI,
    model: str,
    body: list[dict[str, str]],
    temperature: float,
    max_tokens: int,
    **kwargs: Any,
) -> Any:
    return client.chat.completions.create(
        model=model,
        messages=body,
        temperature=temperature,
        max_tokens=max_tokens,
        **kwargs,
    )


class OpenAICompatClient(BaseLLMClient):
    """Uses OpenAI SDK with configurable base_url for Ollama or OpenAI."""

    def __init__(
        self,
        *,
        base_url: str,
        api_key: str = "placeholder",
        model: str = "llama3.2:3b",
        default_temperature: float = 0.7,
        default_max_tokens: int = 1024,
    ) -> None:
        self._client = OpenAI(base_url=base_url, api_key=api_key)
        self._model = model
        self._default_temperature = default_temperature
        self._default_max_tokens = default_max_tokens

    @retry(
        retry=retry_if_exception_type((Exception,)),
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        reraise=True,
    )
    async def generate(
        self,
        messages: list[Message],
        *,
        temperature: float | None = None,
        max_tokens: int | None = None,
        **kwargs: Any,
    ) -> str:
        temperature = temperature if temperature is not None else self._default_temperature
        max_tokens = max_tokens if max_tokens is not None else self._default_max_tokens

        body = [
            {"role": m.role, "content": m.content}
            for m in messages
        ]
        t0 = time.perf_counter()
        response = await asyncio.to_thread(
            _sync_create,
            self._client,
            self._model,
            body,
            temperature,
            max_tokens,
            **kwargs,
        )
        elapsed = time.perf_counter() - t0
        choice = response.choices[0] if response.choices else None
        text = (choice.message.content or "") if choice else ""
        usage = getattr(response, "usage", None)
        in_tokens = usage.prompt_tokens if usage else 0
        out_tokens = usage.completion_tokens if usage else 0
        logger.info(
            "llm_completion model=%s duration_sec=%.2f input_tokens=%s output_tokens=%s",
            self._model,
            elapsed,
            in_tokens,
            out_tokens,
        )
        return text
