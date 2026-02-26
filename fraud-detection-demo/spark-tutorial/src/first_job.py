"""
First Spark job: read CSV, apply 1-2 DataFrame ops, show result.
Run from the spark-tutorial directory so data/sample.csv resolves.
"""
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("FirstJob").getOrCreate()

# Read CSV; path is relative to current working directory (spark-tutorial).
df = spark.read.options(header=True, inferSchema=True).csv("data/sample.csv")

# 1-2 operations: filter then select.
result = df.filter(df["age"] >= 25).select("name", "age", "score")
result.show()

spark.stop()
