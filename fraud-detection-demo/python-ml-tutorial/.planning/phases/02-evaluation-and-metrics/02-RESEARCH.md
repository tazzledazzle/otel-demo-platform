# Phase 2: Evaluation and metrics — Research

**Researched:** 2026-02-25  
**Domain:** scikit-learn classification metrics (precision, recall, F1, confusion matrix); text-only output  
**Confidence:** HIGH

## Summary

Phase 2 adds evaluation metrics beyond accuracy to the existing Phase 1 pipeline (Iris, train/test split, LogisticRegression). Use **scikit-learn only**: `classification_report`, `precision_recall_fscore_support`, and `confusion_matrix`. Output is **text-only** (stdout); no plotting, no ROC/AUC, no learning curves. A new script **lesson2.py** reuses the same data load, split, and model as lesson1.py, then computes predictions and prints the metrics. Success = one runnable script that prints precision, recall, F1, and a text confusion matrix; engineer-oriented and minimal.

**Primary recommendation:** Implement lesson2.py that (1) duplicates Phase 1 setup (load_iris, train_test_split 0.2 random_state=42, LogisticRegression fit on train), (2) gets `y_pred = model.predict(X_test)`, (3) prints `classification_report(y_test, y_pred, target_names=...)`, (4) prints confusion matrix as text (e.g. raw ndarray or a simple formatted grid). Use `classification_report` for the main metrics in one call; optionally show manual use of `precision_recall_fscore_support` if the planner wants to teach the API. Set `zero_division=0` to avoid UndefinedMetricWarning in edge cases.

<user_constraints>

## User Constraints (from CONTEXT.md and phase goal)

### Locked Decisions
- Metrics: accuracy (from Phase 1), precision, recall, F1, confusion matrix. No ROC/AUC or learning curves.
- scikit-learn only: `classification_report`, `precision_recall_fscore_support`, `confusion_matrix`.
- Text-only output; no plotting (no matplotlib/seaborn).
- New script **lesson2.py** reusing Phase 1: same Iris, same split, same model; then add metric computation.
- Single script flow; engineer-oriented.

### Claude's Discretion
- Order of metrics in output; whether to use `classification_report` vs manual `precision_recall_fscore_support`; confusion matrix layout (default print vs custom formatting).
- Optional: write metrics to a small JSON/text file if it stays one-command and minimal.

### Deferred Ideas (OUT OF SCOPE)
- ROC curves, AUC, learning curves.
- Plotting (matplotlib/seaborn).
- Deployment or serving.

</user_constraints>

## What to Use: sklearn APIs

### 1. classification_report

**Purpose:** Build a text report of precision, recall, F1-score, and support per class, plus accuracy and macro/weighted averages.

**Signature (relevant parameters):**
```text
sklearn.metrics.classification_report(
    y_true, y_pred, *,
    labels=None,
    target_names=None,   # optional display names (e.g. Iris: setosa, versicolor, virginica)
    digits=2,
    output_dict=False,  # if True, returns dict instead of string
    zero_division='warn'
)
```

**Returns:** String (default) or dict when `output_dict=True`.

**Recommendation for lesson2.py:**
- Call with `y_test`, `y_pred`. Use `target_names=iris.target_names` (from `load_iris()` without `return_X_y`) for readable class names.
- Set `zero_division=0` to avoid `UndefinedMetricWarning` when a class has no predictions or no true labels (cleaner for tutorials).
- Default `digits=2` is sufficient. Do not use `output_dict` unless the lesson also writes metrics to file or formats them manually.

**Example (from sklearn docs):**
```python
>>> print(classification_report(y_true, y_pred, target_names=['class 0', 'class 1', 'class 2']))
              precision    recall  f1-score   support
     class 0       0.50      1.00      0.67         1
     class 1       0.00      0.00      0.00         1
     class 2       1.00      0.67      0.80         3
    accuracy                           0.60         5
   macro avg       0.50      0.56      0.49         5
weighted avg       0.70      0.60      0.61         5
```

### 2. precision_recall_fscore_support

**Purpose:** Compute precision, recall, F-beta score, and support per class (or averaged).

**Signature (relevant parameters):**
```text
sklearn.metrics.precision_recall_fscore_support(
    y_true, y_pred, *,
    beta=1.0,
    labels=None,
    average=None | 'binary' | 'micro' | 'macro' | 'weighted' | 'samples',
    zero_division='warn'
)
```

**Returns:** Tuple `(precision, recall, fbeta_score, support)`. When `average` is not None, `support` is None. When `average=None`, each of the first three is an array of shape `[n_labels]`.

**Critical for multiclass (Iris):** Default `average='binary'` is for binary classification only. For Iris (3 classes) either:
- Use `average=None` to get per-class arrays, or
- Use `average='macro'` or `average='weighted'` for a single aggregate (matches classification_report’s macro/weighted avg).

**Recommendation:** Use when the planner wants to teach the low-level API or to print a single aggregate (e.g. “Macro F1: 0.xx”). For a full text report, `classification_report` is simpler and consistent. If using both, prefer one primary (classification_report) and optional secondary (e.g. one line: “Macro F1 from precision_recall_fscore_support: …”).

### 3. confusion_matrix

**Purpose:** Compute the count matrix: rows = true class, columns = predicted class. Entry (i, j) = number of samples with true label i and predicted label j.

**Signature (relevant parameters):**
```text
sklearn.metrics.confusion_matrix(
    y_true, y_pred, *,
    labels=None,
    normalize=None  # or 'true', 'pred', 'all'
)
```

**Returns:** ndarray of shape (n_classes, n_classes). No text formatting; caller must print or format.

**Display as text (no plotting):**
- **Simplest:** `print(confusion_matrix(y_test, y_pred))` — prints the raw ndarray (e.g. 3×3 for Iris).
- **Readable:** Pass `labels` for consistent row/column order (e.g. `labels=[0,1,2]` or use `iris.target_names` indices). Optionally add a header row/column with class names when printing (custom loop or simple string formatting).
- **Do not use:** `ConfusionMatrixDisplay` — that is for matplotlib-based plotting; out of scope for Phase 2.

**Recommendation:** Call `confusion_matrix(y_test, y_pred)`. Print the array; optionally format with a title and (if desired) row/column labels using `target_names` for clarity.

## classification_report vs manual precision_recall_fscore_support

| Aspect | classification_report | precision_recall_fscore_support |
|--------|------------------------|---------------------------------|
| **Output** | Single formatted string (per-class + accuracy + macro/weighted). | Tuple of arrays or scalars; caller formats. |
| **Use case** | One call for “full report” to stdout. | Programmatic use, custom layout, or teaching the API. |
| **Iris (multiclass)** | No extra args for averaging; report includes all. | Must set `average=None` (per-class) or `'macro'`/`'weighted'` (single number). |
| **Recommendation** | **Primary** for lesson2: one print gives precision, recall, F1, support, accuracy, averages. | **Optional**: if planner wants to show “how to get one number” (e.g. macro F1) or to avoid duplication when also writing metrics to file. |

**Planner guidance:** Prefer `classification_report` as the main path; add optional use of `precision_recall_fscore_support` only if the lesson explicitly teaches that API or needs numeric values for file output.

## Confusion matrix display as text

- **Built-in:** `confusion_matrix()` returns an ndarray. `print(cm)` is valid and sufficient for “text-only.”
- **Optional improvement:** Add a short title (e.g. “Confusion matrix:”) and, if desired, a header row/column with class names (e.g. setosa, versicolor, virginica) via simple string formatting or a small loop. No extra libraries.
- **Avoid:** `ConfusionMatrixDisplay`, `plot_confusion_matrix`, or any matplotlib/seaborn — all are for plotting; Phase 2 is text-only.

## Single script lesson2.py flow

1. **Reuse Phase 1 exactly:** Same imports (plus `sklearn.metrics`), same `load_iris(return_X_y=True)`, same `train_test_split(X, y, test_size=0.2, random_state=42)`, same `LogisticRegression(max_iter=200, random_state=42)`, same `fit(X_train, y_train)`.
2. **Predict:** `y_pred = model.predict(X_test)`.
3. **Optional for names:** Load Iris again without `return_X_y` to get `target_names`, or use `load_iris().target_names` once and reuse.
4. **Print metrics (order at planner’s discretion):**  
   - Accuracy: e.g. `model.score(X_test, y_test)` or from report.  
   - Full report: `print(classification_report(y_test, y_pred, target_names=..., zero_division=0))`.  
   - Confusion matrix: `cm = confusion_matrix(y_test, y_pred)` then `print(cm)` (optionally with title/labels).
5. **No file I/O required;** optional small JSON/text export is at planner’s discretion.

Dependencies: scikit-learn only (already in Phase 1). No pandas required for this phase unless the planner uses it for display.

## What to Avoid

| Avoid | Use instead | Reason |
|-------|-------------|--------|
| ROC, AUC, learning curves | Not in Phase 2 | Explicitly out of scope. |
| matplotlib, seaborn, ConfusionMatrixDisplay | Print ndarray or simple formatted text | Phase 2 is text-only. |
| precision_recall_fscore_support with default average for Iris | Use `average=None` or `'macro'`/`'weighted'` | Default is `'binary'`; wrong for 3-class Iris. |
| Leaving zero_division as `'warn'` | `zero_division=0` | Avoids UndefinedMetricWarning when a class has no predictions. |
| Changing Phase 1 (lesson1.py) | New lesson2.py only | Phase 1 remains the clean “first model” checkpoint. |

## Pitfalls

### Pitfall 1: Using average='binary' with multiclass (Iris)
**What goes wrong:** `precision_recall_fscore_support(y_test, y_pred)` uses default `average='binary'`; with 3 classes the result is misleading or may not match expectations.  
**How to avoid:** For Iris, use `average=None` (per-class) or `average='macro'` / `average='weighted'`. Or rely on `classification_report` and skip this function unless needed.

### Pitfall 2: UndefinedMetricWarning (zero division)
**What goes wrong:** If a class has no predictions (precision undefined) or no true labels (recall undefined), sklearn raises UndefinedMetricWarning and may show 0.00.  
**How to avoid:** Pass `zero_division=0` to `classification_report` and `precision_recall_fscore_support` for clean tutorial output.

### Pitfall 3: ConfusionMatrixDisplay for “display”
**What goes wrong:** Using `ConfusionMatrixDisplay.from_predictions()` or similar expects matplotlib; conflicts with “no plotting.”  
**How to avoid:** Use only `confusion_matrix()` and print the returned ndarray (and optionally format with labels).

### Pitfall 4: Inconsistent train/test or model
**What goes wrong:** lesson2.py uses different split or model than lesson1.py, so “reuse Phase 1” is not satisfied.  
**How to avoid:** Copy the same `random_state=42`, `test_size=0.2`, and `LogisticRegression(max_iter=200, random_state=42)` so results are reproducible and comparable.

## Recommendations for the planner

1. **Script:** Single file `lesson2.py`; duplicate Phase 1 setup then add prediction and metric printing. Do not modify `lesson1.py`.
2. **Metrics order:** Suggest: (1) accuracy (optional explicit line), (2) classification_report, (3) confusion matrix. Planner can reorder.
3. **Class names:** Use `load_iris().target_names` for `classification_report` and optionally for confusion matrix headers so output uses setosa/versicolor/virginica instead of 0/1/2.
4. **APIs:** Use `classification_report` as the primary way to show precision, recall, F1, and support. Use `confusion_matrix` and print it. Add `precision_recall_fscore_support` only if the lesson is meant to teach that API or to obtain single numbers for file output.
5. **Robustness:** Use `zero_division=0` in both `classification_report` and `precision_recall_fscore_support` to avoid warnings.
6. **Scope:** No ROC/AUC, no learning curves, no plotting; keep Phase 2 minimal and text-only.

## Code sketch (lesson2.py)

```python
# Same as Phase 1
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix

X, y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = LogisticRegression(max_iter=200, random_state=42)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

# Optional: class names for report and CM
target_names = load_iris().target_names

# Metrics (text-only)
print("Accuracy:", model.score(X_test, y_test))
print(classification_report(y_test, y_pred, target_names=target_names, zero_division=0))
print("Confusion matrix:")
print(confusion_matrix(y_test, y_pred))
```

## Sources

### Primary (HIGH confidence)
- sklearn classification_report: https://scikit-learn.org/stable/modules/generated/sklearn.metrics.classification_report.html  
- sklearn precision_recall_fscore_support: https://scikit-learn.org/stable/modules/generated/sklearn.metrics.precision_recall_fscore_support.html  
- sklearn confusion_matrix: https://scikit-learn.org/stable/modules/generated/sklearn.metrics.confusion_matrix.html  

### Secondary
- Phase 1 implementation: `lesson1.py` (load_iris, train_test_split, LogisticRegression, score).  
- Phase 2 context: `02-CONTEXT.md` (metrics, text-only, lesson2.py, no ROC/plots).

## Metadata

**Confidence:** HIGH — APIs are stable and documented; Phase 1 contract is clear.  
**Valid until:** ~30 days; re-check if sklearn metrics API changes.

---

## RESEARCH COMPLETE

**Phase:** 2 — Evaluation and metrics  
**Confidence:** HIGH  

### Key findings
- **APIs:** Use `classification_report` (primary), `precision_recall_fscore_support` (optional), and `confusion_matrix`; all from `sklearn.metrics`. No ROC/AUC or learning curves.
- **classification_report vs manual:** Prefer `classification_report` for one-shot text report; use `precision_recall_fscore_support` only for teaching that API or for single aggregate values.
- **Confusion matrix:** Print the ndarray from `confusion_matrix()`; optionally add title and class labels. Do not use `ConfusionMatrixDisplay` (plotting).
- **lesson2.py flow:** Reuse Phase 1 (Iris, same split, same model), add `y_pred = model.predict(X_test)`, then print report and confusion matrix; use `zero_division=0` to avoid warnings; use `target_names` for readable class names.

### Ready for planning
Planner can create the Phase 2 plan and tasks for a single runnable `lesson2.py` with text-only evaluation metrics.
