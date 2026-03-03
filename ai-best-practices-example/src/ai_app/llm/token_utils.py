"""Token counting: tiktoken when model is known, else simple fallback."""

import logging
from typing import Any

logger = logging.getLogger(__name__)

# Default encoding for unknown models (cl100k_base is used by many OpenAI-style models)
_FALLBACK_ENCODING = "cl100k_base"


def count_tokens(text: str, model: str | None = None) -> int:
    """
    Count tokens in text. Uses tiktoken for known encodings, else fallback.
    """
    try:
        import tiktoken
    except ImportError:
        return _fallback_count(text)

    encoding_name = _encoding_for_model(model)
    try:
        enc = tiktoken.get_encoding(encoding_name)
    except Exception:
        enc = tiktoken.get_encoding(_FALLBACK_ENCODING)
    return len(enc.encode(text))


def _encoding_for_model(model: str | None) -> str:
    """Map model name to tiktoken encoding where possible."""
    if not model:
        return _FALLBACK_ENCODING
    model_lower = model.lower()
    if "gpt-4" in model_lower or "gpt-3.5" in model_lower or "o1" in model_lower:
        return "cl100k_base"
    if "gpt-3" in model_lower:
        return "r50k_base"
    return _FALLBACK_ENCODING


def _fallback_count(text: str) -> int:
    """Rough token count: ~4 chars per token for English."""
    return max(1, len(text) // 4)


def count_message_tokens(messages: list[dict[str, Any]], model: str | None = None) -> int:
    """
    Approximate token count for a list of chat messages (OpenAI format).
    """
    try:
        import tiktoken
    except ImportError:
        total = sum(len(m.get("content", "") or "") for m in messages)
        return _fallback_count(total)

    enc = tiktoken.get_encoding(_encoding_for_model(model) if model else _FALLBACK_ENCODING)
    # OpenAI counting: per-message overhead
    overhead = 4  # approximate per message
    total = 0
    for m in messages:
        content = (m.get("content") or "") if isinstance(m.get("content"), str) else ""
        total += len(enc.encode(content)) + overhead
    return total
