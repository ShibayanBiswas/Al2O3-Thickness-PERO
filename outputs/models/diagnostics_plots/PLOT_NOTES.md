# Plot Notes — `models/diagnostics_plots`

This file is auto-written by the pipeline to describe what each figure in this folder is intended to communicate. All statements are *interpretive guides* to the plotted objects (curves, residuals, densities), not guarantees of causal mechanism.

## Notation

- Thickness: $x$ (nm)
- Target: $Y_j$
- Prediction: $\hat y_j(x)$
- Residual: $\hat\varepsilon_i = y_i-\hat y_i$

## Figures in this folder

### `Model Comparison Overall Error.png`

**Type**: Leaderboard (overall error comparison)

**What it is saying**: Ranks models using an overall in-sample error summary (see `outputs/models/tables/README.md` for the exact aggregation). Use it to shortlist, then validate with residual structure vs thickness.
