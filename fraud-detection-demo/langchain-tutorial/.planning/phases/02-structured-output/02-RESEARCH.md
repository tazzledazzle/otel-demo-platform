# Phase 2: Structured output — Research

**Researched:** 2026-02-25  
**Domain:** LangChain Python — structured output (Pydantic / JSON) with LCEL  
**Confidence:** HIGH  

## Summary

Phase 2 adds one chain that returns **structured data** (Pydantic model or JSON) instead of plain text. The standard approach is to keep the same LCEL shape as Phase 1 (`prompt | llm | parser`) and swap `StrOutputParser` for **PydanticOutputParser** or **JsonOutputParser**. Both parsers work with **Ollama and OpenAI** (same providers as Phase 1). LangChain’s preferred modern API is **`with_structured_output()`** on the model, but **ChatOllama does not support it** (raises `NotImplementedError`); therefore the tutorial should use the **parser-based pattern** so one approach works for both providers. Prompt format must include **format instructions** (e.g. `parser.get_format_instructions()`) so the LLM outputs valid JSON matching the schema. No new dependencies are required beyond Phase 1 (pydantic is already transitive); one new script (e.g. `02_structured_chain.py`) keeps Phase 1 unchanged.

---

## PydanticOutputParser vs JsonOutputParser

### Relationship

- **PydanticOutputParser** extends **JsonOutputParser**. It first parses LLM output as JSON (using JsonOutputParser behavior), then validates and converts to the given Pydantic model instance. Both live in `langchain_core.output_parsers`.
- **JsonOutputParser** without a schema returns a raw **dict**. With `pydantic_object=SomeModel`, it validates JSON against that model and returns a **Pydantic instance** (same end result as PydanticOutputParser for the typed case).

### When to use which

| Parser | Use when | Return type | Pros |
|--------|----------|-------------|------|
| **PydanticOutputParser** | You want explicit “output is this Pydantic class” and clear parser semantics. | Pydantic instance | Clear intent, good errors, same format_instructions pattern. |
| **JsonOutputParser** (no schema) | You want raw JSON/dict with no validation. | `dict` | Minimal; no Pydantic required. |
| **JsonOutputParser(pydantic_object=X)** | You want a Pydantic instance but are fine using the JSON parser plus validation. | Pydantic instance | Same typed result as PydanticOutputParser; one fewer import if you already use JsonOutputParser. |

### Recommendation for Phase 2

- **Prefer PydanticOutputParser** for the tutorial: name matches goal (“structured output”), and it teaches the dedicated structured-output parser. One small Pydantic model (e.g. 2–4 fields: title, summary, tags) is enough.
- **JsonOutputParser(pydantic_object=Model)** is acceptable if the planner wants a single parser type across phases or minimal surface area; both yield a typed Pydantic object when a model is supplied.

---

## get_structured_output / with_structured_output patterns

### with_structured_output (model-level)

- **What:** `llm.with_structured_output(SomePydanticModel)` returns a runnable that calls the LLM and parses the response into an instance of the Pydantic model. No separate parser in the pipe; schema is bound to the model.
- **Docs:** LangChain recommends this as the preferred way to get structured output when the provider supports it.
- **Support:** **ChatOpenAI** (and other cloud chat models) support it. **ChatOllama does not** — calling `ChatOllama(...).with_structured_output(PydanticModel)` raises `NotImplementedError`.
- **Implication for Phase 2:** Phase 2 keeps “same provider as Phase 1” (Ollama default, OpenAI optional). Because Ollama is the default and does not support `with_structured_output`, the phase should **not** rely on it. Use the **parser-based chain** so one pattern works for both Ollama and OpenAI.

### Parser-based pattern (recommended for this phase)

- **What:** Build the chain as `prompt | llm | parser` (same as Phase 1), with `parser` = `PydanticOutputParser(pydantic_object=Model)` or `JsonOutputParser(pydantic_object=Model)`. The prompt must include format instructions so the LLM outputs valid JSON.
- **Why:** Works with **both** ChatOllama and ChatOpenAI; no provider-specific branching. Aligns with Phase 1 (learners only add a different parser and a Pydantic model).
- **Optional note for planner:** In a follow-up or README, the “OpenAI path” could mention `with_structured_output` as an alternative for that provider only; the main script should stay parser-based for consistency.

---

## Prompt format for structured output

### Format instructions

- Both **PydanticOutputParser** and **JsonOutputParser(pydantic_object=X)** expose **`get_format_instructions()`**, which returns a string describing the expected JSON shape (and, for Pydantic, field types/descriptions).
- This string **must** be included in the prompt so the LLM emits parseable JSON. Otherwise parsing fails or is unreliable.

### Where to put them

- **Option A — `partial_variables`:**  
  `PromptTemplate(..., partial_variables={"format_instructions": parser.get_format_instructions()})`  
  No extra input variable; format_instructions are fixed at chain build time.
- **Option B — Template placeholder:**  
  Include `{format_instructions}` in the template and pass `format_instructions=parser.get_format_instructions()` in `invoke()` (or via partial_variables).  
  Same idea; planner can choose either.

### Template shape

- Can use **ChatPromptTemplate** (system + human) like Phase 1, with one of the messages containing `{format_instructions}` and the user input (e.g. “Summarize the following and return title, summary, tags: {input}”).
- Or **PromptTemplate** with a single string that includes `{format_instructions}` and `{input}` (or `{query}`).  
  Both are valid; ChatPromptTemplate keeps consistency with `01_hello_chain.py`.

### Example (conceptual)

```python
parser = PydanticOutputParser(pydantic_object=Summary)
prompt = ChatPromptTemplate.from_messages([
    ("system", "You extract a short summary. Reply with JSON only."),
    ("human", "{format_instructions}\n\nUser request: {input}"),
])
# partial_variables so format_instructions are fixed
prompt = prompt.partial(format_instructions=parser.get_format_instructions())
chain = prompt | llm | parser
result = chain.invoke({"input": "Tell me about Python."})  # result is Pydantic instance
```

---

## Recommendations for planner

1. **Chain shape:** One chain: `prompt | llm | parser`. Same LCEL pattern as Phase 1; only the parser and prompt content change.
2. **Parser:** Prefer **PydanticOutputParser** with one small Pydantic model (e.g. title, summary, tags). **JsonOutputParser(pydantic_object=Model)** is acceptable and yields the same typed result.
3. **Provider:** Reuse Phase 1 setup: **ChatOllama** (default) and optional **ChatOpenAI**. No `with_structured_output` in the main script so Ollama works without branching.
4. **Prompt:** Use **format_instructions** from the chosen parser (`get_format_instructions()`) in the prompt (e.g. via `partial(format_instructions=...)` or `partial_variables`). Prefer **ChatPromptTemplate** for consistency with Phase 1.
5. **Artifact:** New script only (e.g. **02_structured_chain.py**). Do not change `01_hello_chain.py`. Same repo and requirements; add **pydantic** only if not already present (usually transitive from langchain).
6. **Scope:** No agents, no tools. One runnable script that invokes the chain and prints or uses the structured object (e.g. `print(result)` or `print(result.title)`).
7. **Schema:** One simple Pydantic model with a few described fields so the lesson stays focused and format_instructions stay short.

---

## Pitfalls

- **Omitting format_instructions:** LLM then returns free-form text; parsing fails or is flaky. Always inject `get_format_instructions()` into the prompt.
- **Using with_structured_output with Ollama:** ChatOllama does not implement it; use parser-based chain only.
- **Expecting dict from PydanticOutputParser:** It returns a Pydantic instance; document that learners get a typed object (e.g. `result.title`) not a raw dict (unless they use JsonOutputParser without `pydantic_object`).

---

## Dependencies

- **langchain**, **langchain-ollama** (and optionally **langchain-openai**) as in Phase 1.
- **pydantic** is typically already a dependency of langchain-core. If the planner adds an explicit Pydantic model, ensure pydantic is in the environment (add to requirements.txt only if missing).

---

## Sources

- LangChain: PydanticOutputParser and JsonOutputParser (langchain_core); `get_format_instructions()` usage.
- LangChain: “Structured output” / “how to return structured data”; recommendation for `with_structured_output` where supported.
- ChatOllama: does not support `with_structured_output` (NotImplementedError); Ollama path requires parser-based approach.
- Phase 1 research and 01_hello_chain.py: LCEL `prompt | llm | parser`, ChatOllama, ChatPromptTemplate.

---

## RESEARCH COMPLETE
