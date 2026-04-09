# Plot Notes — `eda/plots/Bivariate/Charge Transfer Resistance Initial`

This file is auto-written by the pipeline to describe what each figure in this folder is intended to communicate. All statements are *interpretive guides* to the plotted objects (curves, residuals, densities), not guarantees of causal mechanism.

## Notation

- Thickness: $x$ (nm)
- Target: $Y_j$
- Prediction: $\hat y_j(x)$
- Residual: $\hat\varepsilon_i = y_i-\hat y_i$

## Figures in this folder

### `Residual Pattern.png`

**Type**: EDA residual-pattern probe (shape check)

**What it is saying**: A diagnostic-style view computed during EDA to highlight curvature or heteroscedasticity patterns versus thickness. If strong structure is present here, expect simple linear models to leave thickness-structured residuals later.

### `Scatter With Trends.png`

**Type**: Scatter with trend overlays (bivariate $x$ vs $Y$)

**What it is saying**: Plots observed pairs $(x_i, y_i)$ (with optional jitter for repeated $x$), plus smooth/parametric trend overlays and an IQR band by thickness. Interpret as a *sample description* of $\mathbb{E}[Y\mid x]$ shape and within-thickness spread, not as a causal law.

### `Sorted Profile.png`

**Type**: Sorted-by-thickness profile (ordered response curve)

**What it is saying**: Orders rows by thickness and plots a smoothed response profile. Use it to see whether the response is monotone, step-like, or cohort-dominated.
