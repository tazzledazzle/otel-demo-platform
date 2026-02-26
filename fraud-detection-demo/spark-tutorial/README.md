# spark-tutorial

A tutorial that teaches software engineers Apache Spark: DataFrames, batch and streaming, and deployment.

## Prerequisites

- **Java:** 17+ (or 11 for Spark 3.x). `JAVA_HOME` must be set. Check with: `java -version`
- **Python:** 3.10+
- Run from project root: use the `spark-tutorial` directory as the working directory so paths like `data/sample.csv` resolve correctly.

## Run the first job

From the **spark-tutorial** directory:

```bash
pip install -r requirements.txt
python src/first_job.py
```

You should see tabular output from the Spark job in the terminal.
