# Exploratory Data Analysis Outputs

Exploratory Data Analysis (EDA) answers: **what does the dataset actually look like** before we commit to a parametric model? Here the experimental design is unusually simple: one controlled input (**$\mathrm{Al}_{2}\mathrm{O}_{3}$ thickness** $x\ge 0$ nm, column ``Al2O3 Thickness_nm``) and **four** measured outputs (charge-transfer resistance, coulombic efficiency, reversible capacity, capacity retention). EDA therefore focuses on (i) **where data mass lives** (especially $x=0$ vs sparse positive thicknesses), (ii) **how each $Y_j$ varies with $x$** when many points share the same $x$, and (iii) **linear vs rank association** as a first-pass summary, *not* as a substitute for plotting conditional means.

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

$$
Y_j = g_j(x) + \eta_j,\qquad j=1,\ldots,4,
$$

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

Figures use mathtext: $R_{\mathrm{ct}}$, $Q_{\mathrm{rev}}$, etc. Markdown in these READMEs uses GitHub ``$...$`` / ``$$...$$``.
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

### 51. Trace the exact file path(s) you would open to answer the question; include the README index you would consult first. (outputs/eda/)

Answer using the pipeline’s notation: thickness is $x$ (nm), outcomes are $Y_j$, predictions are $\hat y_j(x)$, residuals are $\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}$. When you reference a metric, state its definition (e.g. $\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum \hat\varepsilon^2}$) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 52. Explain how file naming uses `safe_filename()` and why that matters when target names contain punctuation. (outputs/eda/)

Answer using the pipeline’s notation: thickness is $x$ (nm), outcomes are $Y_j$, predictions are $\hat y_j(x)$, residuals are $\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}$. When you reference a metric, state its definition (e.g. $\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum \hat\varepsilon^2}$) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 53. Describe a minimal repro run: commands, what gets deleted, and which outputs are regenerated. (outputs/eda/)

Answer using the pipeline’s notation: thickness is $x$ (nm), outcomes are $Y_j$, predictions are $\hat y_j(x)$, residuals are $\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}$. When you reference a metric, state its definition (e.g. $\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum \hat\varepsilon^2}$) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

### 54. Explain how the pipeline separates machine-readable tables (CSV/XLSX) from human-readable narratives (Markdown). (outputs/eda/)

Answer using the pipeline’s notation: thickness is $x$ (nm), outcomes are $Y_j$, predictions are $\hat y_j(x)$, residuals are $\hat\varepsilon_{ij}=y_{ij}-\hat y_{ij}$. When you reference a metric, state its definition (e.g. $\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum \hat\varepsilon^2}$) and identify whether it is computed **in-sample**. When you reference a plot, name its stem (e.g. “Residuals Versus Thickness”) and locate it under `outputs/` using the directory README indices.

---

## Appendix: Reproducibility Checklist

- Confirm the workbook is `Data/Data.xlsx` and the sheet policy is followed (Dataset sheet only).
- Confirm the feature is exactly `Al2O3 Thickness_nm` and the sample-id column is ignored.
- Run `py run_all.py` from the repository root; note that it deletes the previous `outputs/` tree.
- Verify that each `outputs/**/README.md` exists and matches the directory inventory described there.
- When comparing runs, prefer comparing **tables** (CSV) first, then figures (PNG) second.
- If optional libraries (SHAP, XGBoost, LightGBM, CatBoost) are missing, confirm the pipeline degrades gracefully.
