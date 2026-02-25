# Architecture

**Analysis Date:** 2025-02-24

**Scope:** `otel-demo-platform`

## Pattern Overview

**Overall:** Multi-service request-response with Temporal workflow orchestration and shared OpenTelemetry tracing.

**Key Characteristics:**
- API is the single HTTP entrypoint; workflow and agent are internal.
- Temporal provides durable workflow and activity execution; worker performs the only cross-service call (to the agent).
- All app services export OTLP traces and use W3C trace context propagation end-to-end.
- No containerization of app services; Docker is used for infrastructure (Temporal, PostgreSQL, Grafana otel-lgtm) only.

## Layers

**API (Kotlin):**
- Purpose: HTTP entrypoint; start workflow and return result.
- Location: `otel-demo-platform/api/src/main/kotlin/dev/otel/demo/api/`
- Contains: Main, routes (chat, health), plugins (routing, serialization), Temporal client factory, Telemetry, models.
- Depends on: contracts, Ktor, Temporal SDK, OpenTelemetry, Jackson.
- Used by: External clients (e.g. curl).

**Worker (Kotlin):**
- Purpose: Execute Temporal workflow and RunAgent activity; call agent over HTTP.
- Location: `otel-demo-platform/worker/src/main/kotlin/dev/otel/demo/worker/`
- Contains: Main, AgentWorkflowImpl, RunAgentActivity(Interface), client (AgentClient), Telemetry.
- Depends on: contracts, Temporal SDK, Ktor client, OpenTelemetry.
- Used by: Temporal (task queue).

**Agent (Python):**
- Purpose: LangChain pipeline (Ollama + stub tools); expose `POST /invoke`.
- Location: `otel-demo-platform/agent/agent/`
- Contains: main (FastAPI app), chain (LLM/tools), telemetry.
- Depends on: FastAPI, LangChain, langchain-ollama, OpenTelemetry.
- Used by: Worker (HTTP).

**Contracts (Kotlin):**
- Purpose: Shared Temporal workflow interface.
- Location: `otel-demo-platform/contracts/src/main/kotlin/dev/otel/demo/contracts/`
- Contains: `AgentWorkflow` (workflow interface).
- Depends on: Temporal SDK only.
- Used by: API (client stub), worker (implementation).

## Data Flow

**Chat request:**

1. Client sends `POST /chat` with `{"message":"..."}` to API.
2. API (`ChatRoutes.kt`) receives body, creates Temporal client via `TemporalClientFactory`, starts `AgentWorkflow` with task queue `agent-task-queue`, synchronously gets result.
3. Worker picks up workflow; `AgentWorkflowImpl` creates activity stub and calls `activity.run(message)`.
4. `RunAgentActivity` calls `agentInvoke(agentBaseUrl, message)` in `worker/.../client/AgentClient.kt` — HTTP `POST` to agent `/invoke` with `{"message": message}`.
5. Agent FastAPI `invoke` gets request, runs `app.state.agent.invoke({"input": req.message})` (LangChain chain), returns `InvokeResponse(reply=...)`.
6. Activity returns reply to workflow; API returns `ChatResponse(result)` to client.

**State Management:**
- No shared app state beyond Temporal workflow state. Agent holds executor in `app.state.agent` (lifespan).

## Key Abstractions

**AgentWorkflow:**
- Purpose: Durable orchestration; single method `run(message: String): String`.
- Examples: `contracts/src/main/kotlin/dev/otel/demo/contracts/AgentWorkflow.kt`, `worker/.../AgentWorkflowImpl.kt`, `api/.../TemporalClientFactory.kt` (stub).
- Pattern: Temporal workflow interface + impl; activity stub used inside workflow.

**RunAgentActivity(Interface):**
- Purpose: Single unit of work: call agent HTTP API.
- Examples: `worker/.../RunAgentActivityInterface.kt`, `worker/.../RunAgentActivity.kt`, `worker/.../client/AgentClient.kt`.
- Pattern: Activity interface + impl delegating to Ktor client; top-level `agentInvoke` in AgentClient.

**Telemetry (per service):**
- Purpose: Configure OTLP exporter and W3C propagator; register global.
- Examples: `api/.../Telemetry.kt`, `worker/.../Telemetry.kt`, `agent/agent/telemetry.py`.
- Pattern: Init at startup; API/worker use same Kotlin pattern; agent uses FastAPI instrumentor + manual setup.

## Entry Points

**API:**
- Location: `otel-demo-platform/api/src/main/kotlin/dev/otel/demo/api/Main.kt`
- Triggers: JVM main.
- Responsibilities: Init OTel, start Netty server on 8080, install serialization and routing (health + chat).

**Worker:**
- Location: `otel-demo-platform/worker/src/main/kotlin/dev/otel/demo/worker/Main.kt`
- Triggers: JVM main.
- Responsibilities: Init OTel, connect to Temporal, create worker for `agent-task-queue`, register workflow and activity, start factory, block.

**Agent:**
- Location: `otel-demo-platform/agent/agent/main.py` (`__main__` runs uvicorn).
- Triggers: `python -m agent.main` or uvicorn.
- Responsibilities: Setup OTel (if endpoint set), create FastAPI app with lifespan (load agent executor), instrument app, serve `/health` and `/invoke`.

## Error Handling

**Strategy:** Minimal explicit handling; failures propagate (Ktor/Temporal/FastAPI).

**Patterns:**
- API: No try/catch in chat route; Temporal or receive failures bubble to Ktor.
- Worker: Activity timeout 2 minutes (`AgentWorkflowImpl.kt`); no retry logic in `AgentClient`.
- Agent: FastAPI/Pydantic validation; no custom exception handlers.
- No global error handler or unified error response shape.

## Cross-Cutting Concerns

**Logging:** println in worker; otherwise no structured logging.

**Validation:** Pydantic for agent request/response; Kotlin data classes (ChatRequest/ChatResponse) with Jackson; no explicit validation beyond types.

**Authentication:** None.

---

*Architecture analysis: 2025-02-24*
