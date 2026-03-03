# Research: ReAct Pattern for Incident Triage

**Domain:** Agentic incident response; runbook automation; root cause analysis.  
**Consumed by:** Phase 4 (Triage Agent), Phase 5 (Tools), roadmap decisions.

---

## Summary

ReAct (Reasoning + Acting) is a thought–action–observation loop: the LLM reasons about the next step, executes a tool, observes the result, and repeats. It fits incident triage where the environment is partially observable and steps are dependent (diagnose → fetch logs → re-evaluate). Recent work shows multi-agent orchestration can yield far higher action specificity and correctness than single-agent baselines when tuned for deterministic, auditable outputs.

---

## Key Findings

### ReAct Fit for Incident Response

- **When to use ReAct for triage:** Partially observable environments; multiple dependent steps (e.g. fetch runbook → query logs → form hypothesis); coordination of multiple tools/APIs; need for transparent reasoning traces for auditing and postmortems.
- **When not to use:** Unreliable or poorly specified tools; high-risk actions without strong governance; strict sub-500ms latency requirements; simple single-step queries.

### Single-Agent vs Multi-Agent

- Multi-agent orchestration for incident response has been shown to achieve **100% actionable recommendation rate** vs **~1.7%** for single-agent in some benchmarks.
- **Action specificity** can be orders of magnitude higher (e.g. “rollback auth-service to v2.3.0” vs “investigate recent changes”).
- **Correctness** (alignment with validated solutions) and **determinism** (zero variance across trials) support SLAs and repeatable triage.
- Latency is similar (~40s) for single vs multi-agent in studied setups; gains are in quality and specificity, not raw speed.

### Root Cause Analysis with Retrieval

- ReAct agents with **retrieval tools** (e.g. runbook/postmortem search) have been shown to perform competitively on production incidents with **higher factual accuracy** than baselines when they use the same diagnostic services that operations teams use.
- Transparent reasoning traces support auditing and post-incident review (hypothesis_accuracy metrics, alignment with postmortem).

### Implications for This Project

- **Single ReAct agent** with RAG + tools is a reasonable default; multi-agent can be a later evolution if determinism and action specificity need to be pushed further.
- Enforce **max iteration limit** (e.g. 10) and **tool allowlist** to avoid runaway loops and unsafe actions.
- Design for **auditability**: every LLM turn and tool call should be traceable (aligns with OTel phase).
- Do not promise sub-500ms triage; target “first useful response” in tens of seconds and document latency in observability.

---

## References (from search)

- ReAct agent pattern (agent-patterns.readthedocs.io, Playbook Atlas).
- “Multi-Agent LLM Orchestration Achieves Deterministic, High-Quality Decision Support for Incident Response” (arXiv 2511.15755).
- LLM-based agents for root cause analysis with retrieval (arXiv 2403.04123).
- NVIDIA Agentiq ReAct Agent documentation.
