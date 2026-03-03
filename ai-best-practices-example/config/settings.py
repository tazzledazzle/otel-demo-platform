"""Application settings via Pydantic Settings (env + .env)."""

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


def _config_dir() -> Path:
    return Path(__file__).resolve().parent


class Settings(BaseSettings):
    """Single source of truth for configuration; no secrets in code."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # LLM provider (OpenAI-compatible, including Ollama)
    openai_api_key: str = "placeholder"
    llm_base_url: str = "http://localhost:11434/v1"
    llm_model: str = "llama3.2:3b"
    temperature: float = 0.7
    max_tokens: int = 1024

    # Paths
    config_root: Path = _config_dir()
    prompts_dir: Path = _config_dir() / "prompts"

    def model_dump_public(self) -> dict:
        """For logging: model, base_url (no keys)."""
        return {
            "llm_model": self.llm_model,
            "llm_base_url": self.llm_base_url,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }
