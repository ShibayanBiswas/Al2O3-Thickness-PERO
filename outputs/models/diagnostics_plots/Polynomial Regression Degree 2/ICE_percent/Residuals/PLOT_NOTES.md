# Plot Notes — `models/diagnostics_plots/Polynomial Regression Degree 2/ICE_percent/Residuals`

This file is auto-written by the pipeline to describe what each figure in this folder is intended to communicate. All statements are *interpretive guides* to the plotted objects (curves, residuals, densities), not guarantees of causal mechanism.

## Notation

- Thickness: $x$ (nm)
- Target: $Y_j$
- Prediction: $\hat y_j(x)$
- Residual: $\hat\varepsilon_i = y_i-\hat y_i$

## Figures in this folder

### `Absolute Error Versus Thickness__Polynomial Regression Degree 2__ICE_percent.png`

**Type**: Absolute error vs thickness (where the model fails)

**What it is saying**: Plots $|\hat\varepsilon|$ against $x$. Use it to see whether certain thickness cohorts are consistently harder to predict.

### `Residuals Versus Actual__Polynomial Regression Degree 2__ICE_percent.png`

**Type**: Residuals vs actual (symmetry / model mismatch)

**What it is saying**: Plots residuals against the true response. Look for systematic trends indicating bias across the response range.

### `Residuals Versus Predicted__Polynomial Regression Degree 2__ICE_percent.png`

**Type**: Residuals vs predicted (heteroscedasticity probe)

**What it is saying**: Plots residuals $\hat\varepsilon_i=y_i-\hat y_i$ against $\hat y_i$. A random cloud around 0 is desirable. Funnels or curvature suggest variance changes or missing nonlinear structure.

### `Residuals Versus Thickness__Polynomial Regression Degree 2__ICE_percent.png`

**Type**: Residuals vs thickness (design-axis stress test)

**What it is saying**: Plots residuals against thickness $x$. This is the primary diagnostic in a $p=1$ project: any trend with $x$ means the model has not captured structure tied to the design variable.
