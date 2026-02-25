# Phase 1: Runnable demo — Context

**Gathered:** 2025-02-24
**Status:** Ready for planning

## Phase Boundary

A full demo can be run from scratch: anyone can start infra (Temporal, Grafana otel-lgtm), start API, worker, and agent, confirm they are healthy, send a chat request with documented test data, and view one end-to-end trace in Grafana. This phase delivers the steps and test data so DOC-02 is satisfied.

## Implementation Decisions

### Where steps live
- **Single source of truth in repo:** Main README in `otel-demo-platform/` stays the primary entry; integration steps can live in README and/or `integration/README.md` with cross-links. No separate runbook in `.planning/` for this phase — keep everything in the app repo so reviewers clone one place.

### Test data
- **Canonical sample file + curl in docs:** Use existing `test-data/sample_requests.json` (e.g. "Hello", "What is 2 + 2?") as the documented examples. README/integration doc should show at least one full `curl` and point to `test-data/` for more. One happy-path focus is enough for "runnable demo"; optional error-case can be Phase 2 or later.

### Start order and verification
- **Order:** Infra first (docker compose), then agent (needs Ollama), then worker, then API — match current `integration/README.md`. Add an explicit **smoke check:** after starting each service (or after all four), document hitting health endpoints (e.g. `GET /health` for API and agent) so the reviewer can confirm each piece is up before sending chat.
- **Verification:** Success = one `curl` to `POST /chat` returns 200 with a reply, and one trace visible in Grafana spanning API → worker → agent.

### Grafana instructions
- **Short step-by-step:** Don’t assume Grafana familiarity. Document: open Grafana (e.g. http://localhost:3000), go to Explore → Tempo, how to run a search/query to find the trace (e.g. by service name or time range), and that they should see one trace with API, worker, and agent spans. No need for a custom dashboard in this phase — finding one trace is enough.

### Audience / prerequisites
- **Assume stack installed, link for Ollama:** Assume reviewer has JDK 17+, Python 3.11+, Docker and Docker Compose. Keep “Install Ollama and pull a model” in Prerequisites with a link (e.g. ollama.ai) and one model suggestion (e.g. llama3.2). No step-by-step OS-specific install for JDK/Python/Docker in this phase.

### Claude's Discretion
- Exact wording and section titles in README vs integration doc.
- Whether to add a one-line “Quick validation” section that lists all health URLs in one place.
- Minor reorder of bullets (e.g. “Send request” before “View traces” or vice versa) as long as dependencies are clear.

## Specific Ideas

- Existing `integration/README.md` and root `README.md` already have the right shape; this phase is about making them complete and consistent (health checks, test data pointer, Grafana steps) so a fresh clone can run the demo without guessing.

## Deferred Ideas

None — discussion stayed within phase scope.

---
*Phase: 01-runnable-demo*
*Context gathered: 2025-02-24*
