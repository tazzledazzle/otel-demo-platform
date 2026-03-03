"""Load and render prompt templates from YAML + Jinja2."""

import logging
from pathlib import Path
from typing import Any

import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape

logger = logging.getLogger(__name__)

_env: Environment | None = None
_registry: dict[str, dict[str, Any]] = {}


def _get_env(prompts_dir: Path) -> Environment:
    global _env
    if _env is None:
        _env = Environment(
            loader=FileSystemLoader(str(prompts_dir)),
            autoescape=select_autoescape(default=False),
        )
    return _env


def load_registry(prompts_dir: Path) -> dict[str, dict[str, Any]]:
    """Load prompts registry from prompts_dir (e.g. config/prompts)."""
    global _registry
    index_path = prompts_dir / "index.yaml"
    if not index_path.exists():
        _registry = {}
        return _registry
    with open(index_path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    _registry = data if isinstance(data, dict) else {}
    return _registry


def get_prompt(
    name: str,
    prompts_dir: Path,
    **variables: Any,
) -> str:
    """
    Get a prompt by name, render with optional variables.
    Caller must pass prompts_dir (e.g. from Settings().prompts_dir).
    """
    reg = load_registry(prompts_dir)
    entry = reg.get(name)
    if not entry:
        raise KeyError(f"Unknown prompt: {name}")

    env = _get_env(prompts_dir)
    template_name = entry.get("template") or entry.get("path") or f"{name}.jinja2"
    if not template_name.endswith((".jinja2", ".j2", ".txt")):
        template_name = f"{template_name}.jinja2"
    try:
        template = env.get_template(template_name)
    except Exception:
        template = env.get_template(f"{name}.jinja2")
    return template.render(**variables).strip()
