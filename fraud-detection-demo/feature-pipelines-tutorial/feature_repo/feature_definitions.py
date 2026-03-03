# Feature definitions for the feature-pipelines-tutorial (Feast)

from datetime import timedelta

from feast import Entity, FeatureView, Field, FileSource
from feast.types import Float32, Int64

# Entity: join key for feature retrieval
driver = Entity(name="driver", join_keys=["driver_id"])

# File source: Parquet under feature repo (path relative to feature_repo/)
driver_stats_source = FileSource(
    path="data/driver_stats.parquet",
    timestamp_field="event_timestamp",
)

# Feature view: schema matches Parquet columns
driver_hourly_stats = FeatureView(
    name="driver_hourly_stats",
    entities=[driver],
    ttl=timedelta(days=1),
    schema=[
        Field(name="conv_rate", dtype=Float32),
        Field(name="avg_daily_trips", dtype=Int64),
    ],
    source=driver_stats_source,
)
