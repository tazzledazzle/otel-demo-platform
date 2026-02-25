# Live-Coding: New Pipeline Step (Python Agent)

Use this as a step-by-step fallback for the "implement a new feature" segment (~20 min). See **INTERVIEW_SCRIPT.md** block 7 for timing.

## Where it fits

1. **Request path:** API → Worker → RunAgent activity → Agent `POST /invoke` → LangChain pipeline (`agent/agent/chain.py`). See **ARCHITECTURE.md** for the full request path.

2. **Pipeline location:** The new step is added inside the **Python agent** pipeline in `agent/agent/chain.py`: either a new tool in the tools list (invoked by the executor when using a tool-calling agent) or a new runnable step in the chain (e.g. `prompt | llm | new_step`).

3. **Observability:** New span(s) from the new step appear in the same trace in Grafana (Tempo) under the agent service, so you can show end-to-end visibility after the change.

---

## Goal

Add one new step in the Python agent that appears as new span(s) in Grafana.

## Option A: New tool (e.g. `get_weather`)

1. **Add the tool** in `agent/agent/chain.py`:
   - Define a new `@tool` function, e.g. `get_weather(location: str) -> str` that returns a fixed string (e.g. `"Sunny, 72°F"`).
   - Add it to the `tools` list passed to the executor (if you switch back to a tool-calling agent) or keep the current simple chain and add the tool for a future agent step.

2. **Wire it into the pipeline** — If using the minimal chain (prompt | llm), you can add a second tool as a stub and document that the next step would be to use `create_tool_calling_agent` with `[search, get_weather]` so the model can call it. For a quick demo, adding the tool and a unit test that the tool exists is enough.

3. **Add a test** in `agent/tests/test_chain.py`: e.g. `test_get_weather_tool()` that calls the new tool and asserts the return value.

4. **Run** the agent, send a request, open Grafana and show the trace (and new span if the tool is invoked).

**Where it fits in the pipeline:** Option A fits as a **tool invoked by the executor** when the agent uses tool-calling; the new tool is registered alongside existing tools and appears as a span when called.

## Option B: New chain step (e.g. "summarize")

1. **Add a runnable step** in `agent/agent/chain.py` that runs after the LLM (e.g. a lambda or a small function that takes the LLM output and returns it or a short summary).
2. **Compose the chain**: e.g. `prompt | llm | summarize_step`.
3. **Add a test** that the chain output still has `output` and (optionally) contains expected text.
4. **Run** and show the new span in Grafana.

**Where it fits in the pipeline:** Option B fits as an **extra runnable after the LLM** in the chain; the new step is a link in `prompt | llm | new_step` and produces its own span in the same trace.

## Suggested order for the 20 min

1. Add the new tool or step in code (5 min).
2. Add a short pytest (3 min).
3. Run tests (1 min).
4. Start the stack and send one request (3 min).
5. Open Grafana and show the new span (5 min).
6. Buffer for questions (3 min).
