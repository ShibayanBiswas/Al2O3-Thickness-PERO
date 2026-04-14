"""
Canonical Markdown README bodies for everything under outputs/.

Kept in one module so run_all.py and on-disk docs stay aligned without duplicating prose.
"""

from __future__ import annotations

from pathlib import Path

from .config import ProjectPaths
from .utils import ensure_dir


def _w(path: Path, text: str) -> None:
    ensure_dir(path.parent)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def write_output_readme_files(paths: ProjectPaths) -> None:
    """Write every outputs/**/README.md (not summary_report.md; that file is data-driven)."""
    # --- Entire outputs/ tree (navigation hub) ---
    _w(
        paths.outputs_root / "README.md",
        r"""# Outputs -- Full Layout And Contents

Everything here is produced by ``py run_all.py`` (or refreshed in part by ``py postprocess.py``). This README is the **top-level index**: it lists the tree, links to deeper guides, and explains how figures and tables fit into a coherent scientific story.

---

## Suggested reading order (for learning the results)

1. **``eda/tables/README.md``** plus **``eda/plots/README.md``** -- understand the *empirical* thickness--response structure (counts, correlations, cohort summaries, and graphics).  
2. **``models/tables/README.md``** -- scalar fit quality **on the training set**, plus tuning summaries (``tuning_best_params.csv``).  
3. **``models/diagnostics_plots/README.md``** -- *shape* of errors (parity, residuals vs thickness, QQ).  
4. **``explainability/``** -- how the **chosen** best-overall model maps thickness to predictions (PDP/ICE, sensitivity, optional SHAP, permutation table).  
5. **``reports/summary_report.md``** -- compact narrative with the same tables embedded.

Each subdirectory README is written to **teach** what the files mean, not only where they sit on disk.

---

## Visual style (figures)

All Matplotlib exports share the **PERO dark theme** configured in ``src/viz_style.py``:

- **Background** deep navy (``PERO.bg``), **axes** and **grid** tuned for contrast without clutter.  
- **Semantic colours** (also ``PeroPalette`` / ``PERO``): e.g. **sky** for primary data traces, **orange** for residuals and KDE overlays, **green** for cohort / median summaries, **red** for magnitude-of-error emphasis, **text** (mist white) for reference lines and ICE/uncertainty ribbons.  
- **Legends** sit **outside** the plotting region when multiple series appear, so points and bands stay visible.  
- **Mathtext** (STIX) for chemistry and symbols on axes (e.g. $\mathrm{Al}_{2}\mathrm{O}_{3}$, $R_{\mathrm{ct}}$).  
- Default **PNG**, **220 DPI** (``RunConfig.figure_format``, ``RunConfig.figure_dpi`` in ``src/config.py``).

EDA heatmaps use the ``vlag`` diverging map with thin **cell outlines** so tiles read clearly on dark backgrounds.

**Filenames** are sanitized with ``safe_filename()`` so paths are portable; compare stems to this documentation if a column name contained special characters.

---

## Directory tree (canonical)

```
outputs/
├── README.md                          (this file)
├── eda/
│   ├── README.md
│   ├── plots/
│   │   ├── README.md
│   │   ├── Univariate/<VariableTitle>/   (1 folder per feature + each target)
│   │   ├── Bivariate/<TargetTitle>/      (1 folder per electrochemical target)
│   │   ├── Grouped/<TargetTitle>/
│   │   └── Relationships/                (heatmaps + optional pair plot)
│   └── tables/                           (CSV, XLSX, one audit TXT)
├── models/
│   ├── README.md
│   ├── tables/
│   │   └── README.md
│   └── diagnostics_plots/
│       ├── README.md
│       ├── Model Comparison Overall Error.png
│       └── <ModelSafeName>/<TargetSafeName>/
│           ├── Calibration/
│           ├── Residuals/
│           └── Distributions/
├── explainability/
│   ├── README.md
│   ├── plots/
│   │   ├── README.md
│   │   ├── PartialDependence/
│   │   ├── Sensitivity/
│   │   └── Shap/                         (optional; requires SHAP + compatible estimator)
│   └── tables/
│       └── README.md
└── reports/
    ├── README.md
    └── summary_report.md                 (data-driven narrative + tables)
```

---

## Cross-links

| If you need... | Go to |
| --- | --- |
| Raw audit + correlation CSVs | ``eda/tables/README.md`` |
| Plot naming per EDA branch | ``eda/plots/README.md`` and subfolder READMEs |
| Per-model CSV metrics + XLSX | ``models/tables/README.md`` |
| Parity / residual file names | ``models/diagnostics_plots/README.md`` |
| PDP, sensitivity, SHAP file stems | ``explainability/plots/README.md`` |
| Permutation CSV columns | ``explainability/tables/README.md`` |
| Single-report PDF-style summary | ``reports/summary_report.md`` |

---

## Regeneration note

``run_all.py`` **deletes** the previous ``outputs/`` tree before rebuilding. Commit or copy anything you need to keep before re-running.
""",
    )

    # --- EDA root ---
    _w(
        paths.eda_root / "README.md",
        r"""# Exploratory Data Analysis Outputs

Exploratory Data Analysis (EDA) answers: **what does the dataset actually look like** before we commit to a parametric model? Here the experimental design is unusually simple: one controlled input (**Al₂O₃ thickness** $x\ge 0$ nm, column ``Al2O3 Thickness_nm``) and **four** measured outputs (charge-transfer resistance, coulombic efficiency, reversible capacity, capacity retention). EDA therefore focuses on (i) **where data mass lives** (especially $x=0$ vs sparse positive thicknesses), (ii) **how each $Y_j$ varies with $x$** when many points share the same $x$, and (iii) **linear vs rank association** as a first-pass summary, *not* as a substitute for plotting conditional means.

---

## Layout under ``outputs/eda/``

```
eda/
├── README.md                 (this file)
├── plots/                    (see ``plots/README.md`` + branch READMEs)
│   ├── Univariate/
│   ├── Bivariate/
│   ├── Grouped/
│   └── Relationships/
└── tables/                   (see ``tables/README.md``)
```

---

## Working model (descriptive only)

```math
Y_j = g_j(x) + \eta_j,\qquad j=1,\ldots,4,
```

$g_j$ might be smooth, piecewise, or **cohort-dominated** (almost constant within each discrete $x_k$). $\eta_j$ is everything else (measurement noise, batch effects, unmodeled factors). **EDA does not assume** $\mathbb{E}[\eta_j\mid x]=0$; that is a **modeling** assumption diagnosed later under ``outputs/models/diagnostics_plots/``.

---

## Why discrete $x$ matters pedagogically

When many cells share the same thickness, scatter plots **stack vertically**. The pipeline uses **horizontal jitter** so you can see density; a **trend line** or **IQR band by $x$** is then a visual estimate of central tendency and spread *within this sample*, not proof of a physical law. Always cross-check **grouped tables** (``05_...``, ``group_by_thickness__...``) with **Bivariate** and **Grouped** plots.

---

## Pipeline mapping (code references)

| Stage | Source module | What is written |
| --- | --- | --- |
| Audit (00\_\*) | ``run_all.py`` + ``src/audit.py`` | Early tables + ``00_data_audit.xlsx`` |
| Deep EDA | ``src/eda.py`` ``run_deep_eda()`` | ``01``--``09`` CSVs + full plot hierarchy |

---

## How plots and tables reinforce each other

| Question | Start with table | Then open plot folder |
| --- | --- | --- |
| How many rows per thickness? | ``00_`` / ``03_thickness_value_counts.csv`` | (counts are tabular) |
| Pearson/Spearman vs $x$? | ``04_thickness_target_correlations.csv`` | **Bivariate** / **Relationships** |
| Moments by thickness | ``05_...``, ``group_by_thickness__*.csv`` | **Grouped**, **Bivariate** (IQR bands) |
| Full association matrix | ``07_`` / ``08_`` | **Relationships** heatmaps |

---

## Electrochemical shorthand

Figures use mathtext: $R_{\mathrm{ct}}$, $Q_{\mathrm{rev}}$, etc. Markdown in these READMEs uses GitHub ``$...$`` for inline math and fenced math blocks (three backticks + ``math``) for display.
""",
    )

    # --- EDA plots index ---
    _w(
        paths.eda_plots / "README.md",
        r"""# Exploratory Plots Index

High-resolution figures for a **1D input** $\rightarrow$ **4D output** study. Thickness $x$ is ``Al2O3 Thickness_nm``. **Format:** ``.png`` by default (``RunConfig.figure_format``). Folder names come from ``safe_filename(to_title_case(...))``.

Each figure also has a **companion ``*.csv``** with the same stem (where ``save_plot_csv`` is wired in ``src/eda.py``): univariate panels, bivariate/grouped plots, correlation heatmaps, pair-plot data, etc.

Styling is unified through ``apply_pero_theme`` + ``PERO`` palette in ``src/viz_style.py``: primary traces in **sky** blue, secondary overlays (KDE, trends) often in **orange**, cohort summaries in **green**, reference lines in **text** (light), dark navy **background** for print-ready contrast.

---

## Subdirectories (what appears where)

| Folder | Path pattern | What is inside |
| --- | --- | --- |
| **Univariate** | ``Univariate/<VarTitle>/`` | Marginal behaviour of $x$ and each $Y_j$ |
| **Bivariate** | ``Bivariate/<TargetTitle>/`` | $Y_j$ **vs** $x$ with design-aware overlays |
| **Grouped** | ``Grouped/<TargetTitle>/`` | Cohort summaries along discrete $x$ |
| **Relationships** | ``Relationships/`` (flat) | Association across all numeric columns |

``<VarTitle>`` / ``<TargetTitle>`` are filesystem-safe titles (e.g. ``Al2o3 Thickness_nm``, ``Charge Transfer Resistance Initial``).

---

## File stems and how to read them

**Univariate** (each ``<VarTitle>/``):

| File stem (``*.png``) | What it shows | Pedagogical note |
| --- | --- | --- |
| ``Histogram And Kernel Density`` | Normalized histogram + KDE | Skew / multi-modality / mass at boundaries. KDE is a smooth **density estimate**, not a model likelihood. |
| ``Box And Violin`` | Box + violin | Quartiles vs full shape; useful when $n$ per $x$ is small globally but you still need marginal spread. |
| ``Raincloud Plot`` | Violin + box + strip | Shows individual points and density simultaneously (optional). |
| ``Empirical Cumulative Distribution`` | ECDF + smooth | Fraction of data below each value; robust to outliers for **ordering**. |
| ``Scaling Comparison Density`` | Several KDEs after transforms | Compares raw vs scaled versions; requires sklearn scalers when available. |

**Bivariate** (each ``<TargetTitle>/``):

| File stem | What it shows | Pedagogical note |
| --- | --- | --- |
| ``Scatter With Trends`` | Jittered $x$, IQR by thickness, linear trend | Jitter reveals **overlap** at repeated $x$; band describes **sample** spread, not a predictive interval. |
| ``Sorted Profile`` | $Y_j$ sorted by $x$ | Makes non-monotone structure visible; smooth line is a **visual smoother**. |
| ``Residual Pattern`` | Residuals from a linear fit vs $x$ | Persistent trends vs $x$ indicate the conditional mean is not captured by a line (motivates more flexible models). |

**Grouped** (each ``<TargetTitle>/``):

| File stem | What it shows | Pedagogical note |
| --- | --- | --- |
| ``Group Mean With Uncertainty`` | $\bar Y_j \pm s$ by $x$ | Connects discrete cohorts; $s$ is **within-cohort** variability, not uncertainty of the global mean unless assumptions hold. |

**Relationships** (flat):

| File stem | What it shows | Pedagogical note |
| --- | --- | --- |
| ``Correlation Heatmap Pearson`` | Pearson $\rho$ matrix | Linear alignment; weak $\rho$ can still hide strong **nonlinear** $g_j(x)$. |
| ``Correlation Heatmap Spearman`` | Spearman $\rho_{\mathrm{s}}$ | Rank association; more robust to monotone nonlinearity. |
| ``Pair Plot Numeric Variables`` | Pairwise scatter grid | Optional; axis labels shortened to reduce clutter. |

---

## Interpretation checklist

- Repeated $x$ $\Rightarrow$ **jitter** is intentional.  
- Smooth curves $\Rightarrow$ **descriptive** aids, not causal claims.  
- Always pair **plots** with **tables** under ``../tables/`` for exact counts and numeric correlations.
""",
    )

    subs = [
        (
            "Univariate",
            "Marginal laws of $x$ and each $Y_j$: histogram + kernel density, ECDF, box/violin/raincloud, scaling-density overlays.",
            """## Files in each ``<VarTitle>/`` subfolder

Each subfolder is one numeric column (thickness $x$ or a target $Y_j$). Typical stems (``*.png``):

- ``Histogram And Kernel Density`` -- compare **tails** and **modes** across variables; check units mentally using the axis label.
- ``Box And Violin`` -- link **quartiles** (box) to **density** (violin wings).
- ``Raincloud Plot`` (optional) -- every point visible; good for spotting duplicates and outliers.
- ``Empirical Cumulative Distribution`` -- probability mass below a threshold; complements histograms for skewed data.
- ``Scaling Comparison Density`` (optional) -- how transforms change overlap of distributions.

See ``../README.md`` for the master table and column-level interpretation cues.

---

## Study questions (self-quiz)

- Does thickness $x$ concentrate at **0 nm**? Do targets show **heavy tails** or **bounded** support?
- Are univariate shapes **similar** across the four electrochemical targets (suggesting shared noise structure)?""",
        ),
        (
            "Bivariate",
            r"Conditional structure $Y_j \mid x$: jittered scatter, interquartile bands by thickness, linear residual view, sorted profiles.",
            r"""## Files in each ``<TargetTitle>/`` subfolder

Stems (``*.png``):

- ``Scatter With Trends`` -- **start here** for each target: raw pairs $(x, Y_j)$ plus trend overlays and an **IQR tube** per discrete $x$.
- ``Sorted Profile`` -- sorts observations by $x$ so you can **trace** $Y_j$ along the experimental axis even when the scatter is dense.
- ``Residual Pattern`` -- subtracts linear structure; **systematic** residual trends vs $x$ mean the conditional mean is not captured by a line.

**Companion table:** ``../../tables/group_by_thickness__<TargetSafe>.csv`` (exact cohort $n$, mean, std).

---

## Study questions

- At each thickness with multiple cells, is the **within-$x$ spread** large compared to **between-$x$** shifts in the median?
- After viewing ``Residual Pattern``, would you defend a **linear** model for this target, or do you expect **nonlinear** or **step-like** behaviour?""",
        ),
        (
            "Grouped",
            r"Cohort summaries: for each thickness atom $x_k$, means $\bar Y_j$ and $\pm s$ tubes along $x$.",
            """## Files in each ``<TargetTitle>/`` subfolder

- ``Group Mean With Uncertainty.png`` -- connects **cohort means** $\bar Y_j$ at each measured $x_k$ with a tube based on within-group standard deviation $s$.

**Aggregate table (all targets):** ``../../tables/05_grouped_summary_all_targets_by_thickness.csv``.

---

## Study questions

- Does $\bar Y_j$ change **monotonically** with $x$, or are some thicknesses **local optima**?
- Is uncertainty **heteroscedastic** (wider tubes at some $x_k$)? That matters for weighted or robust modelling.""",
        ),
        (
            "Relationships",
            r"Association matrix: heatmaps of $\rho$ and $\rho_{\mathrm{s}}$ plus numeric pair plots (short axis names to avoid clutter).",
            r"""## Files in this folder (flat)

- ``Correlation Heatmap Pearson.png`` -- diverging **vlag** palette, annotated cells, thin grid lines for readability on dark background.
- ``Correlation Heatmap Spearman.png`` -- rank-based analogue; compare to Pearson to detect **nonlinear monotone** coupling.
- ``Pair Plot Numeric Variables.png`` -- optional corner **pairplot**; axis labels shortened deliberately.

**Source matrices:** ``../../tables/07_corr_pearson.csv``, ``08_corr_spearman.csv``.

---

## Study questions

- Which off-diagonal blocks link **thickness** to each target in linear vs rank sense?
- Do any two **targets** correlate strongly with each other (suggesting shared latent cell state beyond $x$)?""",
        ),
    ]
    for name, one_line, files_md in subs:
        _w(
            paths.eda_plots / name / "README.md",
            f"""# {name} Plots

{one_line}

{files_md}

---

## Reading guide

Smooth traces are **visual aids** -- they help the eye; they do not replace formal model checks. In this project’s bivariate views we keep the trend line **linear** and use quantile bands to show conditional spread without overfitting the mean shape.

---

## Figure style in this branch

**Title Case** titles, **outside legends** on multi-series panels, mathtext on axes ($R_{{\\mathrm{{ct}}}}$, $Q_{{\\mathrm{{rev}}}}$, $\\mathrm{{Al}}_{{2}}\\mathrm{{O}}_{{3}}$). Colours follow ``PERO`` in ``src/viz_style.py`` for consistency with modelling and explainability figures.
""",
        )

    # --- EDA tables ---
    _w(
        paths.eda_tables / "README.md",
        r"""# Exploratory Tables Index

CSV / XLSX / TXT under ``outputs/eda/tables/``. Written by ``run_all.py`` (audit) and ``src/eda.py`` ``run_deep_eda()``.

---

## File inventory (exact names)

| File | Origin | Role |
| --- | --- | --- |
| ``00_data_audit_table.csv`` | ``run_all`` + ``audit_dataset`` | Column dtypes, missing counts, min/max, etc. |
| ``00_thickness_value_counts.csv`` | same | Count + fraction per thickness value |
| ``00_duplicates_count.txt`` | same | Single integer: duplicate-row count |
| ``00_data_audit.xlsx`` | ``write_tables_excel`` | Workbook: ``data_audit``, ``thickness_value_counts`` sheets |
| ``01_feature_target_definitions.csv`` | EDA | Rows tagging feature vs each target column |
| ``02_describe_numeric.csv`` | EDA | ``pandas.describe`` (incl. 5/25/50/75/95%) for $x$ + targets |
| ``03_thickness_value_counts.csv`` | EDA | Same conceptual content as ``00_`` (EDA pass); kept for ordered 01--09 series |
| ``04_thickness_target_correlations.csv`` | EDA | ``pearson_r``, ``spearman_r`` vs $x$ per target |
| ``05_grouped_summary_all_targets_by_thickness.csv`` | EDA | Multi-index grouped stats by thickness |
| ``06_zero_vs_nonzero_comparison.csv`` | EDA | $x=0$ vs $x>0$ cohort contrasts per target |
| ``07_corr_pearson.csv`` | EDA | Full Pearson matrix (numeric cols) |
| ``08_corr_spearman.csv`` | EDA | Full Spearman matrix |
| ``09_mutual_information_single_feature.csv`` | EDA | MI($x$, $Y_j$) if sklearn available |
| ``group_by_thickness__<TargetSafe>.csv`` | EDA | Per-target cohort table: count, mean, median, std, min, max |
| ``outliers__<NameSafe>.csv`` | EDA | IQR + z-score outlier counts, skew, kurtosis per series |

---

## Core blocks (conceptual)

- **Audit & counts** -- dtypes, missingness, thickness mass at $x=0$.
- **Cohort tables** -- moments stratified by each observed $x_k$.
- **Contrasts** -- ``0`` nm vs pooled $x>0$ (diagnostic, not causal).
- **Correlation** -- $\rho$ and $\rho_{\mathrm{s}}$ matrices + thickness-vs-target vector.

---

## Row-by-row guide (how to use each numbered file)

| File | Read it when you need to... |
| --- | --- |
| ``01_feature_target_definitions.csv`` | Confirm which columns are treated as **input** vs **outputs** in code. |
| ``02_describe_numeric.csv`` | Quote **min / max / quantiles** in text; sanity-check units and outliers. |
| ``03_thickness_value_counts.csv`` | Know **effective sample size** per thickness level for EDA and modelling. |
| ``04_thickness_target_correlations.csv`` | Report a **single-number** association of $x$ with each $Y_j$ (with caveats). |
| ``05_grouped_summary_all_targets_by_thickness.csv`` | Build tables of $\bar Y_j$, std, count **per** $x_k$ for all targets at once. |
| ``06_zero_vs_nonzero_comparison.csv`` | Describe how the **large zero-thickness cohort** differs from pooled positives. |
| ``07_`` / ``08_`` | Access full **numeric correlation** matrices for secondary analysis. |
| ``09_mutual_information_single_feature.csv`` | See a nonlinear dependence score between $x$ and each $Y_j$ (if sklearn ran). |

Per-target cohort CSVs ``group_by_thickness__*.csv`` duplicate part of ``05`` in a **long** layout friendly for plotting one response at a time. ``outliers__*.csv`` summarises IQR/z-score flags **per series** for data cleaning discussions.

---

## Symbol cheat sheet

| Symbol | Meaning |
| --- | --- |
| $x$ | Thickness (nm), ``Al2O3 Thickness_nm`` |
| $Y_j$ | Target $j$ of four |
| $\rho$, $\rho_{\mathrm{s}}$ | Linear / rank association |

---

## Pedagogical warning

A **high** $|\rho|$ between $x$ and $Y_j$ does **not** imply that a **linear model** will achieve high $R^2$ if the relationship is thresholded or cohort-specific. Treat ``04`` and the heatmaps as **screening tools**, then trust **bivariate plots** and **residual diagnostics** for shape.
""",
    )

    # --- Models root ---
    _w(
        paths.models_root / "README.md",
        r"""# Modeling Outputs And Diagnostics

Multi-output regressors $\hat{\mathbf{y}}(x)\in\mathbb{R}^4$ fitted on the **full sample** (no routine holdout). Column ``Al2O3 Thickness_nm`` is the only feature. Written by ``run_all.py`` (loop over ``build_model_suite()`` in ``src/models.py``) plus ``src/diagnostics.py`` and ``src/model_eval.py``.

---

## Layout under ``outputs/models/``

```
models/
├── README.md                 (this file)
├── tables/                   (see ``tables/README.md``)
└── diagnostics_plots/        (see ``diagnostics_plots/README.md``)
    ├── Model Comparison Overall Error.png
    └── <ModelSafe>/<TargetSafe>/
        ├── Calibration/
        ├── Residuals/
        └── Distributions/
```

``<ModelSafe>`` and ``<TargetSafe>`` are ``safe_filename()`` of the registered model name and raw target column name (same convention as on-disk paths in ``run_all.py``).

---

## In-sample metrics

For target $j$, with predictions $\hat{y}_{ij}$ and truths $y_{ij}$, $i=1,\ldots,n$:

```math
\mathrm{MAE}_j=\frac{1}{n}\sum_i |y_{ij}-\hat{y}_{ij}|,\quad
\mathrm{RMSE}_j=\sqrt{\frac{1}{n}\sum_i (y_{ij}-\hat{y}_{ij})^2},\quad
R^2_j = 1 - \frac{\sum_i(y_{ij}-\hat{y}_{ij})^2}{\sum_i(y_{ij}-\bar{y}_j)^2}.
```

These quantify **fit to the tabulated rows**, not guaranteed out-of-sample generalization.

---

## Pipeline touchpoints

| Step | Code | Output |
| --- | --- | --- |
| Fit + predict | ``run_all.py`` | One folder tree per $(\text{model}, Y_j)$ under ``diagnostics_plots/`` |
| Metrics CSV | ``src/model_eval.py`` | ``metrics__<ModelSafe>.csv`` |
| Leaderboard | ``src/model_eval.py`` ``rank_models`` | ``model_comparison_overall.csv`` + bar chart PNG |
| Excel bundle | ``write_tables_excel`` | ``all_model_metrics.xlsx`` |

``py postprocess.py`` can rebuild comparison / best-model tables from existing ``metrics__*.csv`` without refitting.

---

## Supervised learning in this project (tutorial)

Each algorithm learns a map $\hat{\mathbf{f}}:\mathbb{R}\to\mathbb{R}^4$ from **scalar** $x$ to **four** predicted targets. The pipeline now uses a **train split**, and all plots are computed from **training data only**, so:

- **Training metrics** (MAE, RMSE, $R^2$) measure how well $\hat{\mathbf{f}}$ reproduces the observed training pairs $(x, \mathbf{y})$.
- **Cross-validation** tables add an out-of-fold estimate of generalization (within the limits of small $n$).
- They are **not** automatic certificates of future generalization to new cells or synthesis batches.

**Adjusted** $R^2$ penalises extra effective parameters; compare it to plain $R^2$ when choosing between a simple and a flexible estimator.

---

## How to navigate this folder as a student

1. Skim **``tables/model_comparison_overall.csv``** for the global ranking.  
2. Open **``diagnostics_plots/Model Comparison Overall Error.png``** for the same information visually.  
3. For each interesting model, drill into **``diagnostics_plots/<ModelSafe>/<TargetSafe>/``** and read **Residuals vs Thickness** first (strongest link to the physics design).

---

## Honesty check

With one discrete $x$ axis, flexible models can **interpolate cohorts**. High $R^2_j$ plus structured residual-vs-$x$ plots $\Rightarrow$ scrutinize **shape** and **stability**, not only scalar scores. If two models tie on RMSE, prefer the one with **flatter** residuals vs $x$ and more plausible **partial dependence** (see ``../explainability/``).
""",
    )

    _w(
        paths.models_tables / "README.md",
        r"""# Modeling Tables Index

Machine-readable **training-set** scores for every fitted estimator, plus hyperparameter tuning summaries. Produced in ``run_all.py``; ``postprocess.py`` can regenerate the aggregate files from ``metrics__*.csv``.

---

## File inventory

| File | Description |
| --- | --- |
| ``metrics__<ModelSafe>.csv`` | One row per target plus a synthetic row ``target == OVERALL_MEAN`` (mean of per-target metrics). ``<ModelSafe>`` matches ``safe_filename(model.name)``. |
| ``model_comparison_overall.csv`` | One row per successfully fit model; sorted by overall RMSE. |
| ``tuning_best_params.csv`` | Best hyperparameters found by randomized tuning (one row per model; columns are parameter keys). Includes the primary CV mean $R^2$ used by the tuner. |
| ``model_comparison_cv_r2.csv`` | A compact leaderboard sorted by tuned primary-CV mean $R^2$ (descending). |
| ``best_model_per_target.csv`` | Argmin of RMSE over models, separately for each target column. |
| ``all_model_metrics.xlsx`` | Workbook: sheets ``model_comparison_overall``, ``best_model_per_target``, and ``metrics__<ModelName>`` per model. Sheet names pass through ``safe_sheet_name()`` in ``src/utils.py`` (Excel max 31 characters; ``: \\ / ? * [ ]`` removed). |

---

## Columns: ``metrics__*.csv`` (from ``compute_metrics_per_target`` + ``summarize_overall``)

| Column | Meaning |
| --- | --- |
| ``target`` | Electrochemical column name, or ``OVERALL_MEAN`` for the pooled row |
| ``MAE``, ``MSE``, ``RMSE`` | Standard sklearn-style errors |
| ``R2``, ``Adj_R2`` | Coefficient of determination and adjusted form ($p$ from the model spec) |
| ``MAPE_percent`` | Percent MAPE where defined (safe for zeros via ``safe_mape``) |
| ``MedianAE`` | Median absolute error |
| ``ExplainedVariance`` | Explained variance score |

---

## Metric definitions (math; matches ``src/model_eval.py``)

For each target $j$ with observations $y_{ij}$ and predictions $\hat y_{ij}$, define residuals:

```math
\hat\varepsilon_{ij} = y_{ij}-\hat y_{ij}.
```
Then

```math
\mathrm{MAE}_j = \frac{1}{n}\sum_i |\hat\varepsilon_{ij}|,\qquad
\mathrm{MSE}_j = \frac{1}{n}\sum_i \hat\varepsilon_{ij}^2,\qquad
\mathrm{RMSE}_j = \sqrt{\mathrm{MSE}_j}.
```
Coefficient of determination (training):

```math
R^2_j = 1 - \frac{\sum_i \hat\varepsilon_{ij}^2}{\sum_i (y_{ij}-\bar y_j)^2}.
```
Adjusted $R^2$ (with effective feature count $p$ used by the model spec):

```math
R^2_{j,\mathrm{adj}} = 1 - (1-R^2_j)\frac{n-1}{n-p-1}.
```
MAPE (as implemented via ``safe_mape`` with a stabilizer $\varepsilon$):

```math
\mathrm{MAPE}_j = 100\cdot \frac{1}{n}\sum_i \frac{|\hat\varepsilon_{ij}|}{\max(|y_{ij}|,\varepsilon)}.
```
Explained variance score:

```math
\mathrm{EV}_j = 1 - \frac{\mathrm{Var}(y_j-\hat y_j)}{\mathrm{Var}(y_j)}.
```

---

## Columns: ``model_comparison_overall.csv`` (from ``rank_models``)

| Column | Meaning |
| --- | --- |
| ``model`` | Estimator display name |
| ``OVERALL_MAE``, ``OVERALL_RMSE``, ``OVERALL_R2``, ``OVERALL_Adj_R2``, ``OVERALL_MAPE_percent`` | Taken from the ``OVERALL_MEAN`` row of each model's metrics table |
| ``rank_by_overall_rmse`` | 1 = best (lowest overall RMSE) |

---

## Columns: ``best_model_per_target.csv``

| Column | Meaning |
| --- | --- |
| ``target`` | Raw target column name |
| ``best_model_by_rmse`` | Model name achieving lowest RMSE on that target |
| ``RMSE``, ``R2`` | In-sample scores for that best model on that target |

---

## Equations (residual form)

```math
\hat\varepsilon_{ij} = y_{ij}-\hat{y}_{ij},\qquad
\mathrm{RMSE}_j=\sqrt{\frac{1}{n}\sum_{i=1}^{n}\hat\varepsilon_{ij}^2}.
```
Pair tables with ``../diagnostics_plots/`` for thickness-structured residuals.

---

## Interpreting the numbers (quick reference)

| Metric | Plain-language meaning | Typical pitfall |
| --- | --- | --- |
| MAE | Average absolute error in the same units as $Y_j$ | Can hide occasional large errors |
| RMSE | Penalises **large** errors more than MAE | Dominated by outliers if present |
| $R^2$ | Fraction of variance of $Y_j$ explained **in sample** | Can be high with cohort interpolation |
| MAPE | Relative error notion (percent) | Unstable if $y$ crosses zero |
| MedianAE | Robust central error | Does not summarise tail risk |

The **``OVERALL_MEAN``** row inside each ``metrics__*.csv`` averages these quantities across the four targets so you can rank **multi-output** models with one line per model in ``model_comparison_overall.csv``.
""",
    )

    _w(
        paths.models_diagnostics_plots / "README.md",
        r"""# Modeling Diagnostics Plots Index

**Layout:** ``diagnostics_plots/<ModelSafe>/<TargetSafe>/`` with three subfolders --- **Calibration**, **Residuals**, **Distributions** --- plus one **flat** leaderboard figure at the root of ``diagnostics_plots/``.

Naming: each figure stem is passed through ``safe_filename()`` in ``savefig()`` (``src/plots.py``). Below, ``__<base>`` means ``__`` concatenated with ``<ModelSafe>__<TargetSafe>`` as built in ``diagnostic_plots_per_target()`` (``src/diagnostics.py``).

For every exported ``*.png`` in this tree, the pipeline also writes a **matching ``*.csv``** (same stem, tidy long rows) next to the figure via ``save_plot_csv()`` --- use it to rebuild tables or overlay data in another tool.

---

## Root of ``diagnostics_plots/`` (flat)

| File stem (``*.png`` / ``*.csv``) | Content |
| --- | --- |
| ``Model Comparison Overall Error`` | Horizontal bar chart of top models by ``OVERALL_RMSE`` (from ``consolidated_model_comparison_plot``); CSV lists the same bar series. |

---

## Under ``<ModelSafe>/<TargetSafe>/Calibration/``

| File stem pattern | Content |
| --- | --- |
| ``Parity Plot__<ModelSafe>__<TargetSafe>`` | Actual vs predicted; parity line + optional $\pm$std band |
| ``Sorted Actual And Predicted__<ModelSafe>__<TargetSafe>`` | Order statistics of $y$ vs $\hat{y}$ (distributional alignment) |

---

## Under ``.../Residuals/``

| File stem pattern | Content |
| --- | --- |
| ``Residuals Versus Predicted__...`` | $\hat\varepsilon$ vs $\hat{y}$ |
| ``Residuals Versus Actual__...`` | $\hat\varepsilon$ vs $y$ |
| ``Residuals Versus Thickness__...`` | $\hat\varepsilon$ vs $x$ (primary stress test for 1D design) |
| ``Absolute Error Versus Thickness__...`` | $|\hat\varepsilon|$ vs $x$ |

---

## Under ``.../Distributions/``

| File stem pattern | Content |
| --- | --- |
| ``Residual Distribution__...`` | Histogram + KDE of $\hat\varepsilon$ |
| ``Residual Box Plot__...`` | Box summary of $\hat\varepsilon$ |
| ``QQ Plot__...`` | Normal QQ (statsmodels or scipy fallback) |
| ``Predicted And Actual Density__...`` | Overlaid KDE (or histogram fallback) of $y$ vs $\hat{y}$ |

---

## Reading guide

**Parity** --- $\hat{y}$ vs $y$; reference line and band.

**Residuals vs $x$** --- any trend with thickness flags curvature / cohort effects not absorbed by the fit.

**QQ** --- gentle read at $n=51$.

All multi-series panels use **outside legends** (PERO theme).

---

## Diagnostic catalogue (what each plot type teaches)

| Category | Plot family | Ideal (simplified) appearance | Red flag |
| --- | --- | --- | --- |
| Calibration | Parity | Points hug the **diagonal** | Systematic curve above/below diagonal |
| Calibration | Sorted actual vs predicted | Two curves **track** each other | Growing gap vs sorted index |
| Residuals | vs predicted / actual | **Cloud** centred on 0 | Funnel shape (heteroscedasticity) |
| Residuals | vs thickness $x$ | No **trend** | Smooth trend $\Rightarrow$ structure unexplained by model |
| Magnitude | $|\hat\varepsilon|$ vs $x$ | Flat or random | Certain thicknesses always worse |
| Distribution | Residual KDE / QQ | QQ roughly on reference | Heavy tails or skew in residuals |
| Distribution | Predicted vs actual KDE | Overlapping modes | Systematic shift or width mismatch |

At $n=51$, treat QQ and fine-grained density features as **suggestive**, not definitive; thickness-residual plots carry more design-specific weight.

---

## Colour cues (aligned with ``PERO``)

- **Sky** scatter: paired $(y, \hat{y})$ or primary series.  
- **Orange**: residual clouds vs fitted values or $x$.  
- **Red**: absolute error emphasis vs $x$.  
- **Green / sky** pairing: sorted actual vs sorted predicted curves.
""",
    )

    _w(
        paths.explain_root / "README.md",
        r"""# Explainability Outputs

Interpretation of how **Al₂O₃ thickness** $x$ (``Al2O3 Thickness_nm``) steers the **best-overall** model (lowest mean RMSE across targets), refit on the full sample in ``run_all.py`` via ``run_explainability()`` (``src/explainability.py``).

---

## Layout under ``outputs/explainability/``

```
explainability/
├── README.md           (this file)
├── plots/
│   ├── README.md
│   ├── PartialDependence/
│   ├── Sensitivity/
│   └── Shap/           (optional; requires `shap` + compatible estimator)
└── tables/
    └── README.md
```

---

## Objects

**Permutation importance** -- positive drop in $R^2$ when $x$ is shuffled:

```math
\Delta R^{2} = R^{2}(\text{data}) - R^{2}(\pi \circ x).
```

**PDP / ICE** -- mean response vs $x$ plus bootstrap ensemble of univariate prediction curves (ICE band).

**Sensitivity** -- $\hat{y}(x)$ and numerical $\mathrm{d}\hat{y}/\mathrm{d}x$ on a dense grid.

---

## SHAP (optional): no waterfalls

When SHAP applies,

```math
\hat{y}(x) \approx \mathbb{E}[\hat{y}] + \phi(x).
```

We export **beeswarm**, **bar**, **dependence** only -- **no waterfall figures**. Per-target clones are fit for multi-output models. All SHAP panels use **outside legends** (PERO theme).

---

## Why explainability still matters when $p=1$

With only one feature, some global methods (SHAP for many inputs) collapse to triviality, but **curve-based** views remain essential:

- **PDP / ICE** show how the **fitted** response $\hat{y}_j(x)$ changes along the measured thickness range, including **uncertainty ribbons** from bootstrap refits.  
- **Sensitivity** plots expose $\mathrm{d}\hat{y}_j/\mathrm{d}x$, highlighting regions where the learned map is **steep** (small nm changes imply large predicted response changes).  
- **Permutation importance** asks whether **destroying** the ordering of $x$ while keeping its marginal values collapses $R^2$; large drops mean the model relied on the actual pairing $(x, y)$ in the spreadsheet.

These tools describe the **trained estimator**, not necessarily a physical mechanism.

---

## Relationship to modelling outputs

Explainability is run for the **best overall** model (lowest mean RMSE across targets) after refitting on all data. For other models, use **their** diagnostics under ``outputs/models/diagnostics_plots/<ModelSafe>/`` and compare PDP shapes mentally or re-run a custom script if needed.
""",
    )

    _w(
        paths.explain_plots / "README.md",
        r"""# Explainability Plots Index

Each graphic studies $\hat{y}:\mathbb{R}_{\ge0}\to\mathbb{R}$ **per target** for the champion model. Stems are built in ``src/explainability.py`` and saved with ``savefig()``, so the **full stem** (including the target suffix) is normalized by ``safe_filename()``.

PDP/ICE and sensitivity figures already ship **``*.csv``** next to the ``*.png``; SHAP stems (``shap_*``) also have matching CSVs when SHAP runs successfully.

Convention below: ``<TargetRaw>`` is the **exact** target column string from the dataset; on disk it appears as ``safe_filename("...__" + <TargetRaw>)`` merged into one stem.

---

## ``PartialDependence/`` (from ``pdp_ice_1d``)

| File stem pattern (``*.png``) | Role |
| --- | --- |
| ``Partial Dependence And ICE__<TargetRaw>`` | Solid PDP line, optional ICE quantile band from bootstrap refits, filled response area |

Legend title: **PDP / ICE**.

---

## ``Sensitivity/`` (from ``local_sensitivity_curve``)

| File stem pattern | Role |
| --- | --- |
| ``Sensitivity Curve__<TargetRaw>`` | Upper: $\hat{y}(x)$ with optional bootstrap ribbon; lower: $\mathrm{d}\hat{y}/\mathrm{d}x$ |

Legend titles: **Response** (top), **Sensitivity** (bottom).

---

## ``Shap/`` (from ``shap_explain_1d_single_output``; may be empty)

| File stem pattern | Role |
| --- | --- |
| ``shap_beeswarm__<TargetRaw>`` | Jittered $x$ vs SHAP $\phi$, smoothed trend |
| ``shap_bar__<TargetRaw>`` | Single bar: $\mathbb{E}[|\phi|]$ for the one feature |
| ``shap_dependence__<TargetRaw>`` | Dependence-style $\phi$ vs $x$ |

Legend title: **Attribution**. **No waterfall plots.**

---

## How to read each graphic type

- **PDP line** -- the fitted model's prediction $\hat{y}_j(x)$ on a dense thickness grid (smoothed for display).  
- **ICE band** -- quantiles of **bootstrap-refitted** prediction curves; wide bands mean the map is **sensitive** to which rows are in the training draw (interpret cautiously at $n=51$).  
- **Sensitivity** -- derivative of the **smooth** prediction curve; spikes may sit where support is thin.  
- **SHAP panels** -- attribute **local** deviations from the baseline prediction to the single feature; with $p=1$, dependence and beeswarm largely **re-express** $\hat{y}(x)$ and residuals of the explainer.

---

## Note on filenames

If a target name contains parentheses or special characters, compare against the **actual** files on disk --- ``safe_filename`` maps those to spaces/underscores while keeping the stem human-readable.
""",
    )

    _w(
        paths.explain_tables / "README.md",
        r"""# Explainability Tables Index

Single CSV written by ``permutation_importance_single_feature()`` in ``src/explainability.py`` when the call succeeds.

---

## File

| File | Role |
| --- | --- |
| ``permutation_importance_single_feature.csv`` | One row per target: Monte Carlo mean/std of $\Delta R^2$ from shuffling $x$ |

---

## Columns

| Column | Meaning |
| --- | --- |
| ``target`` | Target column name |
| ``feature`` | Shuffled column (always the thickness feature, first column of $X$) |
| ``r2_drop_mean`` | Mean of $R^2_{\text{full}} - R^2_{\text{permuted}}$ over repeats |
| ``r2_drop_std`` | Sample std of that drop (``ddof=1``) |
| ``n_repeats`` | Number of permutations (``run_all`` uses 120) |

---

## Definition

For target $j$,

```math
\Delta R^{2}_j = R^{2}_j - R^{2}_j(\pi),
```

with $\pi$ a random permutation of the thickness column.

---

## How to read

| $\Delta R^{2}_j$ | Reading |
| --- | --- |
| Large | Fit leans on authentic ordering of $x$ |
| Tiny | Thickness weak on the training sample or noise-dominated |

Pair with PDP/ICE and (if present) SHAP $|\phi|$ --- tables encode **stability**, curves encode **shape**.

---

## Connecting table values to plots

| CSV signal | Where to look |
| --- | --- |
| Large ``r2_drop_mean`` for target $j$ | ``../plots/PartialDependence/`` and ``../plots/Sensitivity/`` for that target |
| Small drop for every target | Check whether base $R^2$ in ``outputs/models/tables/`` was already modest |
| High ``r2_drop_std`` | Uncertain importance; read ICE / bootstrap ribbons as **intervals**, not point truth |

---

## Statistical intuition

Permutation destroys **joint structure** $(x, y)$ while preserving the **marginal** histogram of $x$. If predictions barely change, the fitted map did not rely on which row carried which thickness --- either the signal is weak or the estimator is too rigid to use $x$.
""",
    )

    _w(
        paths.reports_root / "README.md",
        r"""# Reports

Narrative Markdown for **thesis appendices**, **supervisor updates**, or **supplementary documentation**. ``summary_report.md`` is generated by ``write_summary_report_md()`` in ``src/report.py`` from tables already written under ``outputs/eda/tables/`` and ``outputs/models/tables/``.

It is **not** a substitute for the folder READMEs: those explain *every* artifact class; the summary report gives a **linear read** with the key tables inlined.

---

## Main file

| File | Role |
| --- | --- |
| ``summary_report.md`` | Single self-contained narrative + embedded Markdown tables (regenerated each full pipeline run) |

---

## Section outline (matches ``write_summary_report_md``)

| # | Section | Educational purpose |
| --- | --- | --- |
| 1 | Title | Identifies the study and branding (PERO). |
| 2 | Notation | Defines $x$, $\mathbf{y}$, and states the **full-sample** fitting policy explicitly. |
| 3 | Data integrity | Shows **where data live** in thickness space (counts, zero group). |
| 4 | EDA correlations | First-pass **linear and rank** association of thickness with each target. |
| 5 | Zero vs non-zero | Highlights the **largest cohort** vs positives (diagnostic contrast). |
| 6 | Modeling | Leaderboard + **best** models; ties narrative to CSVs in ``models/tables/``. |
| 7 | Interpretation | Connects statistics to **physics intuition** (1D design, residuals vs $x$). |
| 8 | Metric definitions | Formal equations for MAE, RMSE, $R^2$ consistent with ``model_eval.py``. |

---

## How to cite alongside figures

When writing prose, reference **specific** PNGs by path (e.g. ``outputs/models/diagnostics_plots/.../Residuals Versus Thickness__...png``) and **anchor** claims with the matching CSV (metrics or grouped summaries). The summary report is the **bridge paragraph**; the README hierarchy is the **encyclopedia**.

---

## Notation (GitHub)

Use ``$...$`` for inline math and a fenced math block (three backticks + ``math``) for display. Example:

```math
\hat\varepsilon_{ij} = y_{ij} - \hat{y}_{ij}.
```

Exported figures use Matplotlib mathtext ($R_{\mathrm{ct}}$, $Q_{\mathrm{rev}}$, $\mathrm{Al}_{2}\mathrm{O}_{3}$).

---

## PERO

**Polished, export-ready, reproducible, organized** -- every artifact has a named home and a stated inferential role.
""",
    )
