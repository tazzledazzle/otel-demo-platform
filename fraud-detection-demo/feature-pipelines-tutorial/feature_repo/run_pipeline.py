# Run "feast apply" from feature_repo/ before running this script after any change to feature_definitions.py.

import pandas as pd
from pathlib import Path

from feast import FeatureStore

# Repo path: run this script from feature_repo/ (e.g. cd feature_repo && python run_pipeline.py).
repo_path = "."
store = FeatureStore(repo_path=repo_path)

# Entity DataFrame for point-in-time join: use driver_id and event_timestamp from source data.
driver_stats_path = Path(repo_path) / "data" / "driver_stats.parquet"
source_df = pd.read_parquet(driver_stats_path)
entity_df = source_df[["driver_id", "event_timestamp"]].copy()

# Historical features for driver_hourly_stats; write to Parquet.
features = [
    "driver_hourly_stats:conv_rate",
    "driver_hourly_stats:avg_daily_trips",
]
df = store.get_historical_features(entity_df=entity_df, features=features).to_df()

out_dir = Path(repo_path) / "output"
out_dir.mkdir(parents=True, exist_ok=True)
out_path = out_dir / "features.parquet"
df.to_parquet(out_path, index=False)
print("Wrote", out_path)
