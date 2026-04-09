# Plot Notes — `models/diagnostics_plots/Extra Trees/Highest Capacity Retention_percent/Calibration`

This file is auto-written by the pipeline to describe what each figure in this folder is intended to communicate. All statements are *interpretive guides* to the plotted objects (curves, residuals, densities), not guarantees of causal mechanism.

## Notation

- Thickness: $x$ (nm)
- Target: $Y_j$
- Prediction: $\hat y_j(x)$
- Residual: $\hat\varepsilon_i = y_i-\hat y_i$

## Figures in this folder

### `Parity Plot__Extra Trees__Highest Capacity Retention_percent.png`

**Type**: Parity plot (calibration: $y$ vs $\hat y$)

**What it is saying**: Plots $(y_i, \hat y_i)$ with the parity line $y=\hat y$. Systematic curvature away from the diagonal indicates bias; fan-shapes indicate heteroscedasticity. Parity can look good even when errors are thickness-structured, so also inspect residuals vs thickness.

### `Sorted Actual And Predicted__Extra Trees__Highest Capacity Retention_percent.png`

**Type**: Sorted actual vs sorted predicted (distributional alignment)

**What it is saying**: Compares order statistics of $y$ and $\hat y$. If curves track closely, predicted and actual distributions align in bulk; persistent gaps indicate distribution shift (e.g. variance under/over-estimation).
