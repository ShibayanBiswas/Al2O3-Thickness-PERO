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
---

## Appendix: Study Questions And Interpretation Prompts

This appendix is a deliberately long-form learning scaffold. Each prompt is designed to force you to connect **a specific file on disk** (a table or a figure) to a **mathematical object** (a curve, a residual, a score) and then to a **scientific claim** you could defend in writing. Treat it as an oral-exam checklist.

### 1. For target $R_{\mathrm{ct}}$ (Rct_initial_ohm): State the scientific question being answered and the operational definition used in the pipeline.

Answer using the pipeline’s notation: thickness is \(x\) (nm), outcomes are \(Y_j\), predictions are \(\hat y_j(x)\), residuals are \(\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}\). When you reference a metric, state its definition (e.g. \(\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum\hat\varepsilon^2}\)) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 2. For target $R_{\mathrm{ct}}$ (Rct_initial_ohm): Identify what is treated as input \(x\) and what is treated as output \(Y_j\).

Answer using the pipeline’s notation: thickness is \(x\) (nm), outcomes are \(Y_j\), predictions are \(\hat y_j(x)\), residuals are \(\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}\). When you reference a metric, state its definition (e.g. \(\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum\hat\varepsilon^2}\)) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 3. For target $R_{\mathrm{ct}}$ (Rct_initial_ohm): Explain what it would mean (in words) if the relationship is cohort-dominated rather than smooth.

Answer using the pipeline’s notation: thickness is \(x\) (nm), outcomes are \(Y_j\), predictions are \(\hat y_j(x)\), residuals are \(\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}\). When you reference a metric, state its definition (e.g. \(\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum\hat\varepsilon^2}\)) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 4. For target $R_{\mathrm{ct}}$ (Rct_initial_ohm): Describe one plausible mechanism and one non-mechanistic confound that could produce the observed pattern.

Answer using the pipeline’s notation: thickness is \(x\) (nm), outcomes are \(Y_j\), predictions are \(\hat y_j(x)\), residuals are \(\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}\). When you reference a metric, state its definition (e.g. \(\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum\hat\varepsilon^2}\)) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 5. For target $R_{\mathrm{ct}}$ (Rct_initial_ohm): Write down the residual definition \(\hat\varepsilon = y-\hat y\) and interpret its sign in context.

Answer using the pipeline’s notation: thickness is \(x\) (nm), outcomes are \(Y_j\), predictions are \(\hat y_j(x)\), residuals are \(\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}\). When you reference a metric, state its definition (e.g. \(\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum\hat\varepsilon^2}\)) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 6. For target $R_{\mathrm{ct}}$ (Rct_initial_ohm): Explain why in-sample metrics can be optimistic when thickness is discrete and models can interpolate cohorts.

Answer using the pipeline’s notation: thickness is \(x\) (nm), outcomes are \(Y_j\), predictions are \(\hat y_j(x)\), residuals are \(\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}\). When you reference a metric, state its definition (e.g. \(\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum\hat\varepsilon^2}\)) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 7. For target $R_{\mathrm{ct}}$ (Rct_initial_ohm): Describe how you would validate stability if you were allowed to collect more thickness levels.

Answer using the pipeline’s notation: thickness is \(x\) (nm), outcomes are \(Y_j\), predictions are \(\hat y_j(x)\), residuals are \(\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}\). When you reference a metric, state its definition (e.g. \(\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum\hat\varepsilon^2}\)) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 8. For target $\mathrm{ICE}$ (ICE_percent): State the scientific question being answered and the operational definition used in the pipeline.

Answer using the pipeline’s notation: thickness is \(x\) (nm), outcomes are \(Y_j\), predictions are \(\hat y_j(x)\), residuals are \(\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}\). When you reference a metric, state its definition (e.g. \(\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum\hat\varepsilon^2}\)) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 9. For target $\mathrm{ICE}$ (ICE_percent): Identify what is treated as input \(x\) and what is treated as output \(Y_j\).

Answer using the pipeline’s notation: thickness is \(x\) (nm), outcomes are \(Y_j\), predictions are \(\hat y_j(x)\), residuals are \(\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}\). When you reference a metric, state its definition (e.g. \(\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum\hat\varepsilon^2}\)) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 10. For target $\mathrm{ICE}$ (ICE_percent): Explain what it would mean (in words) if the relationship is cohort-dominated rather than smooth.

Answer using the pipeline’s notation: thickness is \(x\) (nm), outcomes are \(Y_j\), predictions are \(\hat y_j(x)\), residuals are \(\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}\). When you reference a metric, state its definition (e.g. \(\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum\hat\varepsilon^2}\)) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 11. For target $\mathrm{ICE}$ (ICE_percent): Describe one plausible mechanism and one non-mechanistic confound that could produce the observed pattern.

Answer using the pipeline’s notation: thickness is \(x\) (nm), outcomes are \(Y_j\), predictions are \(\hat y_j(x)\), residuals are \(\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}\). When you reference a metric, state its definition (e.g. \(\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum\hat\varepsilon^2}\)) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 12. For target $\mathrm{ICE}$ (ICE_percent): Write down the residual definition \(\hat\varepsilon = y-\hat y\) and interpret its sign in context.

Answer using the pipeline’s notation: thickness is \(x\) (nm), outcomes are \(Y_j\), predictions are \(\hat y_j(x)\), residuals are \(\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}\). When you reference a metric, state its definition (e.g. \(\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum\hat\varepsilon^2}\)) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 13. For target $\mathrm{ICE}$ (ICE_percent): Explain why in-sample metrics can be optimistic when thickness is discrete and models can interpolate cohorts.

Answer using the pipeline’s notation: thickness is \(x\) (nm), outcomes are \(Y_j\), predictions are \(\hat y_j(x)\), residuals are \(\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}\). When you reference a metric, state its definition (e.g. \(\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum\hat\varepsilon^2}\)) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 14. For target $\mathrm{ICE}$ (ICE_percent): Describe how you would validate stability if you were allowed to collect more thickness levels.

Answer using the pipeline’s notation: thickness is \(x\) (nm), outcomes are \(Y_j\), predictions are \(\hat y_j(x)\), residuals are \(\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}\). When you reference a metric, state its definition (e.g. \(\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum\hat\varepsilon^2}\)) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 15. For target $Q_{\mathrm{rev}}$ (Initial Reversible Capacity): State the scientific question being answered and the operational definition used in the pipeline.

Answer using the pipeline’s notation: thickness is \(x\) (nm), outcomes are \(Y_j\), predictions are \(\hat y_j(x)\), residuals are \(\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}\). When you reference a metric, state its definition (e.g. \(\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum\hat\varepsilon^2}\)) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 16. For target $Q_{\mathrm{rev}}$ (Initial Reversible Capacity): Identify what is treated as input \(x\) and what is treated as output \(Y_j\).

Answer using the pipeline’s notation: thickness is \(x\) (nm), outcomes are \(Y_j\), predictions are \(\hat y_j(x)\), residuals are \(\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}\). When you reference a metric, state its definition (e.g. \(\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum\hat\varepsilon^2}\)) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 17. For target $Q_{\mathrm{rev}}$ (Initial Reversible Capacity): Explain what it would mean (in words) if the relationship is cohort-dominated rather than smooth.

Answer using the pipeline’s notation: thickness is \(x\) (nm), outcomes are \(Y_j\), predictions are \(\hat y_j(x)\), residuals are \(\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}\). When you reference a metric, state its definition (e.g. \(\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum\hat\varepsilon^2}\)) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 18. For target $Q_{\mathrm{rev}}$ (Initial Reversible Capacity): Describe one plausible mechanism and one non-mechanistic confound that could produce the observed pattern.

Answer using the pipeline’s notation: thickness is \(x\) (nm), outcomes are \(Y_j\), predictions are \(\hat y_j(x)\), residuals are \(\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}\). When you reference a metric, state its definition (e.g. \(\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum\hat\varepsilon^2}\)) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 19. For target $Q_{\mathrm{rev}}$ (Initial Reversible Capacity): Write down the residual definition \(\hat\varepsilon = y-\hat y\) and interpret its sign in context.

Answer using the pipeline’s notation: thickness is \(x\) (nm), outcomes are \(Y_j\), predictions are \(\hat y_j(x)\), residuals are \(\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}\). When you reference a metric, state its definition (e.g. \(\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum\hat\varepsilon^2}\)) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 20. For target $Q_{\mathrm{rev}}$ (Initial Reversible Capacity): Explain why in-sample metrics can be optimistic when thickness is discrete and models can interpolate cohorts.

Answer using the pipeline’s notation: thickness is \(x\) (nm), outcomes are \(Y_j\), predictions are \(\hat y_j(x)\), residuals are \(\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}\). When you reference a metric, state its definition (e.g. \(\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum\hat\varepsilon^2}\)) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 21. For target $Q_{\mathrm{rev}}$ (Initial Reversible Capacity): Describe how you would validate stability if you were allowed to collect more thickness levels.

Answer using the pipeline’s notation: thickness is \(x\) (nm), outcomes are \(Y_j\), predictions are \(\hat y_j(x)\), residuals are \(\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}\). When you reference a metric, state its definition (e.g. \(\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum\hat\varepsilon^2}\)) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 22. For target Retention (Highest Capacity Retention_percent): State the scientific question being answered and the operational definition used in the pipeline.

Answer using the pipeline’s notation: thickness is \(x\) (nm), outcomes are \(Y_j\), predictions are \(\hat y_j(x)\), residuals are \(\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}\). When you reference a metric, state its definition (e.g. \(\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum\hat\varepsilon^2}\)) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 23. For target Retention (Highest Capacity Retention_percent): Identify what is treated as input \(x\) and what is treated as output \(Y_j\).

Answer using the pipeline’s notation: thickness is \(x\) (nm), outcomes are \(Y_j\), predictions are \(\hat y_j(x)\), residuals are \(\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}\). When you reference a metric, state its definition (e.g. \(\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum\hat\varepsilon^2}\)) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 24. For target Retention (Highest Capacity Retention_percent): Explain what it would mean (in words) if the relationship is cohort-dominated rather than smooth.

Answer using the pipeline’s notation: thickness is \(x\) (nm), outcomes are \(Y_j\), predictions are \(\hat y_j(x)\), residuals are \(\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}\). When you reference a metric, state its definition (e.g. \(\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum\hat\varepsilon^2}\)) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 25. For target Retention (Highest Capacity Retention_percent): Describe one plausible mechanism and one non-mechanistic confound that could produce the observed pattern.

Answer using the pipeline’s notation: thickness is \(x\) (nm), outcomes are \(Y_j\), predictions are \(\hat y_j(x)\), residuals are \(\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}\). When you reference a metric, state its definition (e.g. \(\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum\hat\varepsilon^2}\)) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 26. For target Retention (Highest Capacity Retention_percent): Write down the residual definition \(\hat\varepsilon = y-\hat y\) and interpret its sign in context.

Answer using the pipeline’s notation: thickness is \(x\) (nm), outcomes are \(Y_j\), predictions are \(\hat y_j(x)\), residuals are \(\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}\). When you reference a metric, state its definition (e.g. \(\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum\hat\varepsilon^2}\)) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 27. For target Retention (Highest Capacity Retention_percent): Explain why in-sample metrics can be optimistic when thickness is discrete and models can interpolate cohorts.

Answer using the pipeline’s notation: thickness is \(x\) (nm), outcomes are \(Y_j\), predictions are \(\hat y_j(x)\), residuals are \(\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}\). When you reference a metric, state its definition (e.g. \(\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum\hat\varepsilon^2}\)) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 28. For target Retention (Highest Capacity Retention_percent): Describe how you would validate stability if you were allowed to collect more thickness levels.

Answer using the pipeline’s notation: thickness is \(x\) (nm), outcomes are \(Y_j\), predictions are \(\hat y_j(x)\), residuals are \(\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}\). When you reference a metric, state its definition (e.g. \(\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum\hat\varepsilon^2}\)) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 29. For the univariate distribution family: what visual feature would count as 'structure' rather than noise at n=51?

Answer using the pipeline’s notation: thickness is \(x\) (nm), outcomes are \(Y_j\), predictions are \(\hat y_j(x)\), residuals are \(\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}\). When you reference a metric, state its definition (e.g. \(\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum\hat\varepsilon^2}\)) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 30. For the univariate distribution family: list two failure modes (plotting or statistical) that can mislead interpretation.

Answer using the pipeline’s notation: thickness is \(x\) (nm), outcomes are \(Y_j\), predictions are \(\hat y_j(x)\), residuals are \(\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}\). When you reference a metric, state its definition (e.g. \(\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum\hat\varepsilon^2}\)) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 31. For the bivariate scatter-with-trends family: what visual feature would count as 'structure' rather than noise at n=51?

Answer using the pipeline’s notation: thickness is \(x\) (nm), outcomes are \(Y_j\), predictions are \(\hat y_j(x)\), residuals are \(\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}\). When you reference a metric, state its definition (e.g. \(\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum\hat\varepsilon^2}\)) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 32. For the bivariate scatter-with-trends family: list two failure modes (plotting or statistical) that can mislead interpretation.

Answer using the pipeline’s notation: thickness is \(x\) (nm), outcomes are \(Y_j\), predictions are \(\hat y_j(x)\), residuals are \(\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}\). When you reference a metric, state its definition (e.g. \(\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum\hat\varepsilon^2}\)) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 33. For the grouped mean with uncertainty family: what visual feature would count as 'structure' rather than noise at n=51?

Answer using the pipeline’s notation: thickness is \(x\) (nm), outcomes are \(Y_j\), predictions are \(\hat y_j(x)\), residuals are \(\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}\). When you reference a metric, state its definition (e.g. \(\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum\hat\varepsilon^2}\)) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 34. For the grouped mean with uncertainty family: list two failure modes (plotting or statistical) that can mislead interpretation.

Answer using the pipeline’s notation: thickness is \(x\) (nm), outcomes are \(Y_j\), predictions are \(\hat y_j(x)\), residuals are \(\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}\). When you reference a metric, state its definition (e.g. \(\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum\hat\varepsilon^2}\)) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 35. For the correlation heatmaps (Pearson/Spearman) family: what visual feature would count as 'structure' rather than noise at n=51?

Answer using the pipeline’s notation: thickness is \(x\) (nm), outcomes are \(Y_j\), predictions are \(\hat y_j(x)\), residuals are \(\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}\). When you reference a metric, state its definition (e.g. \(\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum\hat\varepsilon^2}\)) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 36. For the correlation heatmaps (Pearson/Spearman) family: list two failure modes (plotting or statistical) that can mislead interpretation.

Answer using the pipeline’s notation: thickness is \(x\) (nm), outcomes are \(Y_j\), predictions are \(\hat y_j(x)\), residuals are \(\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}\). When you reference a metric, state its definition (e.g. \(\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum\hat\varepsilon^2}\)) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 37. For the parity (actual vs predicted) family: what visual feature would count as 'structure' rather than noise at n=51?

Answer using the pipeline’s notation: thickness is \(x\) (nm), outcomes are \(Y_j\), predictions are \(\hat y_j(x)\), residuals are \(\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}\). When you reference a metric, state its definition (e.g. \(\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum\hat\varepsilon^2}\)) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 38. For the parity (actual vs predicted) family: list two failure modes (plotting or statistical) that can mislead interpretation.

Answer using the pipeline’s notation: thickness is \(x\) (nm), outcomes are \(Y_j\), predictions are \(\hat y_j(x)\), residuals are \(\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}\). When you reference a metric, state its definition (e.g. \(\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum\hat\varepsilon^2}\)) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 39. For the residuals vs thickness family: what visual feature would count as 'structure' rather than noise at n=51?

Answer using the pipeline’s notation: thickness is \(x\) (nm), outcomes are \(Y_j\), predictions are \(\hat y_j(x)\), residuals are \(\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}\). When you reference a metric, state its definition (e.g. \(\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum\hat\varepsilon^2}\)) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 40. For the residuals vs thickness family: list two failure modes (plotting or statistical) that can mislead interpretation.

Answer using the pipeline’s notation: thickness is \(x\) (nm), outcomes are \(Y_j\), predictions are \(\hat y_j(x)\), residuals are \(\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}\). When you reference a metric, state its definition (e.g. \(\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum\hat\varepsilon^2}\)) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 41. For the residual distribution and QQ family: what visual feature would count as 'structure' rather than noise at n=51?

Answer using the pipeline’s notation: thickness is \(x\) (nm), outcomes are \(Y_j\), predictions are \(\hat y_j(x)\), residuals are \(\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}\). When you reference a metric, state its definition (e.g. \(\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum\hat\varepsilon^2}\)) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 42. For the residual distribution and QQ family: list two failure modes (plotting or statistical) that can mislead interpretation.

Answer using the pipeline’s notation: thickness is \(x\) (nm), outcomes are \(Y_j\), predictions are \(\hat y_j(x)\), residuals are \(\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}\). When you reference a metric, state its definition (e.g. \(\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum\hat\varepsilon^2}\)) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 43. For the PDP/ICE family: what visual feature would count as 'structure' rather than noise at n=51?

Answer using the pipeline’s notation: thickness is \(x\) (nm), outcomes are \(Y_j\), predictions are \(\hat y_j(x)\), residuals are \(\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}\). When you reference a metric, state its definition (e.g. \(\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum\hat\varepsilon^2}\)) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 44. For the PDP/ICE family: list two failure modes (plotting or statistical) that can mislead interpretation.

Answer using the pipeline’s notation: thickness is \(x\) (nm), outcomes are \(Y_j\), predictions are \(\hat y_j(x)\), residuals are \(\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}\). When you reference a metric, state its definition (e.g. \(\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum\hat\varepsilon^2}\)) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 45. For the local sensitivity family: what visual feature would count as 'structure' rather than noise at n=51?

Answer using the pipeline’s notation: thickness is \(x\) (nm), outcomes are \(Y_j\), predictions are \(\hat y_j(x)\), residuals are \(\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}\). When you reference a metric, state its definition (e.g. \(\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum\hat\varepsilon^2}\)) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 46. For the local sensitivity family: list two failure modes (plotting or statistical) that can mislead interpretation.

Answer using the pipeline’s notation: thickness is \(x\) (nm), outcomes are \(Y_j\), predictions are \(\hat y_j(x)\), residuals are \(\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}\). When you reference a metric, state its definition (e.g. \(\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum\hat\varepsilon^2}\)) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 47. For the permutation importance family: what visual feature would count as 'structure' rather than noise at n=51?

Answer using the pipeline’s notation: thickness is \(x\) (nm), outcomes are \(Y_j\), predictions are \(\hat y_j(x)\), residuals are \(\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}\). When you reference a metric, state its definition (e.g. \(\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum\hat\varepsilon^2}\)) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 48. For the permutation importance family: list two failure modes (plotting or statistical) that can mislead interpretation.

Answer using the pipeline’s notation: thickness is \(x\) (nm), outcomes are \(Y_j\), predictions are \(\hat y_j(x)\), residuals are \(\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}\). When you reference a metric, state its definition (e.g. \(\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum\hat\varepsilon^2}\)) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 49. For the SHAP beeswarm / dependence (optional) family: what visual feature would count as 'structure' rather than noise at n=51?

Answer using the pipeline’s notation: thickness is \(x\) (nm), outcomes are \(Y_j\), predictions are \(\hat y_j(x)\), residuals are \(\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}\). When you reference a metric, state its definition (e.g. \(\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum\hat\varepsilon^2}\)) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 50. For the SHAP beeswarm / dependence (optional) family: list two failure modes (plotting or statistical) that can mislead interpretation.

Answer using the pipeline’s notation: thickness is \(x\) (nm), outcomes are \(Y_j\), predictions are \(\hat y_j(x)\), residuals are \(\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}\). When you reference a metric, state its definition (e.g. \(\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum\hat\varepsilon^2}\)) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 51. Trace the exact file path(s) you would open to answer the question; include the README index you would consult first. (outputs/models/)

Answer using the pipeline’s notation: thickness is \(x\) (nm), outcomes are \(Y_j\), predictions are \(\hat y_j(x)\), residuals are \(\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}\). When you reference a metric, state its definition (e.g. \(\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum\hat\varepsilon^2}\)) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 52. Explain how file naming uses safe_filename() and why that matters when target names contain punctuation. (outputs/models/)

Answer using the pipeline’s notation: thickness is \(x\) (nm), outcomes are \(Y_j\), predictions are \(\hat y_j(x)\), residuals are \(\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}\). When you reference a metric, state its definition (e.g. \(\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum\hat\varepsilon^2}\)) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 53. Describe a minimal 'repro run': commands, what gets deleted, and which outputs are regenerated. (outputs/models/)

Answer using the pipeline’s notation: thickness is \(x\) (nm), outcomes are \(Y_j\), predictions are \(\hat y_j(x)\), residuals are \(\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}\). When you reference a metric, state its definition (e.g. \(\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum\hat\varepsilon^2}\)) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 54. Explain how the pipeline separates machine-readable tables (CSV/XLSX) from human-readable narratives (Markdown). (outputs/models/)

Answer using the pipeline’s notation: thickness is \(x\) (nm), outcomes are \(Y_j\), predictions are \(\hat y_j(x)\), residuals are \(\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}\). When you reference a metric, state its definition (e.g. \(\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum\hat\varepsilon^2}\)) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

---

## Appendix: Reproducibility Checklist

- Confirm the workbook is `Data/Data.xlsx` and the sheet policy is followed (Dataset sheet only).
- Confirm the feature is exactly `Al2O3 Thickness_nm` and the sample-id column is ignored.
- Run `py run_all.py` from the repository root; note that it deletes the previous `outputs/` tree.
- Verify that each `outputs/**/README.md` exists and matches the directory inventory described there.
- When comparing runs, prefer comparing **tables** (CSV) first, then figures (PNG) second.
- If optional libraries (SHAP, XGBoost, LightGBM, CatBoost) are missing, confirm the pipeline degrades gracefully.
