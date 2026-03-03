"""Generate synthetic driver_stats.parquet for the feature repo. Run from feature_repo: python scripts/generate_driver_stats.py"""
import pandas as pd
from pathlib import Path

out = Path(__file__).resolve().parent.parent / "data" / "driver_stats.parquet"
out.parent.mkdir(parents=True, exist_ok=True)
df = pd.DataFrame({
    "driver_id": [1001, 1001, 1002],
    "event_timestamp": pd.to_datetime(["2021-04-12 10:00:00", "2021-04-12 11:00:00", "2021-04-12 10:00:00"]),
    "conv_rate": [0.5, 0.6, 0.4],
    "avg_daily_trips": [100, 120, 80],
})
df["conv_rate"] = df["conv_rate"].astype("float32")
df["avg_daily_trips"] = df["avg_daily_trips"].astype("int64")
df.to_parquet(out, index=False)
print("Created", out)
print(df)
