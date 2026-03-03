# Phase 1: Foundation — Research

**Researched:** 2026-02-25
**Domain:** Python ML environment, first scikit-learn model (train/eval), minimal setup
**Confidence:** HIGH

## Summary

Phase 1 delivers a runnable local Python/ML environment and one end-to-end lesson: load a small dataset, split train/test, fit a classifier, and report accuracy. The standard stack is Python 3.10+, venv, pip, scikit-learn (and optionally pandas). Use scikit-learn’s built-in Iris dataset and `train_test_split` so there are no data files or preprocessing; the lesson can be script-only for minimal dependencies and a true single-command run, or a Jupyter notebook if interactivity is preferred (adds Jupyter to the stack).

**Primary recommendation:** Use a single Python script, Iris dataset, `train_test_split`, one classifier (e.g. `LogisticRegression` or `SVC`), and `model.score(X_test, y_test)` for accuracy. Document setup as: create venv → activate → `pip install -r requirements.txt` → `python lesson1.py`. Do not fit on test data or do preprocessing before split; split first, then fit only on train.

<user_constraints>

## User Constraints (from CONTEXT.md)

### Locked Decisions
- **Lesson format:** One primary artifact (script or notebook TBD). Engineer-oriented, code-first, minimal conceptual preamble. Prerequisites stated clearly (Python version, venv, install steps).
- **Scope of first model:** Single small dataset (e.g. built-in or one CSV); no data pipeline. Train + evaluate only; no hyperparameter tuning or comparison in Phase 1. Success = runnable end-to-end; metrics (e.g. accuracy) shown.
- **Setup and run:** Single-command or minimal-step run (e.g. `pip install -r requirements.txt && python train.py` or notebook run-all). No cloud or GPU; local-only for Phase 1.

### Claude's Discretion
- Exact dataset choice; notebook vs script; output format (print vs file).
- Whether to include a tiny "what we did" summary in the lesson.

### Deferred Ideas (OUT OF SCOPE)
- Deployment, production patterns, or ML ops — later phases.
- Deep learning (PyTorch/TensorFlow) — later phase or optional extension.

</user_constraints>

## Standard Stack

### Core
| Library       | Version   | Purpose                          | Why Standard |
|---------------|-----------|----------------------------------|--------------|
| Python        | 3.10+     | Runtime                          | PROJECT.md; scikit-learn 1.7+ requires 3.10 |
| scikit-learn  | ≥1.5 (e.g. 1.5.x) | Load data, split, fit, score | De facto for tabular ML in Python; one package for data, models, metrics |
| pip + venv     | (stdlib)  | Isolate deps, install             | Official scikit-learn install docs recommend venv |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| pandas  | ≥1.5.0  | DataFrames for load_iris(as_frame=True) or CSV | Optional for Phase 1; use if lesson shows DataFrame API for consistency with later phases |
| numpy   | (pulled by sklearn) | Arrays | Required by scikit-learn; no need to list separately if only using sklearn |

### Alternatives Considered
| Instead of     | Could Use | Tradeoff |
|----------------|-----------|----------|
| scikit-learn   | —         | No alternative for “one small dataset, train+eval only” without adding complexity (e.g. TensorFlow/PyTorch deferred). |
| venv + pip     | conda     | venv is zero-install and matches PROJECT.md; conda adds tooling. |
| Script         | Jupyter   | Script: minimal deps, `python lesson1.py`; Jupyter: interactivity, extra deps (jupyter, ipykernel). |

**Installation (minimal):**

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

**requirements.txt (minimal for Phase 1):**

```
scikit-learn>=1.5
```

Optional: add `pandas>=1.5` if the lesson uses DataFrames. scikit-learn pulls numpy, scipy, joblib, threadpoolctl; no need to list them unless pinning.

## Architecture Patterns

### Recommended Project Structure

```
python-ml-tutorial/
├── .venv/                    # (optional, gitignored) venv
├── requirements.txt         # scikit-learn (and optionally pandas)
├── lesson1.py                # or 01_train_eval.py — single runnable artifact
└── README.md                 # Prerequisites + setup + run (minimal steps)
```

Notebook variant: e.g. `lesson1.ipynb` plus `requirements.txt` including `jupyter`; run via “Run All” or `jupyter execute lesson1.ipynb`.

### Pattern 1: Load → Split → Fit → Score

**What:** Load data, split once, fit on train only, evaluate on test with `.score()`.

**When:** Any first lesson with a single dataset and no preprocessing.

**Example:**

```python
# Source: scikit-learn install + load_iris + common_pitfalls
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

X, y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
model = LogisticRegression(max_iter=200, random_state=42)
model.fit(X_train, y_train)
accuracy = model.score(X_test, y_test)
print(f"Test accuracy: {accuracy:.3f}")
```

### Pattern 2: Reproducibility

**What:** Use `random_state` (e.g. 42) on `train_test_split` and on the estimator so runs are reproducible.

**When:** Every lesson and any script that runs in automation or is shared.

### Anti-Patterns to Avoid

- **Fitting or transforming on full data before split:** Causes data leakage. Split first; call `fit`/`fit_transform` only on training data. (Official docs: [common pitfalls](https://scikit-learn.org/stable/common_pitfalls.html).)
- **Evaluating on training data only:** Inflates perceived performance. Always report test (or validation) metric.
- **Skipping train/test split:** For a “first model” lesson, always show a held-out test set so learners see the correct evaluation pattern.

## Don't Hand-Roll

| Problem              | Don't Build           | Use Instead              | Why |
|----------------------|------------------------|---------------------------|-----|
| Train/test split     | Manual indexing/sampling | `sklearn.model_selection.train_test_split` | Stratification, shuffle, reproducibility. |
| Accuracy             | Manual correct-count   | `model.score(X_test, y_test)` or `accuracy_score(y_test, y_pred)` | Classifiers’ `.score` is accuracy; one call. |
| Loading classic data | Download CSV, parse    | `sklearn.datasets.load_iris()` (and similar) | Built-in, no I/O, correct format. |
| Virtual environment  | Custom isolation       | `python -m venv .venv`     | Stdlib, documented in sklearn install. |

**Key insight:** scikit-learn already provides data loaders, splits, and metrics; hand-rolling any of these adds bugs and teaches the wrong API.

## Common Pitfalls

### Pitfall 1: Data leakage from preprocessing

**What goes wrong:** Preprocessing (e.g. scaling, imputation) is fitted on the full dataset, then data is split. Test information leaks into the model.

**Why it happens:** Doing “prepare data” before “split” feels natural.

**How to avoid:** Split first. Fit any transformer only on `X_train`/`y_train`; transform both train and test with the same fitted transformer. For Phase 1, avoid preprocessing entirely so the only rule is “split first, fit on train.”

**Warning signs:** Any `fit` or `fit_transform` called on `X` or `y` before `train_test_split`.

### Pitfall 2: Evaluating only on training data

**What goes wrong:** Model is evaluated with `model.score(X_train, y_train)` and reported as “accuracy,” giving overoptimistic results.

**Why it happens:** Using the same data for training and evaluation.

**How to avoid:** Always compute and report metric on `X_test`, `y_test` (e.g. `model.score(X_test, y_test)`).

**Warning signs:** No `X_test`/`y_test` in the script, or only training accuracy printed.

### Pitfall 3: Inconsistent preprocessing on test

**What goes wrong:** Train is scaled (or otherwise transformed), test is not, or test is transformed with a different fitted state.

**Why it happens:** Forgetting to apply the same transformation to test.

**How to avoid:** For Phase 1, use no preprocessing. Later: use a `Pipeline` so transform is applied consistently (fit on train, transform test with same transformer).

### Pitfall 4: Python or sklearn version mismatch

**What goes wrong:** Learners have Python &lt;3.10 or old sklearn; examples or APIs fail.

**Why it happens:** Prerequisites not stated or not checked.

**How to avoid:** State in README: “Python 3.10+”; pin `scikit-learn>=1.5` (or current stable). Optional: one-line version check at top of script (e.g. `import sys; assert sys.version_info >= (3, 10)`).

## Code Examples

Verified patterns from official sources:

### Load Iris and split

```python
# Source: https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_iris.html
#         https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

X, y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
```

### Train and evaluate (accuracy)

```python
# Source: ClassifierMixin .score returns accuracy; sklearn install + Inria MOOC
from sklearn.linear_model import LogisticRegression

model = LogisticRegression(max_iter=200, random_state=42)
model.fit(X_train, y_train)
accuracy = model.score(X_test, y_test)
print(f"Test accuracy: {accuracy:.3f}")
```

### Optional: Iris as DataFrame (pandas)

```python
# Source: load_iris as_frame parameter
from sklearn.datasets import load_iris

data = load_iris(as_frame=True)
X = data.data
y = data.target
# Then split and fit as above; model.fit() accepts DataFrame.
```

## State of the Art

| Old Approach           | Current Approach        | When Changed | Impact |
|------------------------|-------------------------|--------------|--------|
| Manual train/test split | `train_test_split`       | Long-standing | Always use it; supports stratify, random_state. |
| Fit preprocessing on all data | Fit on train only, transform test | Documented in common pitfalls | Prevents leakage. |
| Python 3.7–3.9        | Python 3.10+ for sklearn 1.7+ | scikit-learn 1.7 | Align with PROJECT.md 3.10+. |

**Deprecated/outdated:** None relevant for Phase 1 (no deprecated sklearn APIs for load_iris, train_test_split, or classifier `.score`).

## Open Questions

1. **Notebook vs script**
   - **Known:** Script = minimal deps, `pip install -r requirements.txt && python lesson1.py`. Notebook = better for step-by-step reading and re-runs; requires Jupyter in requirements and “Run All” or CLI execution.
   - **Unclear:** Whether “engineer-oriented, code-first” implies preference for script (closer to production) or notebook (clearer for learning).
   - **Recommendation:** Prefer **script** for Phase 1 to keep setup minimal and run single-command; planner can choose notebook if interactivity is prioritized and Jupyter is acceptable.

2. **Output format**
   - **Known:** At least one metric (accuracy) must be shown. Print to stdout is sufficient.
   - **Unclear:** Whether to also write metrics to a file (e.g. JSON) for later phases.
   - **Recommendation:** Print only for Phase 1; file output can be added in a later phase if needed.

3. **“What we did” summary**
   - **Known:** Optional short summary (e.g. in README or as comment block) improves clarity.
   - **Recommendation:** Include a 2–3 line “What we did” in the lesson (top of script or README) so learners can confirm they ran the full pipeline.

## Sources

### Primary (HIGH confidence)
- scikit-learn 1.8.0 install: https://scikit-learn.org/stable/install.html — venv, pip, Python 3.10+ for 1.7+
- load_iris: https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_iris.html — return_X_y, as_frame
- Common pitfalls: https://scikit-learn.org/stable/common_pitfalls.html — split first, fit only on train, pipelines
- Inria MOOC “First model with scikit-learn”: https://inria.github.io/scikit-learn-mooc/python_scripts/02_numerical_pipeline_introduction.html — fit/predict/score, train-test split, .score on test

### Secondary (MEDIUM confidence)
- WebSearch: scikit-learn minimal setup, iris train_test_split, classifier .score = accuracy, notebook vs script for ML tutorial, data leakage prevention — verified against official docs above.

### Tertiary (LOW confidence)
- WebSearch note that “Python 3.11” required: install page states scikit-learn 1.7+ requires Python 3.10+; 3.11 is not a strict minimum for this phase.

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — official install and PROJECT/codebase docs.
- Architecture: HIGH — official API and Inria MOOC pattern.
- Pitfalls: HIGH — official common_pitfalls and data-leakage guidance.

**Research date:** 2026-02-25  
**Valid until:** ~30 days (stack is stable).

---

## RESEARCH COMPLETE

**Phase:** 1 - Foundation  
**Confidence:** HIGH

### Key Findings
- Use scikit-learn with built-in Iris; `train_test_split` then fit on train, `model.score(X_test, y_test)` for accuracy. No preprocessing in Phase 1.
- Script recommended for minimal deps and single-command run (`pip install -r requirements.txt && python lesson1.py`); notebook is optional if Jupyter is acceptable.
- Split-before-fit and “never fit on test” are the only critical rules for this phase; document them to avoid data leakage.
- Minimal requirements: `scikit-learn>=1.5`; add pandas only if lesson uses DataFrames; Python 3.10+.

### File Created
`python-ml-tutorial/.planning/phases/01-foundation/01-RESEARCH.md`

### Confidence Assessment
| Area           | Level | Reason |
|----------------|-------|--------|
| Standard Stack | HIGH  | Official install + PROJECT/codebase alignment |
| Architecture   | HIGH  | Official API and Inria MOOC pattern |
| Pitfalls       | HIGH  | Official common_pitfalls and leakage docs |

### Open Questions
- Notebook vs script: recommend script; planner can choose notebook.
- Output: print accuracy; file output deferred.
- “What we did”: recommend including a short summary in the lesson.

### Ready for Planning
Research complete. Planner can create PLAN.md from this research.
