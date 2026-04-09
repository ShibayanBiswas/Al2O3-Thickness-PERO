# Univariate Plots

Marginal laws of $x$ and each $Y_j$: histogram + kernel density, ECDF, box/violin/raincloud, scaling-density overlays.

## Files in each ``<VarTitle>/`` subfolder

Each subfolder is one numeric column (thickness $x$ or a target $Y_j$). Typical stems (``*.png``):

- ``Histogram And Kernel Density`` -- compare **tails** and **modes** across variables; check units mentally using the axis label.
- ``Box And Violin`` -- link **quartiles** (box) to **density** (violin wings).
- ``Raincloud Plot`` (optional) -- every point visible; good for spotting duplicates and outliers.
- ``Empirical Cumulative Distribution`` -- probability mass below a threshold; complements histograms for skewed data.
- ``Scaling Comparison Density`` (optional) -- how transforms change overlap of distributions.

See ``../README.md`` for the master table and column-level interpretation cues.

---

## Study questions (self-quiz)

- Does thickness $x$ concentrate at **0 nm**? Do targets show **heavy tails** or **bounded** support?
- Are univariate shapes **similar** across the four electrochemical targets (suggesting shared noise structure)?

---

## Reading guide

Smooth traces are **visual aids** -- they help the eye; they do not replace formal model checks. In this project’s bivariate views we keep the trend line **linear** and use quantile bands to show conditional spread without overfitting the mean shape.

---

## Figure style in this branch

**Title Case** titles, **outside legends** on multi-series panels, mathtext on axes ($R_{\mathrm{ct}}$, $Q_{\mathrm{rev}}$, $\mathrm{Al}_{2}\mathrm{O}_{3}$). Colours follow ``PERO`` in ``src/viz_style.py`` for consistency with modelling and explainability figures.
