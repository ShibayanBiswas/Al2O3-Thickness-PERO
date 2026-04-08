# Bivariate Plots

Bivariate views emphasize thickness response behavior for each target using trends and uncertainty aware overlays. Each figure is exported with consistent background and grid styling to support direct insertion into a report. Because the dataset is small, these plots are intentionally clean and avoid excessive panel counts that would reduce interpretability.

For distribution style plots, focus on whether the observed values cluster tightly at a small set of levels or whether the variable behaves continuously. For thickness, the concentration at the zero level is expected to be dominant, so plots should be interpreted in a mixed discrete and continuous sense. The goal is not to force a continuous narrative but to represent what the experiment actually provides.

For response style plots, interpret trends as hypotheses about \(\hat{y}(x)\) rather than as proofs of causality. The bivariate suite uses a single linear trend as a conservative summary, plus shaded bands that visualize dispersion across thickness cohorts. In a one dimensional design, these uncertainty aware overlays are often more scientifically honest than stacking multiple trend families.

All plot text follows a strict formatting rule to avoid parentheses and to keep labels in Title Case. Mathematical terms use LaTeX style mathtext when it improves scientific clarity, such as \(R_{\mathrm{ct}}\) and \(Q_{\mathrm{rev}}\). This keeps the visuals both professional and mathematically correct without requiring a full LaTeX installation.
