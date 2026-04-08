# Modeling Diagnostics Plots Index

This directory contains the full diagnostics set for every model and every target. Plots are organized into a hierarchy by model name and then by target name. This structure makes it easy to audit a single target across models or to audit a single model across all targets without mixing files in one flat folder.

The core diagnostics include parity plots, residuals versus predicted, residuals versus actual, residuals versus thickness, residual distribution views, and Qq plots. These diagnostics reveal underfitting as structured residual patterns and overfitting as unnatural collapse of the predicted distribution. In one dimensional discrete input settings, these visuals are essential for scientific honesty.

Because metrics are in-sample, **near-saturated** $R^2$ is compatible with cohort memorization at the discrete $x$ atoms. The residual-vs-$x$ panel is therefore primary: ideally residuals are mean-centered with no systematic thickness trend, while $ \hat{y}(x) $ remains smooth enough to interpolate scientifically between measured levels.

All figures share a consistent PERO visual language: Title Case, minimal decorative punctuation, and Matplotlib mathtext for standard electrochemical symbols. Treat this tree as camera-ready without manual restyling.
