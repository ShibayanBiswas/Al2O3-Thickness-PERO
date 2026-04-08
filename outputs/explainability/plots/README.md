# Explainability Plots Index

These plots dissect the **learned response** $ \hat{y}(x) $ for the champion model: shape, curvature, cohort stratification, and where local slope is steepest.

Partial dependence and individual conditional expectation plots are exported when supported. In one dimension, PDP acts as a smoothed estimate of the mean response curve, while ICE shows individual trajectories around that curve. These plots are valuable for detecting heterogeneity and for spotting cases where the model response is driven by a small number of thickness cohorts.

Each target includes a sensitivity trace approximating $ \frac{\mathrm{d}\hat{y}}{\mathrm{d}x} $ beside $ \hat{y}(x) $, flagging nm windows where incremental thickness shifts explode or compress the predicted electrochemical figure of merit.

SHAP plots are included when the SHAP library can explain the fitted estimator efficiently. In a one dimensional setting, SHAP values provide a consistent signed explanation of how thickness shifts the prediction relative to a background distribution. These plots are intended as interpretability evidence rather than as proof of causality, and they are formatted for direct inclusion in a research report.
