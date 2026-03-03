# Phase 1: Foundation — Research

**Researched:** 2026-02-25
**Domain:** Offline feature pipelines (definition, computation, write to file/store)
**Confidence:** HIGH

## Summary

Phase 1 needs one runnable feature pipeline with clear separation of feature definition and computation, writing to a file or minimal store. Research compared **Feast**, **custom Python (pandas + modules)**, and **Tecton**. **Feast** is the best fit: it provides a standard definition layer (Entity, FeatureView, FileSource), a single-command apply step, and retrieval APIs that naturally separate “what” from “how.” Output can be “minimal store” (Feast’s file-based offline store + optional SQLite online store) or “file” (e.g. `get_historical_features(...).to_df().to_parquet(...)`). Tecton requires cloud login and is oriented toward production; for a single runnable example with no production server, it is a poor fit. A custom pipeline (pandas + one module for “definitions” and one for “compute”) is possible and keeps dependencies minimal, but it does not teach feature-store concepts or set up later phases (versioning, backfills) as cleanly as Feast.

**Primary recommendation:** Use Feast with a local feature repo: Python feature definitions in one module, `feast apply` to register, and a single script or notebook that builds an entity DataFrame, calls `get_historical_features`, and writes the result to Parquet (or relies on the file offline store). Omit or minimize online store usage in Phase 1 so “output = file or minimal store” is satisfied.

<user_constraints>

## User Constraints (from CONTEXT.md)

### Locked Decisions
- One runnable example (script or notebook); engineer-oriented, code-first.
- Feature definition and computation steps clearly separated in the lesson.
- Write computed features to a file or minimal store (no production feature server in Phase 1).
- Single run end-to-end; no scheduling or backfill automation in Phase 1.
- Small, synthetic or built-in dataset; no real data pipeline or versioning yet.
- Success = learner runs the pipeline and sees features produced.

### Claude's Discretion
- Exact tooling (Feast, Tecton, or custom); language (Python typical); output format (Parquet, CSV, or store API).

### Deferred Ideas (OUT OF SCOPE)
- Online serving, versioning, backfills, production stores — later phases.

</user_constraints>

## Standard Stack

### Core
| Library   | Version      | Purpose | Why Standard |
|----------|--------------|---------|--------------|
| Python   | 3.9+         | Runtime | Feast supports 3.9+; tutorial audience standard. |
| feast    | latest (PyPI)| Feature definitions, registry, offline/online stores, retrieval | De facto OSS feature store; local file + SQLite setup; clear definition vs compute. |
| pandas   | (via feast)  | Entity DataFrame, optional transforms | Required by Feast for entity_df and on-demand views. |
| pyarrow  | (via feast)  | Parquet I/O | Used by Feast file offline store and for writing output. |

### Supporting
| Library | Purpose | When to Use |
|---------|---------|-------------|
| (none)  | —       | Phase 1 is minimal; no extra deps. |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Feast      | Custom (pandas + modules) | Custom: fewer deps, no feature-store concepts; later phases (versioning, backfills) don’t map to a real store. |
| Feast      | Tecton    | Tecton requires login (e.g. explore.tecton.ai) and is cloud-oriented; not ideal for “one runnable example” with no production server. |

**Installation:**
```bash
pip install feast
# pandas/pyarrow pulled in as dependencies
```

## Architecture Patterns

### Recommended Project Structure
```
feature-pipelines-tutorial/
├── .planning/                    # existing GSD planning
├── feature_repo/                 # Feast repo (or repo at repo root)
│   ├── feature_store.yaml        # registry path, provider local, offline_store type file
│   ├── feature_definitions.py    # Entity, FileSource, FeatureView(s)
│   ├── data/                     # small synthetic Parquet (e.g. driver_stats.parquet)
│   └── run_pipeline.py           # load store, get_historical_features, write to Parquet
├── requirements.txt              # feast
└── README.md                     # how to run (feast apply, then python run_pipeline.py)
```

Learner flow: (1) Inspect `feature_definitions.py` (definition), (2) Run `feast apply` (register), (3) Run `run_pipeline.py` (compute + write to file). Separation of definition vs computation is explicit.

### Pattern 1: Definition in Python (Feast)
**What:** Define entities, data sources, and feature views in a single module; register with `feast apply`.
**When to use:** Always in Phase 1; keeps “what” (schema, sources) separate from “when” (run script).
**Example:**
```python
# feature_repo/feature_definitions.py (conceptually from Feast quickstart)
from feast import Entity, FeatureView, Field, FileSource
from feast.types import Float32, Int64

entity = Entity(name="driver", join_keys=["driver_id"])
source = FileSource(path="data/driver_stats.parquet", timestamp_field="event_timestamp")
fv = FeatureView(
    name="driver_hourly_stats",
    entities=[entity],
    schema=[
        Field(name="conv_rate", dtype=Float32),
        Field(name="avg_daily_trips", dtype=Int64),
    ],
    source=source,
)
```

### Pattern 2: Compute and Write to File
**What:** Create an entity DataFrame (entity keys + `event_timestamp`), call `get_historical_features`, then write the result to Parquet.
**When to use:** Phase 1 “output = file” requirement; no need to materialize to online store.
**Example:**
```python
# run_pipeline.py
import pandas as pd
from feast import FeatureStore

store = FeatureStore(repo_path="feature_repo")
entity_df = pd.DataFrame({
    "driver_id": [1001, 1002],
    "event_timestamp": pd.to_datetime(["2021-04-12 10:00:00", "2021-04-12 11:00:00"]),
})
features = store.get_historical_features(
    entity_df=entity_df,
    features=["driver_hourly_stats:conv_rate", "driver_hourly_stats:avg_daily_trips"],
).to_df()
features.to_parquet("output/features.parquet")
```

### Anti-Patterns to Avoid
- **Mixing definition and compute in one script:** Keep `feature_definitions.py` for definitions only; run apply and retrieval in a separate script/notebook so separation is obvious.
- **Skipping `feast apply` after editing definitions:** Registry must be updated; planner should add a clear step “run feast apply after changing feature_definitions.py.”
- **Using Tecton for Phase 1:** Requires external login and cloud; contradicts “one runnable example” and “no production server.”

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Feature registry / schema storage | Custom YAML or Python dicts | Feast registry (file-backed) | Versioning and apply workflow come for free; later phases extend same repo. |
| Point-in-time correct joins | Manual pandas joins by timestamp | Feast `get_historical_features` | Correct time-window semantics are subtle; Feast encodes them. |
| “Minimal store” abstraction | Custom read/write layer | Feast file offline store + optional SQLite online | Satisfies “file or minimal store” without building a store. |

**Key insight:** For an engineer-oriented tutorial, using Feast avoids reimplementing feature-store ideas and aligns Phase 1 with later phases (versioning, backfills) that will use the same repo and concepts.

## Common Pitfalls

### Pitfall 1: Wrong working directory / repo_path
**What goes wrong:** `FeatureStore(repo_path=".")` fails or finds no repo when the script is run from the project root instead of inside `feature_repo/`.
**Why it happens:** Feast resolves paths relative to `repo_path`; `feature_store.yaml` and `feature_definitions.py` must be under that path.
**How to avoid:** Use a path relative to the script (e.g. `Path(__file__).parent` for `feature_repo`) or document “run from feature_repo/” and use `repo_path="."`.
**Warning signs:** FileNotFoundError for registry or data files.

### Pitfall 2: entity_df missing event_timestamp
**What goes wrong:** `get_historical_features` errors or returns empty; Feast requires timestamps for point-in-time joins.
**Why it happens:** Entity DataFrame must include the reserved column `event_timestamp`.
**How to avoid:** Always include `event_timestamp` in the entity DataFrame (and use the same name in FileSource).
**Warning signs:** Validation or join errors from Feast.

### Pitfall 3: FileSource path not relative to repo
**What goes wrong:** Feature view cannot read data; path is wrong when run from another cwd.
**Why it happens:** FileSource path is resolved relative to the feature repo directory.
**How to avoid:** Use paths relative to the repo root (e.g. `data/driver_stats.parquet`) and run from repo root or set repo_path correctly.
**Warning signs:** Empty or missing feature values.

### Pitfall 4: Forgetting to run feast apply
**What goes wrong:** New or changed feature views don’t appear; retrieval still uses old schema.
**Why it happens:** Definitions are applied to the registry only when `feast apply` is run.
**How to avoid:** Document “after editing feature_definitions.py, run feast apply” and include it in the run script or README.
**Warning signs:** Old feature list or missing views in retrieval.

## Code Examples

Verified patterns from official sources:

### Minimal feature_store.yaml (local, file offline)
```yaml
# feature_repo/feature_store.yaml (from Feast quickstart)
project: my_project
registry: data/registry.db
provider: local
online_store:
  type: sqlite
  path: data/online_store.db
```
For Phase 1, online store can be omitted or left unused; “output = file” is achieved by writing `get_historical_features(...).to_df()` to Parquet. Optionally use `offline_store: type: file` if documented in the Feast version in use.

### Full definition + compute flow
- **Define:** `feature_definitions.py` with Entity, FileSource, FeatureView (see Pattern 1).
- **Register:** `feast apply` (from `feature_repo/`).
- **Compute and write:** See Pattern 2; entity_df → get_historical_features → .to_df() → .to_parquet("output/features.parquet").

Source: [Feast quickstart](https://docs.feast.dev/getting-started/quickstart) (Steps 2–5, 5 “Generating training data”), and WebSearch-verified File offline store behavior.

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Hand-rolled feature tables only | Feature store (Feast) with registry and apply | Feast adoption in industry | Single place for definitions; same code path for offline and (later) online. |
| Ad hoc scripts only | Definition file + apply + retrieval script | Feast quickstart pattern | Clear separation of definition vs computation. |

**Deprecated/outdated:** Relying on Tecton or a heavy cloud setup for “one runnable example” with no production server — avoid for Phase 1.

## Open Questions

1. **Feast file offline store config**
   - What we know: Local provider uses file/Dask-based offline store; Parquet FileSource is standard.
   - What’s unclear: Exact `feature_store.yaml` for “file” offline store in the latest Feast docs (one fetch 404’d).
   - Recommendation: In implementation, use `feast init` to generate a repo and then simplify to one Entity, one FeatureView, one Parquet under `data/`; if “file” type is specified, add it per [Feast offline store docs](https://docs.feast.dev/reference/offline-stores/overview).

2. **Notebook vs script**
   - What we know: User allows “script or notebook”; engineer-oriented.
   - What’s unclear: No strong preference stated.
   - Recommendation: Let planner choose: script is simpler to run in CI and from CLI; notebook is better for step-by-step explanation. Either way, same two-part structure (definition module + apply + compute/write).

## Sources

### Primary (HIGH confidence)
- [Feast quickstart](https://docs.feast.dev/getting-started/quickstart) — install, init, feature_definitions.py, feature_store.yaml, apply, get_historical_features, to_df().
- Feast quickstart (fetched copy) — Entity, FeatureView, FileSource, get_historical_features, materialize-incremental.

### Secondary (MEDIUM confidence)
- WebSearch: Feast minimal setup offline, Feast write historical to Parquet, File offline store (config and behavior).
- WebSearch: Tecton quickstart — login required; not suitable for Phase 1.

### Tertiary (LOW confidence)
- Feast PyPI version: exact latest version not re-verified; recommend `pip install feast` and document “Python 3.9+, feast from PyPI.”

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — Feast quickstart and docs clearly support local repo, file/Parquet, get_historical_features, and writing to DataFrame/Parquet.
- Architecture: HIGH — Definition vs compute separation is explicit in Feast (definition file vs apply + script).
- Pitfalls: MEDIUM — Repo path, event_timestamp, and apply-after-edit are well-known; file offline store config was partially verified.

**Research date:** 2026-02-25
**Valid until:** ~30 days; re-check Feast docs if implementation lags (e.g. file offline store YAML).

---

## RESEARCH COMPLETE

**Phase:** 1 - Foundation
**Confidence:** HIGH

### Key Findings
- **Feast** is the recommended tooling: local feature repo, clear definition (Python module) vs computation (apply + get_historical_features), output to file via `.to_df().to_parquet()` or file offline store.
- **Tecton** is a poor fit for Phase 1: requires cloud login and is production-oriented.
- **Custom** (pandas-only) is possible but does not teach feature-store concepts or align with later versioning/backfill phases.
- Success path: one feature repo with `feature_definitions.py`, small Parquet under `data/`, `feast apply`, then one script/notebook that runs `get_historical_features` and writes Parquet; learner sees features produced.
- Planner should create tasks for: repo layout, `feature_store.yaml`, `feature_definitions.py`, synthetic data, run script/notebook, and README with run instructions; include “run feast apply after editing definitions” and document repo_path and entity_df requirements.

### File Created
`feature-pipelines-tutorial/.planning/phases/01-foundation/01-RESEARCH.md`

### Confidence Assessment
| Area           | Level  | Reason |
|----------------|--------|--------|
| Standard Stack | HIGH   | Feast quickstart and docs cover local setup and file/Parquet. |
| Architecture   | HIGH   | Definition vs compute is explicit; structure is prescribed. |
| Pitfalls       | MEDIUM | Repo path and apply-after-edit verified; file offline store config partially verified. |

### Open Questions
- Exact `feature_store.yaml` for file-only offline store in latest Feast (optional; `feast init` + docs sufficient to implement).
- Script vs notebook: planner’s choice; both satisfy “one runnable example.”

### Ready for Planning
Research complete. Planner can create PLAN.md and tasks for Phase 1 using Feast, the recommended repo layout, and the pitfalls/patterns above.
