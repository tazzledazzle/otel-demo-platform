# Research: OpenTelemetry for LLM Agents and Observability

**Domain:** Distributed tracing; LLM/agent observability; SRE metrics.  
**Consumed by:** Phase 7 (Observability).

---

## Summary

OpenTelemetry is well-suited for agentic systems: a trace is a tree of spans (LLM calls, tool runs, agent turns) with a single trace ID. W3C Trace Context propagation ties alert → agent → tools → remediation. Semantic conventions for GenAI/agents are emerging; backends (Datadog, Jaeger, Honeycomb, etc.) consume OTel. Instrumentation can be manual (wrap agent loop, LLM, tools) or framework-based (e.g. OpenLIT, AG2); key is capturing model, token count, duration, and tool identity on every span.

---

## Key Findings

### Trace Model

- **Trace** = end-to-end request as a tree of **spans** sharing one trace ID.
- For triage: one trace per alert; child spans for agent loop iterations, each LLM call, each tool call, and (if applicable) remediation step.
- **Span kinds:** CLIENT for outbound LLM API calls; INTERNAL for agent reasoning and tool execution.

### Span Content for Triage Agent

- **LLM spans:** `model`, `token_count` (input/output), `duration_ms`, `tool_called` (which tool, if any), and optionally prompt/completion sampling for debugging.
- **Tool spans:** Tool name, arguments (redact secrets), result summary or status.
- **Agent turn spans:** Iteration number, hypothesis or decision summary, next action.
- **Root span:** Alert ID, source (PagerDuty/Datadog), service/alert type for filtering in dashboards.

### Propagation

- **W3C Trace Context** (traceparent/tracestate) propagated from alert ingestion through agent, tool clients, and any downstream services so the full path is one trace in the backend.
- Ensures “alert → agent → tool execution → remediation” is a single trace for SRE dashboards.

### Metrics

- **triage_duration_seconds** (histogram): time from alert received to first suggestion or escalation.
- **hypothesis_accuracy** (evaluated against postmortem when available): quality metric for tuning.
- **tool_call_success_rate** (success vs failure per tool): reliability of integrations.
- **Token/cost per triage session:** from span attributes or dedicated metrics for budget alerts.

### Backends and Frameworks

- OTel exports to **Datadog**, Jaeger, Grafana Tempo, Honeycomb, New Relic, etc.
- **OpenLIT** and **AG2** offer automatic or low-code instrumentation for LangChain, LlamaIndex, and other agent frameworks; custom instrumentation is still common for full control (e.g. Pydantic validation, HITL events as spans).

### Implications for This Project

- **Full OTel instrumentation** through the agent loop: one span per LLM call, per tool call, per agent turn.
- **Attributes:** `model`, `token_count`, `duration_ms`, `tool_called` on LLM spans; tool name and status on tool spans.
- **Propagate** W3C context from alert handler into agent and all tool clients.
- **Metrics:** triage_duration_seconds, hypothesis_accuracy (postmortem comparison), tool_call_success_rate; expose via OTel or existing metrics pipeline.
- **Dashboards:** In Datadog (or chosen backend), show agent performance alongside existing SRE metrics (error rate, latency, etc.) so on-call sees one place for “what the agent did” and “what the system did.”

---

## References (from search)

- AG2 OpenTelemetry Tracing for multi-agent systems; OneUptime tracing AI agents.
- Traceloop: Visualizing LLM performance with OTel (cost, latency).
- Agent Observability Standard (AOS) – extend OpenTelemetry.
- OpenLIT overview (auto-instrumentation).
