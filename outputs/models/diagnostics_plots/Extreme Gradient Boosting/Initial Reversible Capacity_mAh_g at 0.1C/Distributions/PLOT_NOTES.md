# Plot Notes — `models/diagnostics_plots/Extreme Gradient Boosting/Initial Reversible Capacity_mAh_g at 0.1C/Distributions`

This file is auto-written by the pipeline to describe what each figure in this folder is intended to communicate. All statements are *interpretive guides* to the plotted objects (curves, residuals, densities), not guarantees of causal mechanism.

## Notation

- Thickness: $x$ (nm)
- Target: $Y_j$
- Prediction: $\hat y_j(x)$
- Residual: $\hat\varepsilon_i = y_i-\hat y_i$

## Figures in this folder

### `Predicted And Actual Density__Extreme Gradient Boosting__Initial Reversible Capacity_mAh_g at 0.1C.png`

**Type**: Predicted vs actual density (distribution match)

**What it is saying**: Overlaid densities of $y$ and $\hat y$. Systematic shifts indicate bias; width mismatch indicates under/over-estimated variance.

### `QQ Plot__Extreme Gradient Boosting__Initial Reversible Capacity_mAh_g at 0.1C.png`

**Type**: QQ plot (normality screen)

**What it is saying**: Compares residual quantiles to a normal reference. With $n=51$, treat as a gentle screen: large tail deviations suggest heavy-tailed errors.

### `Residual Box Plot__Extreme Gradient Boosting__Initial Reversible Capacity_mAh_g at 0.1C.png`

**Type**: Residual box plot (robust spread)

**What it is saying**: Box summary of residuals. Large IQR or extreme whiskers indicate error dispersion; median offset from 0 indicates bias.

### `Residual Distribution__Extreme Gradient Boosting__Initial Reversible Capacity_mAh_g at 0.1C.png`

**Type**: Residual distribution (shape of errors)

**What it is saying**: Histogram + KDE of residuals. Center near 0 is ideal; skew or heavy tails indicate systematic bias or outlier-driven error.
