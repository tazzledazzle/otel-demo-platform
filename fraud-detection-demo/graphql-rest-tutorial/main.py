"""
Minimal FastAPI REST API — Phase 1.
Two GET operations: root and greeting (optional name query param).
Interactive docs at /docs.
"""
from fastapi import FastAPI

app = FastAPI(
    title="GraphQL & REST Tutorial API",
    description="Phase 1: minimal REST API with two GET endpoints.",
)


@app.get("/")
async def root() -> dict:
    """Root endpoint. Returns a simple JSON message."""
    return {"message": "Hello World"}


@app.get("/greeting")
async def greeting(name: str = "World") -> dict:
    """Greeting endpoint. Optional query param 'name' (default: World)."""
    return {"greeting": f"Hello, {name}!"}
