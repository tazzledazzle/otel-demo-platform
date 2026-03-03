# Phase 1: Foundation — Research

**Researched:** 2026-02-25  
**Domain:** Apache Spark local job (DataFrames/Spark SQL), tutorial-first run  
**Confidence:** HIGH

## Summary

Phase 1 needs one runnable Spark job (DataFrames or Spark SQL) that learners can run locally with clear build/run steps. Language choice (PySpark vs Scala) and input source are at the planner’s discretion; research recommends **PySpark** for this phase: lower setup (pip, no Scala/sbt), Python familiarity for many engineers, and the same DataFrame/SQL concepts as Scala. Use **local** master (`local[*]` or `local[4]`); no cluster or streaming. Prerequisites: Java 17+ (or 11 for Spark 3.x), Python 3.10+ for PySpark 4.x, and `pip install pyspark` (or a Spark distribution with `spark-submit` for Scala). A minimal job: create a `SparkSession`, read a small CSV (or use inline data via `createDataFrame`), apply one or two DataFrame/SQL operations (e.g. filter, select, groupBy+count), then call `df.show()` so the learner sees output in the terminal. Avoid `collect()` for display; use `show()` to limit data on the driver. Document run command explicitly: `python script.py` (PySpark with pip) or `spark-submit --master local[*] script.py` / equivalent for Scala JAR.

**Primary recommendation:** Use PySpark with `pip install pyspark`, a single script, small CSV or inline data, 1–2 DataFrame ops, and `show()` for success. State Java and Python version prerequisites and the exact run command in the tutorial.

<user_constraints>

## User Constraints (from CONTEXT.md)

### Locked Decisions
- Single job: read small input (e.g. CSV or built-in), one or two DataFrame/SQL operations, show result (e.g. print or write small output). Success = learner runs job and sees output.
- Local Spark only (no YARN/K8s or managed service in Phase 1).
- Prerequisites stated (Java/Python, Spark install or package).
- Code-first; minimal theory. Clear project layout and run command (e.g. spark-submit or IDE run).

### Claude's Discretion
- PySpark vs Scala; input source; exact operations; output format.

### Deferred Ideas (OUT OF SCOPE)
- Cluster deployment, streaming, production patterns — later phases.

</user_constraints>

## Standard Stack

### Core
| Library / runtime | Version | Purpose | Why standard |
|-------------------|---------|---------|--------------|
| Apache Spark (PySpark) | 4.1.x or 3.5.x | DataFrames, Spark SQL, local execution | Official API; pip install for PySpark. |
| Java (JRE/JDK) | 17+ (4.x), 8/11/17 (3.x) | Spark JVM backend | Required by Spark; must be on PATH / JAVA_HOME. |
| Python | 3.10+ (4.x) | PySpark driver | Official PySpark 4.x requirement. |

### Supporting
| Item | Purpose | When to use |
|------|---------|-------------|
| `pip install pyspark` | Install Spark for Python | Default for Phase 1 (no Spark tarball). |
| `spark-submit` | Run app with master/config | When using Spark distro or Scala JAR; optional for PySpark+pip. |
| Small CSV or inline data | Input for job | CSV: realistic I/O; inline: zero file dependency. |

### Alternatives considered
| Instead of | Could use | Tradeoff |
|------------|-----------|----------|
| PySpark | Scala + sbt | Scala: better perf, native API; more setup (sbt, Scala version, JAR packaging). Prefer PySpark for “first run” tutorial. |
| CSV file | `spark.read.text()` or inline `createDataFrame` | Text/built-in: no file; CSV teaches common source and options (header, schema). |
| `show()` | `collect()` then print | `show()` is driver-safe and standard for “see result”; `collect()` risks OOM. |

**Installation (PySpark):**
```bash
pip install pyspark
```
Prerequisites: Java 17+ (4.x) or 11 (3.x), `JAVA_HOME` set; Python 3.10+.

## Architecture Patterns

### Recommended project structure (PySpark)
```
spark-tutorial/
├── .planning/
├── data/                    # optional: small CSV for input
│   └── sample.csv
├── src/ or jobs/             # single script for Phase 1
│   └── first_job.py
├── README.md                 # prerequisites + run command
└── requirements.txt          # pyspark==4.1.1 or 3.5.x
```

### Pattern 1: SparkSession and local master
**What:** Single entry point; default local master when using pip PySpark.  
**When:** Every self-contained app.  
**Example:**
```python
# Source: https://spark.apache.org/docs/latest/quick-start.html
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("SimpleApp").getOrCreate()
# Optional: .master("local[*]") if not using spark-submit
# ... read, transform, show ...
spark.stop()
```

### Pattern 2: Read CSV, 1–2 ops, show result
**What:** DataFrame reader with header/schema options; one or two transformations; show output.  
**When:** Phase 1 “one runnable job.”  
**Example:**
```python
# Source: https://spark.apache.org/docs/latest/sql-data-sources-csv.html
df = spark.read.options(header=True, inferSchema=True).csv("data/sample.csv")
df2 = df.filter(df["age"] > 25).select("name", "age")
df2.show()
```

### Pattern 3: Inline data (no file)
**What:** Use `createDataFrame` so the job needs no input file.  
**When:** Maximize portability or avoid path handling.  
**Example:**
```python
# Source: Spark createDataFrame API
df = spark.createDataFrame([("Alice", 30), ("Bob", 25)], ["name", "age"])
df.filter(df.age > 25).show()
```

### Anti-patterns to avoid
- **Relying on `collect()` for “see result”:** Use `show()` so the driver doesn’t pull the whole dataset; document that `show()` is for inspection.
- **Extending `scala.App` (Scala):** Use a `main(args)` method; see official Quick Start.
- **Bundling Spark in the app JAR (Scala):** Use `provided` scope for Spark so the JAR stays small and compatible with `spark-submit`.

## Don't Hand-Roll

| Problem | Don't build | Use instead | Why |
|---------|-------------|-------------|-----|
| Spark session / context | Manual config of driver/executor | `SparkSession.builder.appName(...).getOrCreate()` | Handles config and reuse. |
| CSV parsing | Custom parser | `spark.read.csv(...)` with `option("header", True)` and optionally `inferSchema=True` | Edge cases, encoding, schema. |
| “Print first N rows” | Custom collect + format | `df.show(n)` | Truncation, formatting, driver safety. |

**Key insight:** Session creation and CSV/DataFrame I/O are standard and well-tested; custom logic here adds failure modes for no benefit in Phase 1.

## Common Pitfalls

### Pitfall 1: Java not installed or not on PATH / JAVA_HOME
**What goes wrong:** PySpark fails at import or job start with JVM errors.  
**Why:** Spark runs on the JVM; PySpark uses Py4J to talk to it.  
**How to avoid:** Document “Java 17+ (or 11 for 3.x) installed and JAVA_HOME set.” Add a one-line check in README (e.g. `java -version`).  
**Warning signs:** “JAVA_HOME is not set” or “Could not find or load main class.”

### Pitfall 2: Input path only works on one machine
**What goes wrong:** Hardcoded absolute path or YOUR_SPARK_HOME-style path; job fails for others.  
**Why:** Quick Start examples use a placeholder path.  
**How to avoid:** Use a path relative to project root (e.g. `data/sample.csv`) or inline data; document “run from repo root” or set working directory.  
**Warning signs:** FileNotFoundError or “path does not exist.”

### Pitfall 3: Forgetting spark.stop()
**What goes wrong:** Script exits but JVM may linger or resources not released (minor for a one-off run).  
**Why:** Session holds resources.  
**How to avoid:** Call `spark.stop()` at end of script, or use session as context manager where supported.  
**Warning signs:** Multiple runs leaving processes or ports in use.

### Pitfall 4: Scala version mismatch (if using Scala)
**What goes wrong:** Spark built for Scala 2.13 fails with 2.12 (or vice versa).  
**Why:** Spark artifacts are Scala-versioned.  
**How to avoid:** In `build.sbt`, use the same Scala version as the Spark distribution (e.g. 2.13 for Spark 4.x).  
**Warning signs:** Resolution or runtime errors about Scala or spark-sql_2.xx.

## Code Examples

Verified patterns from official sources:

### Minimal PySpark job (read text, filter, show)
```python
# Source: https://spark.apache.org/docs/latest/quick-start.html
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("SimpleApp").getOrCreate()
logData = spark.read.text("path/to/file").cache()
numAs = logData.filter(logData.value.contains("a")).count()
numBs = logData.filter(logData.value.contains("b")).count()
print("Lines with a: %i, lines with b: %i" % (numAs, numBs))
spark.stop()
```

### Read CSV with header and schema
```python
# Source: https://spark.apache.org/docs/latest/sql-data-sources-csv.html
df = spark.read.option("delimiter", ",").option("header", True).csv(path)
# or: .options(header=True, inferSchema=True).csv(path)
df.show()
```

### Run with spark-submit (local)
```bash
# Source: https://spark.apache.org/docs/latest/submitting-applications.html
# PySpark (script)
spark-submit --master "local[*]" src/first_job.py

# With pip-installed PySpark, alternative:
python src/first_job.py
```

### Master URLs (local)
| URL | Meaning |
|-----|---------|
| `local` | One thread (no parallelism). |
| `local[K]` | K worker threads. |
| `local[*]` | As many threads as logical cores. |

## State of the Art

| Old approach | Current approach | When / impact |
|--------------|------------------|----------------|
| RDD as main API | Dataset/DataFrame (Spark 2.0+) | Use DataFrames/SQL for Phase 1; avoid RDD in tutorial. |
| Spark 2.x / 3.0 | Spark 3.5.x / 4.1.x | 4.x: Java 17+, Python 3.10+; 3.5 still common. |
| Only Spark distro | PySpark via pip | pip is standard for local/dev; no tarball required. |

**Deprecated/outdated:** Teaching RDD-first for a “first job” is discouraged; Quick Start and docs are DataFrame-first.

## Open Questions

1. **Spark version to pin (4.1 vs 3.5)**  
   - Known: 4.1 is latest in docs; 3.5 has broader Java (8/11/17) and may be more common in some envs.  
   - Recommendation: Pin 3.5.x or 4.1.x in requirements and document the chosen Java/Python matrix.

2. **Input: CSV in repo vs inline only**  
   - CSV: teaches real I/O and options; need a small sample file and path rules.  
   - Inline: no file, simplest run; less I/O practice.  
   - Recommendation: Prefer one small CSV under `data/` and document “run from project root”; optional second example with `createDataFrame` if planner wants both.

## Sources

### Primary (HIGH confidence)
- [Spark 4.1.1 Quick Start](https://spark.apache.org/docs/latest/quick-start.html) — self-contained PySpark/Scala apps, spark-submit, local[4], SimpleApp.
- [Submitting Applications](https://spark.apache.org/docs/latest/submitting-applications.html) — master URLs, local[*], spark-submit options.
- [PySpark Installation](https://spark.apache.org/docs/latest/api/python/getting_started/install.html) — pip, Python 3.10+, Java 17+, JAVA_HOME.
- [CSV Data Source](https://spark.apache.org/docs/latest/sql-data-sources-csv.html) — read options, header, delimiter, examples.

### Secondary (MEDIUM confidence)
- Web search: PySpark vs Scala for beginners; sbt minimal Spark project; show() vs collect(); createDataFrame.
- Spark 3.5.4 overview (Java/Python versions) cross-checked with install docs.

### Tertiary (LOW confidence)
- Community posts on PySpark vs Scala “when to use”; not needed for Phase 1 stack choice.

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — official install, Quick Start, and submitting-applications docs.
- Architecture: HIGH — patterns and examples from same docs.
- Pitfalls: HIGH — JAVA_HOME, paths, and show vs collect are well documented.

**Research date:** 2026-02-25  
**Valid until:** ~30 days (stable Spark 3.x/4.x).

---

## RESEARCH COMPLETE

**Phase:** 1 - Foundation  
**Confidence:** HIGH

### Key findings
- **PySpark recommended** for Phase 1: pip install, no Scala/sbt, same DataFrame/SQL concepts; document Java 17+ (or 11) and Python 3.10+.
- **Local master:** Use default (pip) or `--master local[*]` / `local[4]`; no cluster.
- **Minimal job:** One script, `SparkSession.builder.getOrCreate()`, read small CSV (or `createDataFrame`), 1–2 ops, `show()`; run with `python script.py` or `spark-submit`.
- **Output:** Use `df.show()` for “see result”; avoid `collect()` for display.
- **Prerequisites:** State Java and Python versions and run command in README; optional one-line Java check.

### File created
`spark-tutorial/.planning/phases/01-foundation/01-RESEARCH.md`

### Confidence assessment
| Area         | Level | Reason |
|--------------|-------|--------|
| Standard stack | HIGH | Official install, Quick Start, CSV and submit docs. |
| Architecture   | HIGH | Same docs; SimpleApp and CSV examples. |
| Pitfalls       | HIGH | JAVA_HOME, paths, show vs collect documented. |

### Open questions
- Pin Spark 4.1.x vs 3.5.x (and corresponding Java/Python matrix).
- Prefer one small repo CSV vs inline-only vs both (recommend CSV + “run from root”).

### Ready for planning
Research is complete. Planner can create PLAN.md using this document.
