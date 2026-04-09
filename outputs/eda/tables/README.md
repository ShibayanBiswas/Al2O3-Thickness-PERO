# Exploratory Tables Index

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
- **Correlation** -- $\rho$ and $\rho_s$ matrices + thickness-vs-target vector.

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
| $\rho$, $\rho_s$ | Linear / rank association |

---

## Pedagogical warning

A **high** $|\rho|$ between $x$ and $Y_j$ does **not** imply that a **linear model** will achieve high $R^2$ if the relationship is thresholded or cohort-specific. Treat ``04`` and the heatmaps as **screening tools**, then trust **bivariate plots** and **residual diagnostics** for shape.
