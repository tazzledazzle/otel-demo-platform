# Phase 1: Foundation — Research

**Researched:** 2026-02-25
**Domain:** LangChain Python — minimal LCEL chain (prompt + LLM + optional output parser)
**Confidence:** HIGH

## Summary

Phase 1 is a single runnable LangChain chain: prompt template → LLM → optional output parser. The standard approach is **LCEL** (LangChain Expression Language): compose with the pipe operator (`|`), use `.invoke()` to run. Provider is either **OpenAI** (API key, cloud) or **Ollama** (local, no key). Both are first-class; Ollama is simpler for “run and see output” with no signup. Use **StrOutputParser** for plain text or **JsonOutputParser**/Pydantic for structured output. One script or one notebook is sufficient; docs lean toward notebooks for learning. Prerequisites: Python 3.10+, `pip install langchain langchain-openai` or `langchain-ollama`, and either `OPENAI_API_KEY` or a running Ollama + pulled model.

**Primary recommendation:** Implement one LCEL chain (`prompt | llm | parser`) with one provider (recommend Ollama for zero-setup or OpenAI for cloud); document env and run steps; success = learner runs the file and sees LLM output.

<user_constraints>

## User Constraints (from CONTEXT.md)

### Locked Decisions
- Single chain only: prompt template, LLM call, optional parsing (e.g. structured output). No retrieval, tools, or agent loop in Phase 1.
- Clear env/setup (e.g. API key or local model); one runnable script or notebook. Success = learner runs and sees LLM output (or parsed result).
- Code-first; minimal theory. Prerequisites stated (Python version, install, env vars).

### Claude's Discretion
- LLM provider; prompt example; output format (plain text vs structured); notebook vs script.

### Deferred Ideas (OUT OF SCOPE)
- Agents, tools, RAG, multi-step flows — later phases.

</user_constraints>

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| langchain | latest (pip -U) | Chains, prompts, base abstractions | Official meta-package; pulls langchain-core. Python 3.10+ required. |
| langchain-core | (transitive) | Runnables, LCEL, prompts, output parsers | All LCEL chains use core runnables and parsers. |
| langchain-openai | latest | ChatOpenAI | Official OpenAI integration; standard for cloud. |
| **or** langchain-ollama | latest | ChatOllama | Official Ollama integration; no API key; local. |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| pydantic | (transitive) | Structured output schemas | When using JsonOutputParser with a Pydantic model. |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| langchain-openai | langchain-anthropic, etc. | Phase 1 only needs one provider; OpenAI/Ollama cover cloud + local. |
| ChatOllama (langchain-ollama) | langchain_community ChatOllama | Official docs use `langchain_ollama`; community is legacy. |

**Installation (pick one provider):**

```bash
# Minimal for OpenAI
pip install -U langchain langchain-openai

# Minimal for Ollama (local)
pip install -U langchain langchain-ollama
```

Python 3.10+ required (per official install docs).

## Architecture Patterns

### Recommended Project Structure
```
langchain-tutorial/
├── .planning/
├── requirements.txt     # langchain, langchain-openai OR langchain-ollama
├── .env.example         # OPENAI_API_KEY=... or instructions for Ollama
└── 01_hello_chain.py    # or 01_hello_chain.ipynb
```

Single file for Phase 1 is sufficient; no multi-module layout required.

### Pattern 1: LCEL chain (prompt | LLM | parser)
**What:** Compose a prompt template, a chat model, and an output parser with the pipe operator. Each step is a Runnable; the chain supports `.invoke()`, `.stream()`, `.batch()`, and async variants.
**When to use:** Every Phase 1 runnable — this is the minimal chain.
**Example (plain text output):**
```python
# Source: LangChain docs (Ollama integration, LCEL patterns)
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Answer briefly."),
    ("human", "{question}"),
])
llm = ChatOllama(model="llama3.1", temperature=0)
chain = prompt | llm | StrOutputParser()
result = chain.invoke({"question": "What is 2+2?"})
print(result)
```

### Pattern 2: Optional structured output (parser with Pydantic)
**What:** Use a Pydantic model and JsonOutputParser (or PydanticOutputParser) so the LLM output is parsed into a typed object. Inject format instructions into the prompt.
**When to use:** When “output format” discretion chooses structured over plain text.
**Example:**
```python
# Source: WebSearch-verified LCEL + parser pattern
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field

class Answer(BaseModel):
    value: str = Field(description="short answer")

parser = JsonOutputParser(pydantic_object=Answer)
llm = ChatOllama(model="llama3.1", temperature=0)
prompt = PromptTemplate(
    template="Answer the question. {format_instructions}\nQuestion: {question}\n",
    input_variables=["question"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)
chain = prompt | llm | parser
result = chain.invoke({"question": "What is 2+2?"})
print(result)  # e.g. {"value": "4"}
```

### Anti-Patterns to Avoid
- **Using agents/tools in Phase 1:** CONTEXT defers agents and tools; use only a single LCEL chain.
- **Hand-rolling HTTP calls to OpenAI/Ollama:** Use `langchain-openai` or `langchain-ollama`; they handle messages, retries, and streaming.
- **Mixing sync and async incorrectly:** Use `chain.invoke()` in sync code; use `await chain.ainvoke()` only in async functions. Do not call `ainvoke` from sync context without an event loop.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Calling OpenAI/Ollama API | Raw requests or custom client | ChatOpenAI / ChatOllama | Correct message format, retries, token counting, streaming. |
| Parsing LLM text to structure | Regex or manual JSON parse | JsonOutputParser / PydanticOutputParser | Handles malformed output, format instructions, and validation. |
| Composing steps manually | Custom “chain” class or function glue | LCEL `prompt \| llm \| parser` | Automatic async, streaming, batching, and LangSmith tracing. |

**Key insight:** LangChain’s value here is a single Runnable interface and correct integration with each provider; hand-rolling loses that and introduces edge-case bugs.

## Common Pitfalls

### Pitfall 1: Missing or wrong env / local setup
**What goes wrong:** `OPENAI_API_KEY` not set or Ollama not running / model not pulled → cryptic auth or connection errors.
**Why it happens:** Learners assume “run the script” is enough without reading setup.
**How to avoid:** In prerequisites: (1) Python 3.10+, (2) `pip install` command, (3) “For OpenAI: set OPENAI_API_KEY” or “For Ollama: install Ollama, run `ollama pull llama3.1`”. One clear path per provider.
**Warning signs:** Script fails on first `invoke()` with auth/connection errors.

### Pitfall 2: Using deprecated ChatOllama import
**What goes wrong:** `from langchain_community.chat_models import ChatOllama` may still work but is not the current recommended path.
**Why it happens:** Old tutorials and docs reference langchain_community.
**How to avoid:** Use `from langchain_ollama import ChatOllama` and `pip install langchain-ollama` (per current LangChain Ollama integration docs).
**Warning signs:** Import errors or deprecation warnings when using community package.

### Pitfall 3: ainvoke in sync context
**What goes wrong:** Calling `await chain.ainvoke(...)` from a non-async script, or mixing sync/async incorrectly, leads to runtime errors.
**Why it happens:** LCEL supports both sync and async; using the wrong one in the wrong context fails.
**How to avoid:** In a single runnable script, use `chain.invoke(...)`. Reserve `ainvoke` for async apps or notebooks with async runtimes.
**Warning signs:** “coroutine was never awaited” or event-loop errors.

### Pitfall 4: No output parser when expecting a string
**What goes wrong:** Without a parser, `chain.invoke()` returns an `AIMessage`; learners expecting “just text” get an object and may not know to use `.content`.
**How to avoid:** End the chain with `StrOutputParser()` so `invoke()` returns a plain string. Document that omitting the parser returns a message object.
**Warning signs:** Printed output shows `<AIMessage ...>` instead of the reply text.

## Code Examples

Verified patterns from official/current sources:

### Minimal chain (Ollama, plain text)
```python
# Source: python.langchain.com (Ollama integration)
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOllama(model="llama3.1", temperature=0)
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("human", "{input}"),
])
chain = prompt | llm | StrOutputParser()
print(chain.invoke({"input": "Say hello in one sentence."}))
```

### Minimal chain (OpenAI, plain text)
```python
# Source: LangChain install + LCEL patterns
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Requires OPENAI_API_KEY in env
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("human", "{input}"),
])
chain = prompt | llm | StrOutputParser()
print(chain.invoke({"input": "Say hello in one sentence."}))
```

### Optional: Structured output (Pydantic + JsonOutputParser)
```python
# Source: WebSearch-verified LCEL + JsonOutputParser
from pydantic import BaseModel, Field
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_ollama import ChatOllama

class Joke(BaseModel):
    setup: str = Field(description="question to set up a joke")
    punchline: str = Field(description="answer to resolve the joke")

parser = JsonOutputParser(pydantic_object=Joke)
llm = ChatOllama(model="llama3.1", temperature=0)
prompt = PromptTemplate(
    template="Tell a short joke.\n{format_instructions}\n",
    input_variables=[],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)
chain = prompt | llm | parser
print(chain.invoke({}))
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Legacy Chain class | LCEL with `\|` and Runnables | LCEL became default | Use pipe composition; avoid deprecated Chain subclasses. |
| langchain_community ChatOllama | langchain_ollama.ChatOllama | Package split | Prefer `langchain-ollama` for new code. |
| Manual message building for chat | ChatPromptTemplate.from_messages | Standardized | Use template with system/human placeholders. |

**Deprecated/outdated:**
- Building Phase 1 around `create_agent` or tools: CONTEXT defers agents; use a single LCEL chain only.

## Open Questions

1. **Notebook vs script**
   - What we know: Docs recommend notebooks for learning; both work with LCEL.
   - What’s unclear: None for Phase 1 — planner can choose one and state it in prerequisites.
   - Recommendation: Pick one (e.g. single `.py` script for simplicity, or `.ipynb` if targeting notebook-first learners); document in setup.

2. **Default provider**
   - What we know: Ollama needs no API key; OpenAI needs OPENAI_API_KEY. Both are documented and supported.
   - What’s unclear: Which to make the “default” in the tutorial.
   - Recommendation: Planner chooses one as default (e.g. Ollama for zero signup) and optionally add a short “Using OpenAI instead” subsection with env and import swap.

## Sources

### Primary (HIGH confidence)
- https://python.langchain.com/docs/integrations/chat/ollama/ — ChatOllama setup, `langchain-ollama`, StrOutputParser in chain, Python 3.10+
- https://docs.langchain.com/oss/python/langchain/install — `pip install langchain` + provider packages, Python 3.10+

### Secondary (MEDIUM confidence)
- WebSearch: LCEL minimal chain (prompt | model | parser), JsonOutputParser/Pydantic, ChatPromptTemplate pipe to LLM — multiple results aligned with official patterns.
- WebSearch: OpenAI vs Ollama setup, ainvoke/sync pitfalls — verified against docs and Stack Overflow.

### Tertiary (LOW confidence)
- WebSearch: “notebook vs script” — docs favor notebooks for learning; no hard requirement for Phase 1.

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — official install and integration docs, current package names.
- Architecture: HIGH — LCEL and pipe pattern are standard; Ollama doc shows same pattern.
- Pitfalls: MEDIUM — ainvoke and parser behavior verified; community vs ollama package from docs.

**Research date:** 2026-02-25
**Valid until:** ~30 days (stack is stable; re-check if LangChain releases major LCEL or package changes).

---

## RESEARCH COMPLETE

**Phase:** 1 - Foundation
**Confidence:** HIGH

### Key Findings
- One runnable chain = LCEL: `prompt | llm | parser`; use `StrOutputParser` for plain text or `JsonOutputParser`/Pydantic for structured.
- Two supported provider paths: **OpenAI** (`langchain-openai`, `OPENAI_API_KEY`) and **Ollama** (`langchain-ollama`, local, no key); recommend one as default and document the other as optional.
- Prerequisites: Python 3.10+, `pip install langchain` + one of `langchain-openai` or `langchain-ollama`; env or Ollama setup must be explicit so “run and see output” works.
- Planner has discretion on: default provider, prompt example, plain vs structured output, and notebook vs script; research supports either choice.

### File Created
`langchain-tutorial/.planning/phases/01-foundation/01-RESEARCH.md`

### Confidence Assessment
| Area | Level | Reason |
|------|-------|--------|
| Standard Stack | HIGH | Official install and integration docs; package names and imports verified. |
| Architecture | HIGH | LCEL pipe pattern and parser usage confirmed from Ollama and general LCEL docs. |
| Pitfalls | MEDIUM | Documented from docs + community reports; ainvoke/parser verified. |

### Open Questions
- None blocking. Notebook vs script and default provider are left to planner per CONTEXT.

### Ready for Planning
Research complete. Planner can create PLAN.md and tasks for one runnable LCEL chain, prerequisites, and provider/env setup.
