# Grouped Plots

Cohort summaries: for each thickness atom $x_k$, means $\bar Y_j$ and $\pm s$ tubes along $x$.

## Files in each ``<TargetTitle>/`` subfolder

- ``Group Mean With Uncertainty.png`` -- connects **cohort means** $ar Y_j$ at each measured $x_k$ with a tube based on within-group standard deviation $s$.

**Aggregate table (all targets):** ``../../tables/05_grouped_summary_all_targets_by_thickness.csv``.

---

## Study questions

- Does $ar Y_j$ change **monotonically** with $x$, or are some thicknesses **local optima**?
- Is uncertainty **heteroscedastic** (wider tubes at some $x_k$)? That matters for weighted or robust modelling.

---

## Reading guide

Smooth traces are **visual aids** -- they help the eye; they do not replace formal model checks. In this project’s bivariate views we keep the trend line **linear** and use quantile bands to show conditional spread without overfitting the mean shape.

---

## Figure style in this branch

**Title Case** titles, **outside legends** on multi-series panels, mathtext on axes ($R_{\mathrm{ct}}$, $Q_{\mathrm{rev}}$, $\mathrm{Al}_{2}\mathrm{O}_{3}$). Colours follow ``PERO`` in ``src/viz_style.py`` for consistency with modelling and explainability figures.
