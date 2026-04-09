# Plot Notes — `explainability/plots/Shap`

This file is auto-written by the pipeline to describe what each figure in this folder is intended to communicate. All statements are *interpretive guides* to the plotted objects (curves, residuals, densities), not guarantees of causal mechanism.

## Notation

- Thickness: $x$ (nm)
- Target: $Y_j$
- Prediction: $\hat y_j(x)$
- Residual: $\hat\varepsilon_i = y_i-\hat y_i$

## Figures in this folder

### `shap_bar__Highest Capacity Retention_percent.png`

**Type**: SHAP bar (mean absolute attribution)

**What it is saying**: Reports $\mathbb{E}[|\phi|]$ for the single feature. With $p=1$, it is a magnitude summary, not a ranking among many features.

### `shap_bar__ICE_percent.png`

**Type**: SHAP bar (mean absolute attribution)

**What it is saying**: Reports $\mathbb{E}[|\phi|]$ for the single feature. With $p=1$, it is a magnitude summary, not a ranking among many features.

### `shap_bar__Initial Reversible Capacity_mAh_g at 0.1C.png`

**Type**: SHAP bar (mean absolute attribution)

**What it is saying**: Reports $\mathbb{E}[|\phi|]$ for the single feature. With $p=1$, it is a magnitude summary, not a ranking among many features.

### `shap_bar__Rct_initial_ohm.png`

**Type**: SHAP bar (mean absolute attribution)

**What it is saying**: Reports $\mathbb{E}[|\phi|]$ for the single feature. With $p=1$, it is a magnitude summary, not a ranking among many features.

### `shap_beeswarm__Highest Capacity Retention_percent.png`

**Type**: SHAP beeswarm (1D attribution cloud)

**What it is saying**: In 1D, SHAP values $\phi(x)$ largely re-express deviations from the baseline prediction. Use it as a consistency view: does attribution vary smoothly with thickness, or is it cohort-stepped?

### `shap_beeswarm__ICE_percent.png`

**Type**: SHAP beeswarm (1D attribution cloud)

**What it is saying**: In 1D, SHAP values $\phi(x)$ largely re-express deviations from the baseline prediction. Use it as a consistency view: does attribution vary smoothly with thickness, or is it cohort-stepped?

### `shap_beeswarm__Initial Reversible Capacity_mAh_g at 0.1C.png`

**Type**: SHAP beeswarm (1D attribution cloud)

**What it is saying**: In 1D, SHAP values $\phi(x)$ largely re-express deviations from the baseline prediction. Use it as a consistency view: does attribution vary smoothly with thickness, or is it cohort-stepped?

### `shap_beeswarm__Rct_initial_ohm.png`

**Type**: SHAP beeswarm (1D attribution cloud)

**What it is saying**: In 1D, SHAP values $\phi(x)$ largely re-express deviations from the baseline prediction. Use it as a consistency view: does attribution vary smoothly with thickness, or is it cohort-stepped?

### `shap_dependence__Highest Capacity Retention_percent.png`

**Type**: SHAP dependence (attribution vs thickness)

**What it is saying**: Plots SHAP value $\phi(x)$ against thickness. In a single-feature project, this often mirrors the fitted response shape and can highlight thickness regions where the model’s contribution changes fastest.

### `shap_dependence__ICE_percent.png`

**Type**: SHAP dependence (attribution vs thickness)

**What it is saying**: Plots SHAP value $\phi(x)$ against thickness. In a single-feature project, this often mirrors the fitted response shape and can highlight thickness regions where the model’s contribution changes fastest.

### `shap_dependence__Initial Reversible Capacity_mAh_g at 0.1C.png`

**Type**: SHAP dependence (attribution vs thickness)

**What it is saying**: Plots SHAP value $\phi(x)$ against thickness. In a single-feature project, this often mirrors the fitted response shape and can highlight thickness regions where the model’s contribution changes fastest.

### `shap_dependence__Rct_initial_ohm.png`

**Type**: SHAP dependence (attribution vs thickness)

**What it is saying**: Plots SHAP value $\phi(x)$ against thickness. In a single-feature project, this often mirrors the fitted response shape and can highlight thickness regions where the model’s contribution changes fastest.
