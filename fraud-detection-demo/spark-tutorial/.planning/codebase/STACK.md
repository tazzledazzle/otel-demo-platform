# Technology Stack

**Analysis Date:** 2025-02-25

## Languages

**Primary (intended):**
- Python (PySpark) or Scala — stated in `spark-tutorial/.planning/PROJECT.md`; not yet chosen or locked.

**Secondary:**
- Not applicable.

## Runtime

**Environment:**
- Apache Spark (local or cluster). Version and distribution (e.g. upstream, Databricks, EMR) TBD.

**Package Manager:**
- Not present. When added: pip/venv for Python, sbt or Maven for Scala. No lockfile yet.

## Frameworks

**Core:**
- Apache Spark — DataFrames, Spark SQL, batch and streaming (from PROJECT.md).

**Testing:**
- Not selected. Likely pytest (Python) or ScalaTest/sbt (Scala) when tests are added.

**Build/Dev:**
- GSD workflow driven by `spark-tutorial/config.json` (mode, depth, parallelization, commit_docs, model_profile, workflow flags). No build tool in repo yet.

## Key Dependencies

**Critical (intended):**
- Apache Spark — core runtime and APIs for the tutorial.

**Infrastructure:**
- Deployment target: standalone, YARN, or managed (from PROJECT.md). No infra code yet.

## Configuration

**Environment:**
- No `.env` or env docs. Future: Spark master URL, app name, resource settings typically via env or Spark config.

**Build:**
- No build config (no `pyproject.toml`, `build.sbt`, `pom.xml`). GSD config only: `spark-tutorial/config.json`.

## Platform Requirements

**Development:**
- To be defined with first phase (e.g. Java/Python version, Spark install or Docker).

**Production:**
- Tutorial-focused; “production” only if a phase explicitly covers deployment (standalone/YARN/managed).

---

*Stack analysis: 2025-02-25*
