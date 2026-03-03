# Optional: for running the app service in Docker (e.g. FastAPI).
FROM python:3.11-slim

WORKDIR /app

# Install uv for fast installs
COPY pyproject.toml ./
RUN pip install --no-cache-dir uv && uv pip install --system -e .

COPY config/ ./config/
COPY src/ ./src/
COPY examples/ ./examples/

# Default: run chat CLI; override to run uvicorn for API
CMD ["python", "-m", "examples.chat_cli"]
