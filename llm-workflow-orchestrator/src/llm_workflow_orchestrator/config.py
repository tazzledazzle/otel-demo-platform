"""Configuration from environment."""

import os


def get_temporal_host() -> str:
    return os.getenv("TEMPORAL_HOST", "localhost:7233")


def get_temporal_task_queue() -> str:
    return os.getenv("TEMPORAL_TASK_QUEUE", "llm-workflow-queue")


def get_llm_base_url() -> str:
    return os.getenv("LLM_BASE_URL", "https://api.openai.com/v1")


def get_llm_api_key() -> str:
    return os.getenv("LLM_API_KEY", "")


def get_llm_model() -> str:
    return os.getenv("LLM_MODEL", "gpt-4o-mini")


def get_otlp_endpoint() -> str:
    return os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4317")
