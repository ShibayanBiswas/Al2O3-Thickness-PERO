# Explainability Outputs

This directory explains how $x$ enters the **selected** best-overall model for each target. With $p=1$, explainability collapses to geometry: the graph of $ \hat{y}(x) $, its local stability, and perturbation sensitivity—not Shapley-style competition among many inputs.

Permutation importance is reported as the drop in $R^2$ when $x$ is randomly shuffled within target. Large collapses imply the fit leans hard on thickness ordering; near-zero drops suggest noise dominance or an already flat ridge along $x$. The statistic is model-agnostic and pairs naturally with the curve plots.

When libraries permit, **PDP** and **ICE** curves are exported. In 1D, the PDP traces a marginal average of $ \hat{y}(x) $ while ICE ribbons reveal unit-level deviations. A **sensitivity** overlay estimates $ \frac{\mathrm{d}\hat{y}}{\mathrm{d}x} $ via local differencing—useful for highlighting nm regimes where deposition control would move predictions fastest.

SHAP exports are included when the installed SHAP library supports the selected estimator. In one dimension, SHAP values primarily reflect how the prediction shifts as thickness moves away from the reference distribution. These plots should be interpreted as a consistent explanation of a one dimensional response function rather than as a competition among multiple inputs. All exports are formatted for integration into a research report without additional manual styling work.
