# Phase 1: Foundation — Context

**Gathered:** 2026-02-25
**Status:** Ready for planning

<domain>
## Phase Boundary

Deliver one runnable Spark job: DataFrames or Spark SQL, running locally. Language (PySpark or Scala) TBD by research/planner. Build/run steps clear; no cluster or streaming in Phase 1. Engineer-oriented, code-first.

</domain>

<decisions>
## Implementation Decisions

### Job scope
- Single job: read small input (e.g. CSV or built-in), one or two DataFrame/SQL operations, show result (e.g. print or write small output).
- Success = learner runs job and sees output.

### Runtime
- Local Spark only (no YARN/K8s or managed service in Phase 1).
- Prerequisites stated (Java/Python, Spark install or package).

### Format
- Code-first; minimal theory. Clear project layout and run command (e.g. spark-submit or IDE run).

### Claude's Discretion
- PySpark vs Scala; input source; exact operations; output format.

</decisions>

<specifics>
## Specific Ideas

No specific requirements — open to standard Spark tutorial patterns.

</specifics>

<deferred>
## Deferred Ideas

- Cluster deployment, streaming, production patterns — later phases.

</deferred>

---
*Phase: 01-foundation*
*Context gathered: 2026-02-25*
