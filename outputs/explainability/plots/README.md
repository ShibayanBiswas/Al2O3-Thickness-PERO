# Explainability Plots Index

This directory contains plots that explain how thickness influences each target for the selected best overall model. In a one dimensional feature space, explainability focuses on the shape of the learned response function \(\hat{y}(x)\) and on how predictions change as thickness varies. These plots are designed to support mechanistic discussion, such as monotonic trends, threshold like behavior, or localized sensitivity ranges.

Partial dependence and individual conditional expectation plots are exported when supported. In one dimension, PDP acts as a smoothed estimate of the mean response curve, while ICE shows individual trajectories around that curve. These plots are valuable for detecting heterogeneity and for spotting cases where the model response is driven by a small number of thickness cohorts.

A sensitivity curve is included for each target and overlays the predicted response with a local slope diagnostic that approximates \(\frac{d\hat{y}}{dx}\). This helps identify thickness regimes where small thickness changes are associated with large predicted changes in the target. Such regimes are scientifically important because they indicate where deposition control would matter most in practice.

SHAP plots are included when the SHAP library can explain the fitted estimator efficiently. In a one dimensional setting, SHAP values provide a consistent signed explanation of how thickness shifts the prediction relative to a background distribution. These plots are intended as interpretability evidence rather than as proof of causality, and they are formatted for direct inclusion in a research report.
