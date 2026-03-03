# Phase 2: Structured output — Context

**Gathered:** 2026-02-25
**Status:** Ready for planning

<domain>
## Phase Boundary

Learners run a chain that returns structured data (Pydantic model or JSON) instead of plain text. Same provider/setup as Phase 1; add an output parser (e.g. PydanticOutputParser or JsonOutputParser). No agents or tools. Success = one runnable script that invokes a chain and gets a structured object; engineer-oriented.

</domain>

<decisions>
## Implementation Decisions

### Parser type
- Prefer Pydantic model + PydanticOutputParser for type-safe, documented output. JsonOutputParser acceptable if planner prefers minimal deps.
- One simple schema (e.g. a few fields: title, summary, tags) so the lesson stays focused.

### Chain shape
- Single chain: prompt (that asks for structured output) | llm | parser. Builds on Phase 1 LCEL pattern.
- Reuse Phase 1 env (Ollama/OpenAI); no new providers.

### Artifact
- New script (e.g. 02_structured_chain.py) so Phase 1 script stays unchanged. Same repo, same requirements (add nothing beyond langchain + provider if parser is built-in).

### Claude's Discretion
- Exact Pydantic fields and prompt wording; whether to use get_structured_output() vs pipe with parser; example schema (e.g. "extract title and summary from this text").

</decisions>

<specifics>
## Specific Ideas

No specific references — open to standard LangChain structured-output patterns.

</specifics>

<deferred>
## Deferred Ideas

- Agents, tools, RAG, multi-step flows — later phases.

</deferred>

---
*Phase: 02-structured-output*
*Context gathered: 2026-02-25*
