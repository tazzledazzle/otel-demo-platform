"""
Minimal FastAPI app — Phase 1 foundation.
Two GET operations: root and /greeting with optional name.
"""
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    """Root endpoint. Returns a simple JSON message."""
    return {"message": "Hello World"}


@app.get("/greeting")
async def greeting(name: str = "World"):
    """Greeting endpoint. Optional query param `name` (default: World)."""
    return {"greeting": f"Hello, {name}!"}
