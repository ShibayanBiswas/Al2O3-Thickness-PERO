# Grouped Plots

Grouped views emphasize cohort comparisons across discrete thickness levels with uncertainty bands. Each figure is exported with consistent background and grid styling to support direct insertion into a report. Because the dataset is small, these plots are intentionally clean and avoid excessive panel counts that would reduce interpretability.

For distribution style plots, focus on whether the observed values cluster tightly at a small set of levels or whether the variable behaves continuously. For thickness, the concentration at the zero level is expected to be dominant, so plots should be interpreted in a mixed discrete and continuous sense. The goal is not to force a continuous narrative but to represent what the experiment actually provides.

On response panels, smooth traces are **estimators** of $ \hat{y}(x) $, not causal claims. They surface monotonicity, saturation, or threshold phenomenology; polynomial overlays provide an ordered family of curvature tests up to cubic order—often the decisive modeling degree of freedom when $p=1$.

Annotation rules: Title Case labels, no gratuitous parentheses in display text, and Matplotlib mathtext for electrochemical symbols ($R_{\mathrm{ct}}$, $Q_{\mathrm{rev}}$). Companion Markdown in this repository uses GitHub `$...$` delimiters so the same expressions render in-browser without a LaTeX engine.
