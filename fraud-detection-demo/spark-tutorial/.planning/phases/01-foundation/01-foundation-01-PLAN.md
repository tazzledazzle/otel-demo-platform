---
phase: 01-foundation
plan: 01
type: execute
wave: 1
depends_on: []
files_modified:
  - spark-tutorial/requirements.txt
  - spark-tutorial/README.md
  - spark-tutorial/data/sample.csv
  - spark-tutorial/src/first_job.py
autonomous: true
user_setup: []

must_haves:
  truths:
    - "Learner can run the job from project root and see DataFrame output in the terminal"
    - "Prerequisites (Java 17+ or 11, Python 3.10+, pyspark) are documented and run command is explicit"
    - "Job uses DataFrames (read CSV), 1–2 operations, and show() for output (no collect for display)"
  artifacts:
    - path: spark-tutorial/requirements.txt
      provides: pyspark dependency
      contains: pyspark
    - path: spark-tutorial/README.md
      provides: prerequisites and run instructions
      contains: "run from project root", run command, Java, Python
    - path: spark-tutorial/data/sample.csv
      provides: small CSV input
      min_lines: 2
    - path: spark-tutorial/src/first_job.py
      provides: runnable Spark job
      contains: SparkSession, read csv, show(), spark.stop()
  key_links:
    - from: spark-tutorial/src/first_job.py
      to: spark-tutorial/data/sample.csv
      via: relative path (e.g. data/sample.csv)
      pattern: "read.*csv|\.csv\("
    - from: spark-tutorial/README.md
      to: run command
      via: "python src/first_job.py"
      pattern: "python.*first_job"
---

<objective>
Deliver one runnable PySpark job that learners run locally from the project root: DataFrames, read small CSV, 1–2 operations, show result in the terminal. Prerequisites and run command documented.

Purpose: Satisfy Phase 1 goal (one runnable Spark job, local, code-first). Uses RESEARCH recommendation: PySpark, pip install pyspark, Java 17+ (or 11), Python 3.10+, run with `python src/first_job.py` from repo root.

Output: requirements.txt, README.md, data/sample.csv, src/first_job.py; verified by running the job and seeing output.
</objective>

<execution_context>
@/Users/terenceschumacher/.claude/get-shit-done/workflows/execute-plan.md
@/Users/terenceschumacher/.claude/get-shit-done/templates/summary.md
</execution_context>

<context>
@spark-tutorial/.planning/PROJECT.md
@spark-tutorial/.planning/ROADMAP.md
@spark-tutorial/.planning/STATE.md
@spark-tutorial/.planning/phases/01-foundation/01-CONTEXT.md
@spark-tutorial/.planning/phases/01-foundation/01-RESEARCH.md
</context>

<tasks>

<task type="auto">
  <name>Task 1: Project setup — requirements and README</name>
  <files>spark-tutorial/requirements.txt</files>
  <files>spark-tutorial/README.md</files>
  <action>
Create spark-tutorial/requirements.txt with pyspark pinned (use pyspark==3.5.3 or 4.1.1 per RESEARCH; prefer 3.5.x for broader Java 11/17 compatibility).

Create or update spark-tutorial/README.md with:
- Prerequisites: Java 17+ (or 11 for Spark 3.x), Python 3.10+, and that JAVA_HOME must be set. Include a one-line verification (e.g. "Check with: java -version").
- Instruction: run from project root (spark-tutorial/ or repo root as appropriate—clarify "from spark-tutorial directory" so paths like data/sample.csv resolve).
- Exact run command: `pip install -r requirements.txt` then `python src/first_job.py`.
Do not add cluster, streaming, or deployment content (deferred per CONTEXT).
  </action>
  <verify>File spark-tutorial/requirements.txt exists and contains pyspark; README mentions Java, Python, run-from-root, and the run command.</verify>
  <done>requirements.txt has pyspark; README states prerequisites and "run from project root" plus `python src/first_job.py`.</done>
</task>

<task type="auto">
  <name>Task 2: Sample data and runnable job</name>
  <files>spark-tutorial/data/sample.csv</files>
  <files>spark-tutorial/src/first_job.py</files>
  <action>
Create spark-tutorial/data/sample.csv: small CSV with header (e.g. name,age or id,value). At least 3–5 rows so filter/aggregate output is visible. Use simple values (no special chars that break CSV).

Create spark-tutorial/src/first_job.py:
- Use SparkSession.builder.appName("FirstJob").getOrCreate() (no hand-rolled session config per RESEARCH).
- Read CSV with relative path so it works from project root: e.g. spark.read.options(header=True, inferSchema=True).csv("data/sample.csv"). Use path relative to current working directory (runner must be in spark-tutorial).
- Apply exactly 1–2 DataFrame operations (e.g. filter on a column, then select; or groupBy + count). Must be real ops, not just show.
- Call df.show() to print result (do not use collect() for display per RESEARCH).
- Call spark.stop() at end.
Use standard PySpark APIs only; no RDD. Document in a short comment that the script expects to be run from the spark-tutorial directory.
  </action>
  <verify>data/sample.csv exists with header and rows; src/first_job.py exists, contains SparkSession, read csv, at least one filter/select or groupBy, show(), spark.stop().</verify>
  <done>CSV and script exist; script reads CSV via relative path, applies 1–2 ops, shows result, stops session.</done>
</task>

<task type="auto">
  <name>Task 3: Verify runnable job</name>
  <files>spark-tutorial/src/first_job.py</files>
  <action>
From repository root (parent of spark-tutorial): cd spark-tutorial, then run:
  pip install -r requirements.txt
  python src/first_job.py
Confirm exit code 0 and that stdout contains tabular/text output from show() (e.g. grep or expect lines that look like DataFrame output). If run fails due to JAVA_HOME or missing Java, document the failure in verification step; success means learner would see the same. Do not add cluster or streaming.
  </action>
  <verify>cd spark-tutorial && pip install -r requirements.txt && python src/first_job.py exits 0; stdout shows DataFrame output (e.g. column headers and rows).</verify>
  <done>Job runs from spark-tutorial directory and prints DataFrame result to terminal; prerequisites satisfied (Java/Python/pyspark) for a clean run.</done>
</task>

</tasks>

<verification>
- From spark-tutorial: pip install -r requirements.txt && python src/first_job.py → exit 0, output visible.
- README run command and prerequisites match what is required.
- No use of collect() for displaying result; show() used.
</verification>

<success_criteria>
- One runnable PySpark job (src/first_job.py) using DataFrames, local only.
- Clear build/run: requirements.txt + README with prereqs and run-from-root + python src/first_job.py.
- Learner runs job and sees DataFrame output in the terminal.
</success_criteria>

<output>
After completion, create spark-tutorial/.planning/phases/01-foundation/01-foundation-01-SUMMARY.md
</output>
