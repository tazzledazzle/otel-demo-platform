---
phase: 01-foundation
plan: 01
type: execute
wave: 1
depends_on: []
files_modified:
  - feature_repo/feature_store.yaml
  - feature_repo/feature_definitions.py
  - feature_repo/data/driver_stats.parquet
  - requirements.txt
autonomous: true

must_haves:
  truths:
    - "Feature repo exists with Feast config and registry path"
    - "Feature definitions (Entity, FileSource, FeatureView) exist in one module"
    - "Synthetic Parquet data exists under data/ with schema matching FeatureView"
  artifacts:
    - path: feature_repo/feature_store.yaml
      provides: Feast registry and provider config
      contains: "project:", "registry:", "provider: local"
    - path: feature_repo/feature_definitions.py
      provides: Entity, FileSource, FeatureView definitions
      contains: "Entity(", "FeatureView(", "FileSource("
    - path: feature_repo/data/driver_stats.parquet
      provides: Source data for offline feature computation
    - path: requirements.txt
      provides: feast dependency
      contains: "feast"
  key_links:
    - from: feature_repo/feature_definitions.py
      to: feature_repo/data/driver_stats.parquet
      via: FileSource path
      pattern: "path=.*data/.*parquet"
---

<objective>
Set up the Feast feature repo: config, feature definitions, and synthetic source data so that `feast apply` can register the schema and historical retrieval can read from the file source.

Purpose: Establish clear definition layer (what features exist, where they come from) separate from computation.
Output: feature_repo/ with feature_store.yaml, feature_definitions.py, data/driver_stats.parquet; requirements.txt at repo root.
</objective>

<execution_context>
@/Users/terenceschumacher/.claude/get-shit-done/workflows/execute-plan.md
@/Users/terenceschumacher/.claude/get-shit-done/templates/summary.md
</execution_context>

<context>
@.planning/PROJECT.md
@.planning/ROADMAP.md
@.planning/STATE.md
@feature-pipelines-tutorial/.planning/phases/01-foundation/01-CONTEXT.md
@feature-pipelines-tutorial/.planning/phases/01-foundation/01-RESEARCH.md
</context>

<tasks>

<task type="auto">
  <name>Task 1: Repo layout and Feast config</name>
  <files>feature_repo/feature_store.yaml, requirements.txt</files>
  <action>
Create at project root (feature-pipelines-tutorial/):
- requirements.txt containing a single line: feast (or feast with version pin if PROJECT/stack specifies).
Create feature_repo/ and inside it feature_store.yaml with: project (e.g. feature_pipelines_tutorial), registry path under the repo (e.g. data/registry.db), provider: local. Per RESEARCH, omit or minimize online store for Phase 1—either omit online_store or use minimal SQLite at e.g. data/online_store.db so "output = file" remains primary. Use paths relative to the feature repo (registry and data under feature_repo/).
Do not run feast init if it would overwrite or conflict; create the files directly so structure matches RESEARCH (feature_repo/feature_store.yaml, feature_repo/feature_definitions.py, feature_repo/data/).
  </action>
  <verify>Cat feature_repo/feature_store.yaml shows project, registry, provider; cat requirements.txt shows feast; directory feature_repo exists.</verify>
  <done>Feast repo root exists with valid feature_store.yaml and project has feast in requirements.txt.</done>
</task>

<task type="auto">
  <name>Task 2: Feature definitions and synthetic data</name>
  <files>feature_repo/feature_definitions.py, feature_repo/data/driver_stats.parquet</files>
  <action>
In feature_repo/feature_definitions.py define (using feast imports: Entity, FeatureView, Field, FileSource; feast.types Float32, Int64):
- One Entity with name "driver", join_keys=["driver_id"].
- One FileSource with path "data/driver_stats.parquet" (relative to feature repo) and timestamp_field="event_timestamp".
- One FeatureView "driver_hourly_stats" with that entity and source, and schema fields e.g. conv_rate (Float32), avg_daily_trips (Int64). Use the exact field names in the Parquet so the source matches.
Create feature_repo/data/ and a small synthetic Parquet file data/driver_stats.parquet with columns: driver_id (int), event_timestamp (datetime64 or timestamp), conv_rate (float32), avg_daily_trips (int64). Include at least 2–3 rows (e.g. 2 drivers, 1–2 timestamps each) so get_historical_features has something to return. Use pandas DataFrame then .to_parquet(); ensure event_timestamp is the reserved name Feast expects.
  </action>
  <verify>Run from feature_repo: feast apply (should succeed and register the feature view). Python -c "import pandas as pd; print(pd.read_parquet('feature_repo/data/driver_stats.parquet'))" shows the synthetic rows.</verify>
  <done>feature_definitions.py defines one Entity and one FeatureView backed by data/driver_stats.parquet; Parquet exists and feast apply completes without error.</done>
</task>

</tasks>

<verification>
- From feature-pipelines-tutorial: pip install -r requirements.txt (or ensure venv), then cd feature_repo && feast apply → success.
- feature_repo/data/driver_stats.parquet exists and has columns driver_id, event_timestamp, conv_rate, avg_daily_trips.
</verification>

<success_criteria>
- feature_repo/ contains feature_store.yaml and feature_definitions.py; data/driver_stats.parquet exists.
- feast apply runs successfully from feature_repo/.
- Definition (feature_definitions.py) is separate from any compute script; no run_pipeline.py in this plan.
</success_criteria>

<output>
After completion, create .planning/phases/01-foundation/01-foundation-01-SUMMARY.md
</output>
