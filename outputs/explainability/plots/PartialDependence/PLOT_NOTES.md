# Plot Notes — `explainability/plots/PartialDependence`

This file is auto-written by the pipeline to describe what each figure in this folder is intended to communicate. All statements are *interpretive guides* to the plotted objects (curves, residuals, densities), not guarantees of causal mechanism.

## Notation

- Thickness: $x$ (nm)
- Target: $Y_j$
- Prediction: $\hat y_j(x)$
- Residual: $\hat\varepsilon_i = y_i-\hat y_i$

## Figures in this folder

### `Partial Dependence And ICE__Highest Capacity Retention_percent.png`

**Type**: PDP + ICE (model response curve)

**What it is saying**: Shows the fitted response curve $\hat y_j(x)$ along a dense thickness grid (PDP) with bootstrap/ICE variability. Large bands indicate instability under resampling (important at small $n$).

### `Partial Dependence And ICE__ICE_percent.png`

**Type**: PDP + ICE (model response curve)

**What it is saying**: Shows the fitted response curve $\hat y_j(x)$ along a dense thickness grid (PDP) with bootstrap/ICE variability. Large bands indicate instability under resampling (important at small $n$).

### `Partial Dependence And ICE__Initial Reversible Capacity_mAh_g at 0.1C.png`

**Type**: PDP + ICE (model response curve)

**What it is saying**: Shows the fitted response curve $\hat y_j(x)$ along a dense thickness grid (PDP) with bootstrap/ICE variability. Large bands indicate instability under resampling (important at small $n$).

### `Partial Dependence And ICE__Rct_initial_ohm.png`

**Type**: PDP + ICE (model response curve)

**What it is saying**: Shows the fitted response curve $\hat y_j(x)$ along a dense thickness grid (PDP) with bootstrap/ICE variability. Large bands indicate instability under resampling (important at small $n$).
