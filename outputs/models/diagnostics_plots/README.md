# Modeling Diagnostics Plots Index

This directory contains the full diagnostics set for every model and every target. Plots are organized into a hierarchy by model name and then by target name. This structure makes it easy to audit a single target across models or to audit a single model across all targets without mixing files in one flat folder.

The core diagnostics include parity plots, residuals versus predicted, residuals versus actual, residuals versus thickness, residual distribution views, and Qq plots. These diagnostics reveal underfitting as structured residual patterns and overfitting as unnatural collapse of the predicted distribution. In one dimensional discrete input settings, these visuals are essential for scientific honesty.

Because metrics are in sample, a very high \(R^2\) can occur when a model effectively memorizes thickness cohorts. The residuals versus thickness plot is therefore treated as a primary diagnostic. A good model will show residuals that are centered without strong thickness dependent structure, while still producing a smooth and plausible response curve.

All figures share a consistent PERO visual language. Titles and labels are written in Title Case and avoid parentheses, while mathematical notation uses LaTeX style mathtext for scientifically standard symbols. This directory is intended to be directly usable for report figures without further manual styling edits.
