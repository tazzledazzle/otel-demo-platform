#!/usr/bin/env python3
"""Simple chat CLI: read user input → build messages → call service → print reply."""

import asyncio
import sys
from pathlib import Path

# Ensure project root is on path so config and ai_app are resolvable
_root = Path(__file__).resolve().parent.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from config.settings import Settings
from ai_app.llm.openai_compat import OpenAICompatClient
from ai_app.services.chat import ChatService


async def main() -> None:
    settings = Settings()
    client = OpenAICompatClient(
        base_url=settings.llm_base_url,
        api_key=settings.openai_api_key,
        model=settings.llm_model,
        default_temperature=settings.temperature,
        default_max_tokens=settings.max_tokens,
    )
    service = ChatService(client, settings.prompts_dir)
    print("Chat (Ctrl+C or empty line to exit). Config:", settings.model_dump_public())
    while True:
        try:
            line = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not line:
            break
        reply = await service.chat(line)
        print("Assistant:", reply)
        print()
    print("Bye.")


if __name__ == "__main__":
    asyncio.run(main())
