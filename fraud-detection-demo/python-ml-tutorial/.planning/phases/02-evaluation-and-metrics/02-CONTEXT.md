# Phase 2: Evaluation and metrics — Context

**Gathered:** 2026-02-25
**Status:** Ready for planning

<domain>
## Phase Boundary

Learners go beyond single-number accuracy: add evaluation metrics (precision, recall, F1, confusion matrix) and optionally a simple text-based view of the confusion matrix. Still local, script or notebook; no deployment. Builds on Phase 1 (same Iris dataset and classifier or equivalent). Success = at least one runnable lesson that computes and displays multiple metrics; engineer-oriented.

</domain>

<decisions>
## Implementation Decisions

### Which metrics to include
- Include: accuracy (already in Phase 1), precision, recall, F1 (macro or weighted), and confusion matrix.
- Use scikit-learn: `precision_recall_fscore_support`, `confusion_matrix`, and optionally `classification_report` for a single call that prints a summary.
- No ROC/AUC or learning curves in Phase 2 (can be deferred).

### Output format
- Print metrics to stdout (human-readable: e.g. classification_report text or one line per metric).
- Confusion matrix: print as formatted text (e.g. 2D array or a simple grid); no plotting library required for Phase 2.
- Optional: planner may add writing metrics to a small JSON or text file if it fits "engineer-oriented" and single-command run.

### Reuse vs new artifact
- New script `lesson2.py` (or single notebook) that builds on Phase 1: same Iris, same train/test split and model, then add metric computation. Keeps lesson1.py unchanged so Phase 1 remains a clean "first model" checkpoint.
- Dependencies: add nothing beyond scikit-learn (already in requirements); no pandas required for Phase 2 unless planner prefers it for display.

### Visualization
- No matplotlib/seaborn in Phase 2; confusion matrix as text only. Keeps setup minimal and avoids "run and see numbers" turning into "run and see plot." Defer plot-based visualization to a later phase if desired.

### Claude's Discretion
- Exact ordering of metrics in output; whether to use `classification_report` vs manual precision/recall/F1; confusion matrix layout (e.g. sklearn default print vs custom formatting).
- File output (yes/no and format) if it stays one-command and minimal.

</decisions>

<specifics>
## Specific Ideas

No specific references — open to standard scikit-learn evaluation patterns (classification_report, confusion_matrix).

</specifics>

<deferred>
## Deferred Ideas

- ROC curves, AUC, learning curves — later phase.
- Plotting (matplotlib/seaborn) — later phase if desired.
- Deployment or serving — out of scope for Phase 2.

</deferred>

---
*Phase: 02-evaluation-and-metrics*
*Context gathered: 2026-02-25*
