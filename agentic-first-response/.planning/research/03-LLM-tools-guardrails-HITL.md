# Research: LLM Function Calling, Guardrails, and Human-in-the-Loop

**Domain:** LLM tool use; safety; incident response guardrails.  
**Consumed by:** Phase 4 (Triage Agent), Phase 5 (Tools), Phase 6 (Guardrails & Safety).

---

## Summary

Function calling is powerful for triage agents but introduces risk: LLMs can be manipulated into unsafe tool use. Defenses include tool allowlists, explicit human-in-the-loop (HITL) gates for high-risk actions, output validation (e.g. Pydantic), and dedicated guardrail components. For incident response, read-only observability tools by default and gating write actions (restart, scale, rollback) behind on-call approval is the right safety posture.

---

## Key Findings

### Function Calling Risks

- **2024 research:** Function calling can be highly susceptible to jailbreak-style misuse (e.g. coercing the model to call disallowed tools or with bad arguments), with high success rates across major models when safety filters are absent.
- **Mitigations:** Strict **allowlists** (only these tools, these parameters); **input/output validation** (Pydantic or similar on every LLM response); **defensive system prompts** and **security filters** specifically for tool use; **no direct execution** of write actions without an explicit approval step.

### Guardrail Patterns

- **GuardAgent-style pattern:** A separate guard agent or middleware checks whether the main agent’s intended actions satisfy safety policy before execution; reported high accuracy on policy adherence when given clear safety requirements.
- **Layered defenses:** Combine prompt-level instructions, schema enforcement, allowlists, and HITL for destructive or high-impact actions.
- **Moderation tools** (e.g. prompt/response safety, refusal rates) can complement tool-calling guardrails but do not replace allowlists and HITL for production systems.

### Human-in-the-Loop for Incident Response

- **HITL approval gate** for high-risk actions (restart pod, scale deployment, rollback) aligns with SRE practice: on-call confirms before execution.
- **Read-only by default:** `query_logs`, `get_pod_status`, `get_recent_deploys` (and similar) can be callable without approval; `suggest_remediation` returns a suggestion that is then gated.
- **Structured output** (`hypothesis`, `confidence`, `suggested_action`, `risk_level`) enables both automation (low-risk, well-defined suggestions) and human review (high-risk or ambiguous).

### Cost and Resource Controls

- **Token budget per triage session** and **max iteration limit** prevent runaway cost and infinite loops.
- Tracking usage in OpenTelemetry (token_count, model, duration) supports cost visibility and alerts when budgets are exceeded.

### Implications for This Project

- **Tool allowlist:** Only registered tools; no dynamic or user-defined tool execution.
- **Pydantic (or equivalent) validation** on every LLM response before any tool is invoked or suggestion is shown.
- **HITL gate:** All write/destructive actions require explicit on-call confirmation; design API and UI for “approve / reject / modify” workflow.
- **Model routing:** Use a capable model (e.g. Sonnet) for routine triage; escalate to a stronger model (e.g. Opus) for ambiguous cases, with clear criteria to avoid over-use.
- **Document** safety assumptions (allowlist, HITL, validation) in runbooks and postmortems so future changes preserve guardrails.

---

## References (from search)

- “The Dark Side of Function Calling: Pathways to Jailbreaking Large Language Models” (arXiv 2407.17915).
- “GuardAgent: Safeguard LLM Agents by a Guard Agent via Knowledge-Enabled Reasoning” (arXiv 2406.09187).
- Microsoft on discovering and mitigating attacks against AI guardrails.
- Snowflake Cortex Guard; WILDGUARD (open-source moderation).
