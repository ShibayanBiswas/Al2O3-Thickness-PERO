# Bivariate Plots

Conditional structure $Y_j \mid x$: jittered scatter, interquartile bands by thickness, linear residual view, sorted profiles.

## Files in each ``<TargetTitle>/`` subfolder

Stems (``*.png``):

- ``Scatter With Trends`` -- **start here** for each target: raw pairs $(x, Y_j)$ plus trend overlays and an **IQR tube** per discrete $x$.
- ``Sorted Profile`` -- sorts observations by $x$ so you can **trace** $Y_j$ along the experimental axis even when the scatter is dense.
- ``Residual Pattern`` -- subtracts linear structure; **systematic** residual trends vs $x$ mean the conditional mean is not captured by a line.

**Companion table:** ``../../tables/group_by_thickness__<TargetSafe>.csv`` (exact cohort $n$, mean, std).

---

## Study questions

- At each thickness with multiple cells, is the **within-$x$ spread** large compared to **between-$x$** shifts in the median?
- After viewing ``Residual Pattern``, would you defend a **linear** model for this target, or do you expect **nonlinear** or **step-like** behaviour?

---

## Reading guide

Smooth traces are **visual aids** -- they help the eye; they do not replace formal model checks. In this project’s bivariate views we keep the trend line **linear** and use quantile bands to show conditional spread without overfitting the mean shape.

---

## Figure style in this branch

**Title Case** titles, **outside legends** on multi-series panels, mathtext on axes ($R_{\mathrm{ct}}$, $Q_{\mathrm{rev}}$, $\mathrm{Al}_{2}\mathrm{O}_{3}$). Colours follow ``PERO`` in ``src/viz_style.py`` for consistency with modelling and explainability figures.
