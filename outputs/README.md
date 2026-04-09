# Outputs -- Full Layout And Contents

Everything here is produced by ``py run_all.py`` (or refreshed in part by ``py postprocess.py``). This README is the **top-level index**: it lists the tree, links to deeper guides, and explains how figures and tables fit into a coherent scientific story.

---

## Suggested reading order (for learning the results)

1. **``eda/tables/README.md``** plus **``eda/plots/README.md``** -- understand the *empirical* thickness--response structure (counts, correlations, cohort summaries, and graphics).  
2. **``models/tables/README.md``** -- scalar fit quality (in-sample) for every candidate model.  
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
---

## Appendix: Study Questions And Interpretation Prompts

This appendix is a deliberately long-form learning scaffold. Each prompt is designed to force you to connect **a specific file on disk** (a table or a figure) to a **mathematical object** (a curve, a residual, a score) and then to a **scientific claim** you could defend in writing. Treat it as an oral-exam checklist.

### 1. For target $R_{\mathrm{ct}}$ (`Rct_initial_ohm`): State the scientific question being answered and the operational definition used in the pipeline.

Answer using the pipeline’s notation: thickness is $x$ (nm), outcomes are $Y_j$, predictions are $\hat y_j(x)$, residuals are $\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}$. When you reference a metric, state its definition (e.g. $\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum \hat\varepsilon^2}$) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 2. For target $R_{\mathrm{ct}}$ (`Rct_initial_ohm`): Identify what is treated as input $x$ and what is treated as output $Y_j$.

Answer using the pipeline’s notation: thickness is $x$ (nm), outcomes are $Y_j$, predictions are $\hat y_j(x)$, residuals are $\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}$. When you reference a metric, state its definition (e.g. $\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum \hat\varepsilon^2}$) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 3. For target $R_{\mathrm{ct}}$ (`Rct_initial_ohm`): Explain what it would mean (in words) if the relationship is cohort-dominated rather than smooth.

Answer using the pipeline’s notation: thickness is $x$ (nm), outcomes are $Y_j$, predictions are $\hat y_j(x)$, residuals are $\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}$. When you reference a metric, state its definition (e.g. $\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum \hat\varepsilon^2}$) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 4. For target $R_{\mathrm{ct}}$ (`Rct_initial_ohm`): Describe one plausible mechanism and one non-mechanistic confound that could produce the observed pattern.

Answer using the pipeline’s notation: thickness is $x$ (nm), outcomes are $Y_j$, predictions are $\hat y_j(x)$, residuals are $\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}$. When you reference a metric, state its definition (e.g. $\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum \hat\varepsilon^2}$) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 5. For target $R_{\mathrm{ct}}$ (`Rct_initial_ohm`): Write down the residual definition $\hat\varepsilon = y-\hat y$ and interpret its sign in context.

Answer using the pipeline’s notation: thickness is $x$ (nm), outcomes are $Y_j$, predictions are $\hat y_j(x)$, residuals are $\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}$. When you reference a metric, state its definition (e.g. $\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum \hat\varepsilon^2}$) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 6. For target $R_{\mathrm{ct}}$ (`Rct_initial_ohm`): Explain why in-sample metrics can be optimistic when thickness is discrete and models can interpolate cohorts.

Answer using the pipeline’s notation: thickness is $x$ (nm), outcomes are $Y_j$, predictions are $\hat y_j(x)$, residuals are $\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}$. When you reference a metric, state its definition (e.g. $\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum \hat\varepsilon^2}$) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 7. For target $R_{\mathrm{ct}}$ (`Rct_initial_ohm`): Describe how you would validate stability if you were allowed to collect more thickness levels.

Answer using the pipeline’s notation: thickness is $x$ (nm), outcomes are $Y_j$, predictions are $\hat y_j(x)$, residuals are $\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}$. When you reference a metric, state its definition (e.g. $\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum \hat\varepsilon^2}$) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 8. For target $\mathrm{ICE}$ (`ICE_percent`): State the scientific question being answered and the operational definition used in the pipeline.

Answer using the pipeline’s notation: thickness is $x$ (nm), outcomes are $Y_j$, predictions are $\hat y_j(x)$, residuals are $\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}$. When you reference a metric, state its definition (e.g. $\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum \hat\varepsilon^2}$) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 9. For target $\mathrm{ICE}$ (`ICE_percent`): Identify what is treated as input $x$ and what is treated as output $Y_j$.

Answer using the pipeline’s notation: thickness is $x$ (nm), outcomes are $Y_j$, predictions are $\hat y_j(x)$, residuals are $\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}$. When you reference a metric, state its definition (e.g. $\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum \hat\varepsilon^2}$) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 10. For target $\mathrm{ICE}$ (`ICE_percent`): Explain what it would mean (in words) if the relationship is cohort-dominated rather than smooth.

Answer using the pipeline’s notation: thickness is $x$ (nm), outcomes are $Y_j$, predictions are $\hat y_j(x)$, residuals are $\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}$. When you reference a metric, state its definition (e.g. $\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum \hat\varepsilon^2}$) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 11. For target $\mathrm{ICE}$ (`ICE_percent`): Describe one plausible mechanism and one non-mechanistic confound that could produce the observed pattern.

Answer using the pipeline’s notation: thickness is $x$ (nm), outcomes are $Y_j$, predictions are $\hat y_j(x)$, residuals are $\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}$. When you reference a metric, state its definition (e.g. $\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum \hat\varepsilon^2}$) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 12. For target $\mathrm{ICE}$ (`ICE_percent`): Write down the residual definition $\hat\varepsilon = y-\hat y$ and interpret its sign in context.

Answer using the pipeline’s notation: thickness is $x$ (nm), outcomes are $Y_j$, predictions are $\hat y_j(x)$, residuals are $\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}$. When you reference a metric, state its definition (e.g. $\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum \hat\varepsilon^2}$) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 13. For target $\mathrm{ICE}$ (`ICE_percent`): Explain why in-sample metrics can be optimistic when thickness is discrete and models can interpolate cohorts.

Answer using the pipeline’s notation: thickness is $x$ (nm), outcomes are $Y_j$, predictions are $\hat y_j(x)$, residuals are $\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}$. When you reference a metric, state its definition (e.g. $\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum \hat\varepsilon^2}$) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 14. For target $\mathrm{ICE}$ (`ICE_percent`): Describe how you would validate stability if you were allowed to collect more thickness levels.

Answer using the pipeline’s notation: thickness is $x$ (nm), outcomes are $Y_j$, predictions are $\hat y_j(x)$, residuals are $\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}$. When you reference a metric, state its definition (e.g. $\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum \hat\varepsilon^2}$) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 15. For target $Q_{\mathrm{rev}}$ (`Initial Reversible Capacity_mAh_g at 0.1C`): State the scientific question being answered and the operational definition used in the pipeline.

Answer using the pipeline’s notation: thickness is $x$ (nm), outcomes are $Y_j$, predictions are $\hat y_j(x)$, residuals are $\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}$. When you reference a metric, state its definition (e.g. $\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum \hat\varepsilon^2}$) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 16. For target $Q_{\mathrm{rev}}$ (`Initial Reversible Capacity_mAh_g at 0.1C`): Identify what is treated as input $x$ and what is treated as output $Y_j$.

Answer using the pipeline’s notation: thickness is $x$ (nm), outcomes are $Y_j$, predictions are $\hat y_j(x)$, residuals are $\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}$. When you reference a metric, state its definition (e.g. $\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum \hat\varepsilon^2}$) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 17. For target $Q_{\mathrm{rev}}$ (`Initial Reversible Capacity_mAh_g at 0.1C`): Explain what it would mean (in words) if the relationship is cohort-dominated rather than smooth.

Answer using the pipeline’s notation: thickness is $x$ (nm), outcomes are $Y_j$, predictions are $\hat y_j(x)$, residuals are $\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}$. When you reference a metric, state its definition (e.g. $\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum \hat\varepsilon^2}$) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 18. For target $Q_{\mathrm{rev}}$ (`Initial Reversible Capacity_mAh_g at 0.1C`): Describe one plausible mechanism and one non-mechanistic confound that could produce the observed pattern.

Answer using the pipeline’s notation: thickness is $x$ (nm), outcomes are $Y_j$, predictions are $\hat y_j(x)$, residuals are $\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}$. When you reference a metric, state its definition (e.g. $\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum \hat\varepsilon^2}$) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 19. For target $Q_{\mathrm{rev}}$ (`Initial Reversible Capacity_mAh_g at 0.1C`): Write down the residual definition $\hat\varepsilon = y-\hat y$ and interpret its sign in context.

Answer using the pipeline’s notation: thickness is $x$ (nm), outcomes are $Y_j$, predictions are $\hat y_j(x)$, residuals are $\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}$. When you reference a metric, state its definition (e.g. $\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum \hat\varepsilon^2}$) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 20. For target $Q_{\mathrm{rev}}$ (`Initial Reversible Capacity_mAh_g at 0.1C`): Explain why in-sample metrics can be optimistic when thickness is discrete and models can interpolate cohorts.

Answer using the pipeline’s notation: thickness is $x$ (nm), outcomes are $Y_j$, predictions are $\hat y_j(x)$, residuals are $\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}$. When you reference a metric, state its definition (e.g. $\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum \hat\varepsilon^2}$) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 21. For target $Q_{\mathrm{rev}}$ (`Initial Reversible Capacity_mAh_g at 0.1C`): Describe how you would validate stability if you were allowed to collect more thickness levels.

Answer using the pipeline’s notation: thickness is $x$ (nm), outcomes are $Y_j$, predictions are $\hat y_j(x)$, residuals are $\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}$. When you reference a metric, state its definition (e.g. $\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum \hat\varepsilon^2}$) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 22. For target $\mathrm{Retention}$ (`Highest Capacity Retention_percent`): State the scientific question being answered and the operational definition used in the pipeline.

Answer using the pipeline’s notation: thickness is $x$ (nm), outcomes are $Y_j$, predictions are $\hat y_j(x)$, residuals are $\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}$. When you reference a metric, state its definition (e.g. $\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum \hat\varepsilon^2}$) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 23. For target $\mathrm{Retention}$ (`Highest Capacity Retention_percent`): Identify what is treated as input $x$ and what is treated as output $Y_j$.

Answer using the pipeline’s notation: thickness is $x$ (nm), outcomes are $Y_j$, predictions are $\hat y_j(x)$, residuals are $\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}$. When you reference a metric, state its definition (e.g. $\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum \hat\varepsilon^2}$) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 24. For target $\mathrm{Retention}$ (`Highest Capacity Retention_percent`): Explain what it would mean (in words) if the relationship is cohort-dominated rather than smooth.

Answer using the pipeline’s notation: thickness is $x$ (nm), outcomes are $Y_j$, predictions are $\hat y_j(x)$, residuals are $\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}$. When you reference a metric, state its definition (e.g. $\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum \hat\varepsilon^2}$) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 25. For target $\mathrm{Retention}$ (`Highest Capacity Retention_percent`): Describe one plausible mechanism and one non-mechanistic confound that could produce the observed pattern.

Answer using the pipeline’s notation: thickness is $x$ (nm), outcomes are $Y_j$, predictions are $\hat y_j(x)$, residuals are $\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}$. When you reference a metric, state its definition (e.g. $\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum \hat\varepsilon^2}$) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 26. For target $\mathrm{Retention}$ (`Highest Capacity Retention_percent`): Write down the residual definition $\hat\varepsilon = y-\hat y$ and interpret its sign in context.

Answer using the pipeline’s notation: thickness is $x$ (nm), outcomes are $Y_j$, predictions are $\hat y_j(x)$, residuals are $\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}$. When you reference a metric, state its definition (e.g. $\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum \hat\varepsilon^2}$) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 27. For target $\mathrm{Retention}$ (`Highest Capacity Retention_percent`): Explain why in-sample metrics can be optimistic when thickness is discrete and models can interpolate cohorts.

Answer using the pipeline’s notation: thickness is $x$ (nm), outcomes are $Y_j$, predictions are $\hat y_j(x)$, residuals are $\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}$. When you reference a metric, state its definition (e.g. $\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum \hat\varepsilon^2}$) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 28. For target $\mathrm{Retention}$ (`Highest Capacity Retention_percent`): Describe how you would validate stability if you were allowed to collect more thickness levels.

Answer using the pipeline’s notation: thickness is $x$ (nm), outcomes are $Y_j$, predictions are $\hat y_j(x)$, residuals are $\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}$. When you reference a metric, state its definition (e.g. $\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum \hat\varepsilon^2}$) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 29. For the univariate distribution family: what visual feature would count as 'structure' rather than noise at n=51?

Answer using the pipeline’s notation: thickness is $x$ (nm), outcomes are $Y_j$, predictions are $\hat y_j(x)$, residuals are $\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}$. When you reference a metric, state its definition (e.g. $\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum \hat\varepsilon^2}$) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 30. For the univariate distribution family: list two failure modes (plotting or statistical) that can mislead interpretation.

Answer using the pipeline’s notation: thickness is $x$ (nm), outcomes are $Y_j$, predictions are $\hat y_j(x)$, residuals are $\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}$. When you reference a metric, state its definition (e.g. $\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum \hat\varepsilon^2}$) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 31. For the bivariate scatter-with-trends family: what visual feature would count as 'structure' rather than noise at n=51?

Answer using the pipeline’s notation: thickness is $x$ (nm), outcomes are $Y_j$, predictions are $\hat y_j(x)$, residuals are $\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}$. When you reference a metric, state its definition (e.g. $\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum \hat\varepsilon^2}$) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 32. For the bivariate scatter-with-trends family: list two failure modes (plotting or statistical) that can mislead interpretation.

Answer using the pipeline’s notation: thickness is $x$ (nm), outcomes are $Y_j$, predictions are $\hat y_j(x)$, residuals are $\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}$. When you reference a metric, state its definition (e.g. $\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum \hat\varepsilon^2}$) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 33. For the grouped mean with uncertainty family: what visual feature would count as 'structure' rather than noise at n=51?

Answer using the pipeline’s notation: thickness is $x$ (nm), outcomes are $Y_j$, predictions are $\hat y_j(x)$, residuals are $\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}$. When you reference a metric, state its definition (e.g. $\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum \hat\varepsilon^2}$) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 34. For the grouped mean with uncertainty family: list two failure modes (plotting or statistical) that can mislead interpretation.

Answer using the pipeline’s notation: thickness is $x$ (nm), outcomes are $Y_j$, predictions are $\hat y_j(x)$, residuals are $\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}$. When you reference a metric, state its definition (e.g. $\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum \hat\varepsilon^2}$) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 35. For the correlation heatmaps (Pearson/Spearman) family: what visual feature would count as 'structure' rather than noise at n=51?

Answer using the pipeline’s notation: thickness is $x$ (nm), outcomes are $Y_j$, predictions are $\hat y_j(x)$, residuals are $\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}$. When you reference a metric, state its definition (e.g. $\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum \hat\varepsilon^2}$) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 36. For the correlation heatmaps (Pearson/Spearman) family: list two failure modes (plotting or statistical) that can mislead interpretation.

Answer using the pipeline’s notation: thickness is $x$ (nm), outcomes are $Y_j$, predictions are $\hat y_j(x)$, residuals are $\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}$. When you reference a metric, state its definition (e.g. $\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum \hat\varepsilon^2}$) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 37. For the parity (actual vs predicted) family: what visual feature would count as 'structure' rather than noise at n=51?

Answer using the pipeline’s notation: thickness is $x$ (nm), outcomes are $Y_j$, predictions are $\hat y_j(x)$, residuals are $\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}$. When you reference a metric, state its definition (e.g. $\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum \hat\varepsilon^2}$) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 38. For the parity (actual vs predicted) family: list two failure modes (plotting or statistical) that can mislead interpretation.

Answer using the pipeline’s notation: thickness is $x$ (nm), outcomes are $Y_j$, predictions are $\hat y_j(x)$, residuals are $\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}$. When you reference a metric, state its definition (e.g. $\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum \hat\varepsilon^2}$) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 39. For the residuals vs thickness family: what visual feature would count as 'structure' rather than noise at n=51?

Answer using the pipeline’s notation: thickness is $x$ (nm), outcomes are $Y_j$, predictions are $\hat y_j(x)$, residuals are $\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}$. When you reference a metric, state its definition (e.g. $\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum \hat\varepsilon^2}$) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 40. For the residuals vs thickness family: list two failure modes (plotting or statistical) that can mislead interpretation.

Answer using the pipeline’s notation: thickness is $x$ (nm), outcomes are $Y_j$, predictions are $\hat y_j(x)$, residuals are $\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}$. When you reference a metric, state its definition (e.g. $\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum \hat\varepsilon^2}$) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 41. For the residual distribution and QQ family: what visual feature would count as 'structure' rather than noise at n=51?

Answer using the pipeline’s notation: thickness is $x$ (nm), outcomes are $Y_j$, predictions are $\hat y_j(x)$, residuals are $\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}$. When you reference a metric, state its definition (e.g. $\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum \hat\varepsilon^2}$) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 42. For the residual distribution and QQ family: list two failure modes (plotting or statistical) that can mislead interpretation.

Answer using the pipeline’s notation: thickness is $x$ (nm), outcomes are $Y_j$, predictions are $\hat y_j(x)$, residuals are $\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}$. When you reference a metric, state its definition (e.g. $\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum \hat\varepsilon^2}$) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 43. For the PDP/ICE family: what visual feature would count as 'structure' rather than noise at n=51?

Answer using the pipeline’s notation: thickness is $x$ (nm), outcomes are $Y_j$, predictions are $\hat y_j(x)$, residuals are $\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}$. When you reference a metric, state its definition (e.g. $\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum \hat\varepsilon^2}$) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 44. For the PDP/ICE family: list two failure modes (plotting or statistical) that can mislead interpretation.

Answer using the pipeline’s notation: thickness is $x$ (nm), outcomes are $Y_j$, predictions are $\hat y_j(x)$, residuals are $\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}$. When you reference a metric, state its definition (e.g. $\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum \hat\varepsilon^2}$) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 45. For the local sensitivity family: what visual feature would count as 'structure' rather than noise at n=51?

Answer using the pipeline’s notation: thickness is $x$ (nm), outcomes are $Y_j$, predictions are $\hat y_j(x)$, residuals are $\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}$. When you reference a metric, state its definition (e.g. $\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum \hat\varepsilon^2}$) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 46. For the local sensitivity family: list two failure modes (plotting or statistical) that can mislead interpretation.

Answer using the pipeline’s notation: thickness is $x$ (nm), outcomes are $Y_j$, predictions are $\hat y_j(x)$, residuals are $\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}$. When you reference a metric, state its definition (e.g. $\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum \hat\varepsilon^2}$) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 47. For the permutation importance family: what visual feature would count as 'structure' rather than noise at n=51?

Answer using the pipeline’s notation: thickness is $x$ (nm), outcomes are $Y_j$, predictions are $\hat y_j(x)$, residuals are $\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}$. When you reference a metric, state its definition (e.g. $\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum \hat\varepsilon^2}$) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 48. For the permutation importance family: list two failure modes (plotting or statistical) that can mislead interpretation.

Answer using the pipeline’s notation: thickness is $x$ (nm), outcomes are $Y_j$, predictions are $\hat y_j(x)$, residuals are $\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}$. When you reference a metric, state its definition (e.g. $\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum \hat\varepsilon^2}$) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 49. For the SHAP beeswarm / dependence (optional) family: what visual feature would count as 'structure' rather than noise at n=51?

Answer using the pipeline’s notation: thickness is $x$ (nm), outcomes are $Y_j$, predictions are $\hat y_j(x)$, residuals are $\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}$. When you reference a metric, state its definition (e.g. $\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum \hat\varepsilon^2}$) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 50. For the SHAP beeswarm / dependence (optional) family: list two failure modes (plotting or statistical) that can mislead interpretation.

Answer using the pipeline’s notation: thickness is $x$ (nm), outcomes are $Y_j$, predictions are $\hat y_j(x)$, residuals are $\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}$. When you reference a metric, state its definition (e.g. $\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum \hat\varepsilon^2}$) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 51. Trace the exact file path(s) you would open to answer the question; include the README index you would consult first. (outputs/)

Answer using the pipeline’s notation: thickness is $x$ (nm), outcomes are $Y_j$, predictions are $\hat y_j(x)$, residuals are $\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}$. When you reference a metric, state its definition (e.g. $\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum \hat\varepsilon^2}$) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 52. Explain how file naming uses `safe_filename()` and why that matters when target names contain punctuation. (outputs/)

Answer using the pipeline’s notation: thickness is $x$ (nm), outcomes are $Y_j$, predictions are $\hat y_j(x)$, residuals are $\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}$. When you reference a metric, state its definition (e.g. $\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum \hat\varepsilon^2}$) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 53. Describe a minimal repro run: commands, what gets deleted, and which outputs are regenerated. (outputs/)

Answer using the pipeline’s notation: thickness is $x$ (nm), outcomes are $Y_j$, predictions are $\hat y_j(x)$, residuals are $\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}$. When you reference a metric, state its definition (e.g. $\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum \hat\varepsilon^2}$) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 54. Explain how the pipeline separates machine-readable tables (CSV/XLSX) from human-readable narratives (Markdown). (outputs/)

Answer using the pipeline’s notation: thickness is $x$ (nm), outcomes are $Y_j$, predictions are $\hat y_j(x)$, residuals are $\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}$. When you reference a metric, state its definition (e.g. $\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum \hat\varepsilon^2}$) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

---

## Appendix: Reproducibility Checklist

- Confirm the workbook is `Data/Data.xlsx` and the sheet policy is followed (Dataset sheet only).
- Confirm the feature is exactly `Al2O3 Thickness_nm` and the sample-id column is ignored.
- Run `py run_all.py` from the repository root; note that it deletes the previous `outputs/` tree.
- Verify that each `outputs/**/README.md` exists and matches the directory inventory described there.
- When comparing runs, prefer comparing **tables** (CSV) first, then figures (PNG) second.
- If optional libraries (SHAP, XGBoost, LightGBM, CatBoost) are missing, confirm the pipeline degrades gracefully.
