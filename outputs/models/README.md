# Modeling Outputs And Diagnostics

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

$$
\mathrm{MAE}_j=\frac{1}{n}\sum_i |y_{ij}-\hat{y}_{ij}|,\quad
\mathrm{RMSE}_j=\sqrt{\frac{1}{n}\sum_i (y_{ij}-\hat{y}_{ij})^2},\quad
R^2_j = 1 - \frac{\sum_i(y_{ij}-\hat{y}_{ij})^2}{\sum_i(y_{ij}-\bar{y}_j)^2}.
$$

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

Each algorithm learns a map $\hat{\mathbf{f}}:\mathbb{R}\to\mathbb{R}^4$ from **scalar** $x$ to **four** predicted targets. Training uses **every row** in the table (no default train/test split), so:

- **Metrics** (MAE, RMSE, $R^2$) are **in-sample**: they measure how well $\hat{\mathbf{f}}$ reproduces the observed $(x, \mathbf{y})$ pairs you already fed in.  
- They are **not** automatic certificates of future generalization to new cells or synthesis batches.

**Adjusted $R^2$** penalises extra effective parameters; compare it to plain $R^2$ when choosing between a simple and a flexible estimator.

---

## How to navigate this folder as a student

1. Skim **``tables/model_comparison_overall.csv``** for the global ranking.  
2. Open **``diagnostics_plots/Model Comparison Overall Error.png``** for the same information visually.  
3. For each interesting model, drill into **``diagnostics_plots/<ModelSafe>/<TargetSafe>/``** and read **Residuals vs Thickness** first (strongest link to the physics design).

---

## Honesty check

With one discrete $x$ axis, flexible models can **interpolate cohorts**. High $R^2_j$ plus structured residual-vs-$x$ plots $\Rightarrow$ scrutinize **shape** and **stability**, not only scalar scores. If two models tie on RMSE, prefer the one with **flatter** residuals vs $x$ and more plausible **partial dependence** (see ``../explainability/``).
