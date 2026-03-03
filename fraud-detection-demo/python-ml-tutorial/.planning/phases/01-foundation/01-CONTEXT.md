# Phase 1: Foundation — Context

**Gathered:** 2026-02-25
**Status:** Ready for planning

<domain>
## Phase Boundary

Deliver a runnable Python/ML environment and one end-to-end lesson: train and evaluate a model on a small dataset. Setup, code-first flow, minimal theory. No deployment or production concerns in this phase.

</domain>

<decisions>
## Implementation Decisions

### Lesson format
- One primary artifact: script or notebook (TBD by research/planner).
- Engineer-oriented: code-first, minimal conceptual preamble.
- Prerequisites stated clearly (Python version, venv, install steps).

### Scope of first model
- Single small dataset (e.g. built-in or one CSV); no data pipeline.
- Train + evaluate only; no hyperparameter tuning or comparison in Phase 1.
- Success = runnable end-to-end; metrics (e.g. accuracy) shown.

### Setup and run experience
- Single-command or minimal-step run (e.g. `pip install -r requirements.txt && python train.py` or notebook run-all).
- No cloud or GPU required; local-only for Phase 1.

### Claude's Discretion
- Exact dataset choice; notebook vs script; output format (print vs file).
- Whether to include a tiny "what we did" summary in the lesson.

</decisions>

<specifics>
## Specific Ideas

No specific references — open to standard approaches (e.g. scikit-learn iris or similar).

</specifics>

<deferred>
## Deferred Ideas

- Deployment, production patterns, or ML ops — later phases.
- Deep learning (PyTorch/TensorFlow) — later phase or optional extension.

</deferred>

---
*Phase: 01-foundation*
*Context gathered: 2026-02-25*
