# Exploratory Plots Index

High-resolution figures for a **1D input** $\rightarrow$ **4D output** study. Thickness $x$ is ``Al2O3 Thickness_nm``. **Format:** ``.png`` by default (``RunConfig.figure_format``). Folder names come from ``safe_filename(to_title_case(...))``.

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
| ``Residual Pattern`` | Residuals from linear vs cubic fits vs $x$ | If cubic residuals still trend with $x$, a low-order polynomial is insufficient (motivates flexible models). |

**Grouped** (each ``<TargetTitle>/``):

| File stem | What it shows | Pedagogical note |
| --- | --- | --- |
| ``Group Mean With Uncertainty`` | $\bar Y_j \pm s$ by $x$ | Connects discrete cohorts; **$s$** is within-cohort variability, not uncertainty of the global mean unless assumptions hold. |

**Relationships** (flat):

| File stem | What it shows | Pedagogical note |
| --- | --- | --- |
| ``Correlation Heatmap Pearson`` | Pearson $\rho$ matrix | Linear alignment; weak $\rho$ can still hide strong **nonlinear** $g_j(x)$. |
| ``Correlation Heatmap Spearman`` | Spearman $\rho_s$ | Rank association; more robust to monotone nonlinearity. |
| ``Pair Plot Numeric Variables`` | Pairwise scatter grid | Optional; axis labels shortened to reduce clutter. |

---

## Interpretation checklist

- Repeated $x$ $\Rightarrow$ **jitter** is intentional.  
- Smooth curves $\Rightarrow$ **descriptive** aids, not causal claims.  
- Always pair **plots** with **tables** under ``../tables/`` for exact counts and numeric correlations.
