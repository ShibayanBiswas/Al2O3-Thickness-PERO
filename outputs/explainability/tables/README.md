# Explainability Tables Index

This directory contains export ready tables that quantify the importance and sensitivity of the thickness feature for each target. In a single feature setting, importance is not a competition among many inputs. Instead, it provides a stability oriented measure of whether the fitted model meaningfully relies on thickness to explain variance in each electrochemical outcome.

Permutation importance tabulates the positive decrement in $R^2$ when $x$ is permuted; large values mean the in-sample fit is brittle without correct thickness ordering. Bootstrap dispersion across repeats quantifies Monte Carlo noise.

These values should be interpreted together with the response curve plots. A model can show importance even when the response shape is not monotonic, which may indicate nonlinear or threshold like behavior. Conversely, a smooth response curve with low importance may indicate that the variation is small relative to measurement noise at the thickness levels available.

Tables ship with explicit column semantics and stable target keys. Companion prose uses GitHub-flavored `$...$` math so coefficients and symbols stay legible on GitHub without a LaTeX toolchain—**PERO** appendix hygiene.
