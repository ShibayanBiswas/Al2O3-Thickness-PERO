# Plot Notes — `eda/plots/Univariate/Ice_percent`

This file is auto-written by the pipeline to describe what each figure in this folder is intended to communicate. All statements are *interpretive guides* to the plotted objects (curves, residuals, densities), not guarantees of causal mechanism.

## Notation

- Thickness: $x$ (nm)
- Target: $Y_j$
- Prediction: $\hat y_j(x)$
- Residual: $\hat\varepsilon_i = y_i-\hat y_i$

## Figures in this folder

### `Box And Violin.png`

**Type**: Box/violin summary (univariate spread)

**What it is saying**: Summarizes median, quartiles, and distribution shape. Use it to compare spread across variables and to detect outliers or strong asymmetry.

### `Empirical Cumulative Distribution.png`

**Type**: ECDF (univariate cumulative mass)

**What it is saying**: Shows $F(t)=\mathbb{P}(X\le t)$ directly. Useful for reading quantiles without binning choices and for seeing how quickly mass accumulates near key values.

### `Histogram And Kernel Density.png`

**Type**: Histogram + KDE (univariate density)

**What it is saying**: Shows the empirical distribution of a single variable. The histogram approximates the density; the KDE is a smoothed estimate. Use it to see skew, heavy tails, multi-modality, and whether a few points dominate the range.

### `Raincloud Plot.png`

**Type**: Raincloud-style view (univariate)

**What it is saying**: Combines a density impression with a point-level view, making it easier to see sample size and discrete clumping.

### `Scaling Comparison Density.png`

**Type**: Scaling comparison (diagnostic density overlay)

**What it is saying**: Overlays density under multiple rescalings/transforms (when available) to illustrate how scale choices change visual interpretation. This is a plotting/EDA diagnostic, not a modeling claim.
