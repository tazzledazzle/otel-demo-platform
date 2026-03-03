# otel-demo-platform — one-command bootstrap
# Run from repo root. Ports: API 8080, Agent 8000 (override with API_PORT/AGENT_PORT before make run).
# See CONFIG.md for all env vars.

.PHONY: infra up-infra run-agent run-worker run-api run smoke e2e-smoke

# Start infrastructure (Temporal, Grafana otel-lgtm). Use "docker compose" for compatibility.
infra up-infra:
	docker compose up -d

# Start Agent in foreground (for debugging). Install deps first: cd agent && pip install -e ".[dev]"
run-agent:
	cd agent && python -m agent.main

# Start Worker from repo root.
run-worker:
	./gradlew :worker:run

# Start API from repo root.
run-api:
	./gradlew :api:run

# One-command start: infra, then Agent (bg), Worker (bg), API (fg). Ctrl+C stops API; Agent/Worker keep running.
run: infra
	@echo "Starting Agent in background..."
	@(cd agent && python -m agent.main > ../.agent.log 2>&1) & echo $$! > .agent.pid; sleep 3
	@echo "Starting Worker in background..."
	@./gradlew :worker:run > .worker.log 2>&1 & echo $$! > .worker.pid; sleep 5
	@echo "Starting API in foreground (Ctrl+C to stop API only). API: http://localhost:8080, Agent: http://localhost:8000"
	@./gradlew :api:run

# E2E smoke: bring up infra, start apps in background, wait, then curl health + POST /chat.
# Used by CI. Override ports via API_PORT/AGENT_PORT if needed.
e2e-smoke smoke: infra
	@echo "Waiting for infra (Temporal, otel-lgtm)..."
	@sleep 15
	@echo "Starting Agent..."
	@(cd agent && python -m agent.main > ../.agent.log 2>&1) & echo $$! > .agent.pid; sleep 5
	@echo "Starting Worker..."
	@./gradlew :worker:run --no-daemon > .worker.log 2>&1 & echo $$! > .worker.pid; sleep 8
	@echo "Starting API..."
	@./gradlew :api:run --no-daemon > .api.log 2>&1 & echo $$! > .api.pid; sleep 5
	@echo "Smoke: GET /health..."
	@curl -sf http://localhost:8080/health | grep -q "ok" || (echo "Health check failed"; exit 1)
	@echo "Smoke: POST /chat..."
	@curl -sf -X POST http://localhost:8080/chat -H "Content-Type: application/json" -d '{"message":"Hello"}' | grep -q "reply" || (echo "POST /chat failed or no reply"; exit 1)
	@echo "Smoke passed."
