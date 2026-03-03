# Roadmap: langchain-tutorial

## Overview

Tutorial teaching LangChain: chains, agents, tools, and LLM app patterns. Phases TBD after research and requirement derivation.

## Milestones

- 📋 **v1.0** — TBD

## Phases

### Phase 1: Foundation — first chain
**Goal:** Learners run a minimal LangChain chain (prompt + LLM + output parser). One runnable script with Ollama as default; OpenAI optional. No agents or tools.
**Success Criteria:** One runnable example; clear env/setup; engineer-oriented.

**Plans:** 1 plan

Plans:
- [x] 01-01-PLAN.md — Project setup + runnable LCEL chain (executed)

### Phase 2: Structured output
**Goal:** Learners run a chain that returns structured data (e.g. Pydantic model or JSON) instead of plain text. Same provider/setup as Phase 1; add output parser (e.g. PydanticOutputParser or JsonOutputParser). No agents or tools.
**Success Criteria:** One runnable script or notebook that invokes a chain and gets a structured object; engineer-oriented.
**Depends on:** Phase 1

Plans:
- [ ] 02-01-PLAN.md — Structured-output chain (PydanticOutputParser, format_instructions, prompt | llm | parser)

## Progress

| Phase | Milestone | Plans | Status | Completed |
|-------|-----------|-------|--------|-----------|
| 1. Foundation | v1.0 | 1/1 | Complete | — |
| 2. Structured output | v1.0 | 1/1 | Not started | — |

---
*Initialized by GSD new-project workflow*
