"""Abstract LLM client interface (provider-agnostic)."""

from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel


class Message(BaseModel):
    """Chat message with role and content."""

    role: str  # "system", "user", "assistant"
    content: str


class BaseLLMClient(ABC):
    """Abstract interface for LLM generation."""

    @abstractmethod
    async def generate(
        self,
        messages: list[Message],
        *,
        temperature: float | None = None,
        max_tokens: int | None = None,
        **kwargs: Any,
    ) -> str:
        """Generate a completion from messages. Returns assistant text only."""
        ...
