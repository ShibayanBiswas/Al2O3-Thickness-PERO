# Al₂O₃ Thickness → Multi-Output Electrochemical Response

A **PERO-grade** workflow (polished, export-ready, reproducible, organized) for quantifying how a single deposition parameter—**`Al2O3 Thickness_nm`**—tracks four coupled battery figures of merit.

---

## Problem geometry (mathematical frame)

Treat thickness as a scalar design coordinate $x$ (nanometers) and the measurements as a vector response

$$
\mathbf{y}(x) =
\bigl(
y_{\mathrm{R_{ct}}},\;
y_{\mathrm{ICE}},\;
y_{Q_{\mathrm{rev}}},\;
y_{\mathrm{retention}}
\bigr)^{\!\top}
\in \mathbb{R}^{4}.
$$

Each algorithmic competitor estimates a map $\hat{\mathbf{f}} : x \mapsto \widehat{\mathbf{y}}$ under the project constraint **$p=1$ feature**. Core inferential objects are therefore **univariate response curves** $\hat{y}_j(x)$, their curvature, residual structure versus $x$, and local sensitivities $\mathrm{d}\hat{y}_j / \mathrm{d}x$—not high-dimensional attribution games.

> **Markdown math on GitHub:** this repository uses `$...$` (inline) and `$$...$$` (display). Plot labels use Matplotlib mathtext with the same symbols (e.g. $R_{\mathrm{ct}}$, $Q_{\mathrm{rev}}$).

---

## Targets (outputs)

| Column | Role |
| --- | --- |
| `Rct_initial_ohm` | Proxy for interfacial kinetics ($R_{\mathrm{ct}}$ narrative) |
| `ICE_percent` | Initial Coulombic efficiency |
| `Initial Reversible Capacity_mAh_g at 0.1C` | Reversible lithiation capacity ($Q_{\mathrm{rev}}$ narrative) |
| `Highest Capacity Retention_percent` | Cyclability ceiling |

---

## Hard data & modeling constraints

| Rule | Statement |
| --- | --- |
| Source | `Data/Data.xlsx`, sheet **`Dataset`** only |
| Ignored | `Sample` identifier column |
| Feature space | **`Al2O3 Thickness_nm` exclusively** |
| Training regime | **100% of rows** for final fits (no routine train/test split) |
| Metrics | **In-sample** diagnostics unless explicitly noted |

---

## Quickstart

### Environment

```bash
python -m pip install -r requirements.txt
```

On Windows with multiple interpreters:

```bash
py -m pip install -r requirements.txt
```

### Full pipeline (EDA → models → diagnostics → explainability → reports)

```bash
py run_all.py
```

Artifacts land under `outputs/` (plots, tables, Markdown reports, per-folder READMEs).

**Incremental refresh** after manual edits to metric CSVs:

```bash
py postprocess.py
```

---

## Deliverables

- **`run_all.py`** — end-to-end regeneration (clears `outputs/` first).
- **`postprocess.py`** — revises comparisons / explainability / summary from saved `metrics__*.csv`.
- **`src/`** — modular library: I/O, EDA, models, diagnostics, explainability, reporting.
- **`outputs/**`** — hierarchical exports; each major directory carries a README interpretive index.

---

## Repository cartography

### Root

| Path | Purpose |
| --- | --- |
| `README.md` | Scientific framing, constraints, navigation (this file) |
| `requirements.txt` | Locked third-party stack |
| `run_all.py` / `postprocess.py` | Executable entry points |
| `logs/pipeline.log` | Structured run transcript (see logging configuration) |

### Data

| Path | Purpose |
| --- | --- |
| `Data/Data.xlsx` | Canonical workbook |
| `Data/README.md` | Provenance + schema discipline |

### Source modules (`src/`)

See **`src/README.md`** for the full module digest (`config`, `io_data`, `eda`, `models`, `diagnostics`, `explainability`, …).

### Outputs (generated)

```
outputs/
  eda/          plots/, tables/, README.md
  models/       diagnostics_plots/, tables/, README.md
  explainability/
  reports/      summary_report.md, README.md
```

Nested README files document naming conventions, statistical intent, and how to cite each figure class without ambiguity.

---

## Documentation map

- **`Data/README.md`** — sheet policy, column contract, discrete-thickness cautions.
- **`src/README.md`** — architectural decomposition & symbol conventions.
- **`outputs/**/README.md`** — folder-local curator notes (auto-written by `run_all.py`).

---

## Optional dependencies

SHAP, XGBoost, LightGBM, and CatBoost are **autodetected**. Missing libraries simply elide their sections; the pipeline continues.

---

## Figure quality

All raster/vector exports honor a unified dark PERO theme—publication contrast, consistent typographic scale, and math-aware axis labels suitable for thesis or journal submission.
