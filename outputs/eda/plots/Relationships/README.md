# Relationships Plots

Association matrix: heatmaps of $\rho$ and $\rho_s$ plus numeric pair plots (short axis names to avoid clutter).

## Files in this folder (flat)

- ``Correlation Heatmap Pearson.png`` -- diverging **vlag** palette, annotated cells, thin grid lines for readability on dark background.
- ``Correlation Heatmap Spearman.png`` -- rank-based analogue; compare to Pearson to detect **nonlinear monotone** coupling.
- ``Pair Plot Numeric Variables.png`` -- optional corner **pairplot**; axis labels shortened deliberately.

**Source matrices:** ``../../tables/07_corr_pearson.csv``, ``08_corr_spearman.csv``.

---

## Study questions

- Which off-diagonal blocks link **thickness** to each target in linear vs rank sense?
- Do any two **targets** correlate strongly with each other (suggesting shared latent cell state beyond $x$)?

---

## Reading guide

Smooth traces are **nonparametric aids** -- they help the eye; they do not replace formal model checks. Polynomial overlays (through cubic) in bivariate views form a **nested** family: each step relaxes linearity.

---

## Figure style in this branch

**Title Case** titles, **outside legends** on multi-series panels, mathtext on axes ($R_{\mathrm{ct}}$, $Q_{\mathrm{rev}}$, $\mathrm{Al}_2\mathrm{O}_3$). Colours follow ``PERO`` in ``src/viz_style.py`` for consistency with modelling and explainability figures.
