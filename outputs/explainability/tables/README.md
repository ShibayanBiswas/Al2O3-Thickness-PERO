# Explainability Tables Index

This directory contains export ready tables that quantify the importance and sensitivity of the thickness feature for each target. In a single feature setting, importance is not a competition among many inputs. Instead, it provides a stability oriented measure of whether the fitted model meaningfully relies on thickness to explain variance in each electrochemical outcome.

Permutation importance is reported as a drop in \(R^2\) when thickness values are permuted. A large positive drop indicates that thickness is essential for explaining the target in the fitted model, while a small drop suggests that thickness has limited explanatory power in that target. Standard deviation across repeats is also reported to reflect sensitivity to resampling of the permutation process.

These values should be interpreted together with the response curve plots. A model can show importance even when the response shape is not monotonic, which may indicate nonlinear or threshold like behavior. Conversely, a smooth response curve with low importance may indicate that the variation is small relative to measurement noise at the thickness levels available.

All tables are designed for reporting and include clear column names and consistent target naming. Mathematical expressions are provided in documentation using LaTeX style mathtext. The goal is a PERO style output that is polished, reproducible, and ready for a thesis appendix without manual cleanup.
