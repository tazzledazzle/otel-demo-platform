"""Embeddings via OpenAI-compatible API (Ollama or OpenAI)."""

from openai import OpenAI


def get_embeddings(
    client: OpenAI,
    model: str,
    texts: list[str],
) -> list[list[float]]:
    """Return embedding vectors for each text. Uses same base_url as chat."""
    if not texts:
        return []
    response = client.embeddings.create(model=model, input=texts)
    order = sorted(response.data, key=lambda d: d.index)
    return [order[i].embedding for i in range(len(order))]
