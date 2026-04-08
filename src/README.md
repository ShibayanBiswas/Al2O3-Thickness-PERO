# Source Code — Architecture & Symbol Discipline

Composable Python modules implement the full **single-input / multi-output** statistical narrative. `run_all.py` orchestrates them; nothing business-critical is hidden in notebooks.

---

## Why the split matters

1. **Integrity layer** — ingest, dtype enforcement, validation (`io_data`, `audit`).
2. **Exploration layer** — distributional + cohort geometry of $(x, \mathbf{y})$ (`eda`).
3. **Inference layer** — regressors $\hat{\mathbf{f}}$, metrics, diagnostics (`models`, `model_eval`, `diagnostics`).
4. **Interpretation layer** — PDP/ICE/sensitivity/SHAP when supported (`explainability`).
5. **Communication layer** — Markdown + tabular synthesis (`report`, `plots`, `viz_style`).

This separation keeps each stage testable and lets you regen figures without rereading raw Excel ad hoc.

---

## Notation bridges code ↔ paper

| Concept | Symbol (docs / GitHub Markdown) | Figure labels |
| --- | --- | --- |
| Thickness | $x$ (nm) | `Al2O3 Thickness_nm` |
| Predicted response | $\hat{y}_j(x)$ or $\hat{\mathbf{y}}(x)$ | Matplotlib mathtext |
| Charge-transfer resistance narrative | $R_{\mathrm{ct}}$ | Same |
| Reversible capacity narrative | $Q_{\mathrm{rev}}$ | Same |
| Goodness-of-fit (in-sample) | $R^2$ | Text metric tables |

Repository Markdown intentionally uses `$...$` so math renders on GitHub; exported PNG/SVG rely on matplotlib’s mathtext interpreter (no external LaTeX required).

---

## Module inventory

| Module | Responsibility |
| --- | --- |
| **`config.py`** | Paths, column spec, run settings, plotting DPI/theme hooks |
| **`io_data.py`** | Excel read (sheet-locked), coercion, validation |
| **`audit.py`** | Compact audit frames + thickness histogram of duplicates |
| **`viz_style.py`** | PERO rcParams, axis polish, legend placement |
| **`plots.py`** | Save helpers + annotation utilities |
| **`eda.py`** | Deep EDA figure+table suite |
| **`models.py`** | Estimator zoo + multi-output wrappers / scaling |
| **`model_eval.py`** | Per-target metrics + leaderboards |
| **`diagnostics.py`** | Residual & calibration geometry per model/target |
| **`explainability.py`** | Permutation drops in $R^2$, PDP/ICE/slope/SHAP |
| **`report.py`** | `summary_report.md` assembly |
| **`logging_config.py`** | Structured logging + warning hygiene |
| **`utils.py`** | Filename safety, robust stats, Excel bundling |
