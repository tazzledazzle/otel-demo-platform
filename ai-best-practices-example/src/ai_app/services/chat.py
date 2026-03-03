"""Chat service: builds messages with config-driven system prompt, calls LLM."""

from pathlib import Path

from ai_app.llm.base import BaseLLMClient, Message
from ai_app.prompts.loader import get_prompt


class ChatService:
    """Uses shared LLM client and prompt manager for chat."""

    def __init__(
        self,
        llm: BaseLLMClient,
        prompts_dir: Path,
        *,
        system_prompt_name: str = "chat_system",
        system_instructions: str | None = None,
    ) -> None:
        self._llm = llm
        self._prompts_dir = prompts_dir
        self._system_prompt_name = system_prompt_name
        self._system_instructions = system_instructions

    async def chat(self, user_message: str, history: list[Message] | None = None) -> str:
        """Single turn: optional history + user_message → assistant reply."""
        system_text = get_prompt(
            self._system_prompt_name,
            self._prompts_dir,
            instructions=self._system_instructions or "",
        )
        messages: list[Message] = [
            Message(role="system", content=system_text),
        ]
        if history:
            messages.extend(history)
        messages.append(Message(role="user", content=user_message))
        return await self._llm.generate(messages)

    async def chat_messages(self, messages: list[Message]) -> str:
        """Generate assistant reply for a full list of messages (e.g. with system)."""
        return await self._llm.generate(messages)
