# Technology Stack

**Analysis Date:** 2025-02-25

## Languages

**Primary (intended):**
- Python 3.10+ — Tutorial and ML content (from PROJECT.md). No Python files in repo yet.

**Secondary:**
- None. Markdown and JSON only for planning and config.

## Runtime

**Environment:**
- Python 3.10+ (stated in PROJECT.md). No `.python-version` or runtime config in repo.

**Package Manager:**
- pip with venv (PROJECT.md). No `requirements.txt`, `pyproject.toml`, or lockfile present.

## Frameworks

**Core (intended):**
- pandas — Data handling (PROJECT.md).
- scikit-learn — Model training and evaluation (PROJECT.md).
- Optional: PyTorch and/or TensorFlow for deep learning (PROJECT.md).

**Testing (intended):**
- pytest — Standard tooling per PROJECT.md. Not configured in-repo.

**Build/Dev:**
- No build tool detected. Standard tooling: pip/venv, pytest.

## Key Dependencies

**Critical (when implemented):**
- pandas — Data prep and manipulation for labs.
- scikit-learn — Training, evaluation, and deployment patterns.
- (Optional) PyTorch / TensorFlow — If deep-learning phases are added.

**Infrastructure:**
- None. Tutorial scaffold only; no serving or deployment stack in repo.

## Configuration

**Environment:**
- No `.env` or env template. When adding: document required env vars for any external data or APIs.
- Config present: `python-ml-tutorial/config.json` (GSD workflow only).

**Build:**
- No build config. Future: add `pyproject.toml` or `setup.py` if packaging is needed.

## Platform Requirements

**Development:**
- Python 3.10+, pip, venv; optionally Jupyter for notebook-based labs if roadmap includes it.

**Production:**
- Not defined; tutorial focus is learning, not deployment. Deployment patterns may be covered in content later.

---

*Stack analysis: 2025-02-25*
