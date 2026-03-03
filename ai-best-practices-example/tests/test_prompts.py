"""Unit tests for prompt loader."""

from pathlib import Path

import pytest

from ai_app.prompts.loader import get_prompt, load_registry


def test_load_registry_empty_dir(tmp_path: Path) -> None:
    reg = load_registry(tmp_path)
    assert reg == {}


def test_load_registry_with_index(prompts_dir: Path) -> None:
    reg = load_registry(prompts_dir)
    assert "chat_system" in reg
    assert reg["chat_system"].get("template") == "chat_system.jinja2"


def test_get_prompt_chat_system(prompts_dir: Path) -> None:
    text = get_prompt("chat_system", prompts_dir, instructions="Be brief.")
    assert "test assistant" in text
    assert "Be brief" in text


def test_get_prompt_rag_qa(prompts_dir: Path) -> None:
    text = get_prompt(
        "rag_qa",
        prompts_dir,
        context="Some context.",
        question="What is it?",
    )
    assert "Some context" in text
    assert "What is it?" in text


def test_get_prompt_unknown_raises(prompts_dir: Path) -> None:
    with pytest.raises(KeyError, match="Unknown prompt"):
        get_prompt("nonexistent", prompts_dir)
