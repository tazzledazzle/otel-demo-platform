---
phase: 01-foundation
plan: 02
type: execute
wave: 2
depends_on: [01]
files_modified:
  - feature_repo/run_pipeline.py
  - README.md
autonomous: true

must_haves:
  truths:
    - "Learner can run the pipeline end-to-end (feast apply then run script)"
    - "Computed features are written to a file (Parquet)"
    - "Definition (feature_definitions.py) and computation (run_pipeline.py) are separate"
  artifacts:
    - path: feature_repo/run_pipeline.py
      provides: Compute step and file output
      contains: "FeatureStore(", "get_historical_features", "to_parquet"
    - path: README.md
      provides: Run instructions
      contains: "feast apply", "run_pipeline" or "python run_pipeline"
  key_links:
    - from: feature_repo/run_pipeline.py
      to: feature_repo (FeatureStore repo_path)
      via: FeatureStore(repo_path=...)
      pattern: "FeatureStore\\(.*repo_path"
    - from: feature_repo/run_pipeline.py
      to: output file
      via: get_historical_features(...).to_df().to_parquet(...)
      pattern: "to_parquet"
    - from: README.md
      to: run sequence
      via: instructions to run feast apply then run_pipeline.py
---

<objective>
Add the compute-and-write step and run instructions so the learner can execute one full pipeline run and see features written to a file.

Purpose: Satisfy "one runnable example" and "write to file" with clear separation—compute lives in run_pipeline.py, not in feature_definitions.py.
Output: feature_repo/run_pipeline.py (entity_df → get_historical_features → Parquet), README.md with run steps.
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
  <name>Task 1: Run script (compute and write to Parquet)</name>
  <files>feature_repo/run_pipeline.py</files>
  <action>
Create feature_repo/run_pipeline.py that:
- Resolves repo_path so it works when the script is run from feature_repo/ (e.g. repo_path="." when run from feature_repo, or use Path(__file__).parent so it works from repo root). Per RESEARCH pitfall: avoid wrong working directory—document or implement so running from feature_repo/ works.
- Instantiates FeatureStore(repo_path=...).
- Builds an entity_df pandas DataFrame with columns driver_id and event_timestamp (required by Feast for point-in-time join). Use timestamps that exist in the synthetic data (e.g. the same event_timestamp values from data/driver_stats.parquet) so features are returned.
- Calls store.get_historical_features(entity_df=entity_df, features=["driver_hourly_stats:conv_rate", "driver_hourly_stats:avg_daily_trips"]) (or equivalent for the feature view name from plan 01).
- Converts to DataFrame with .to_df(), then writes to output/features.parquet (create output/ directory if needed, e.g. under feature_repo or project root—choose one and be consistent).
- Add a short comment at top: run "feast apply" from feature_repo/ before running this script after any change to feature_definitions.py.
  </action>
  <verify>From feature_repo: python run_pipeline.py runs without error; output file exists (e.g. feature_repo/output/features.parquet or path used in script). Python -c "import pandas as pd; print(pd.read_parquet('feature_repo/output/features.parquet'))" shows columns including feature columns.</verify>
  <done>Running run_pipeline.py produces a Parquet file with historical features for the entity_df; no crash and file is readable.</done>
</task>

<task type="auto">
  <name>Task 2: README run instructions</name>
  <files>README.md</files>
  <action>
Create or update README.md at project root (feature-pipelines-tutorial/) with:
- Brief description: one runnable feature pipeline (define features, compute offline, write to file) using Feast.
- How to run: (1) pip install -r requirements.txt, (2) cd feature_repo, (3) feast apply, (4) python run_pipeline.py. State that after editing feature_definitions.py you must run feast apply again.
- Note where output is written (e.g. feature_repo/output/features.parquet).
Keep it engineer-oriented and code-first; no lengthy theory.
  </action>
  <verify>README exists and contains the four-step run sequence and the note about feast apply after editing definitions.</verify>
  <done>README allows a learner to run the pipeline end-to-end and find the output file.</done>
</task>

</tasks>

<verification>
- Full run: pip install -r requirements.txt, cd feature_repo, feast apply, python run_pipeline.py → success and output Parquet exists.
- README documents this sequence and output location.
</verification>

<success_criteria>
- One runnable pipeline: definition in feature_definitions.py, compute in run_pipeline.py, output to Parquet.
- Learner can follow README to produce features.parquet.
- Clear definition/compute separation (no computation in feature_definitions.py).
</success_criteria>

<output>
After completion, create .planning/phases/01-foundation/01-foundation-02-SUMMARY.md
</output>
