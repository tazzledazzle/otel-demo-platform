# Feature Pipelines Tutorial

One runnable feature pipeline with Feast: define features, compute offline, write to file.

## How to run

1. `pip install -r requirements.txt`
2. `cd feature_repo`
3. `feast apply`
4. `python run_pipeline.py`

After editing `feature_definitions.py`, run `feast apply` again before `python run_pipeline.py`.

**Output:** `feature_repo/output/features.parquet` (historical features for the entity DataFrame).
