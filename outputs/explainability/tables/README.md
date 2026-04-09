# Explainability Tables Index

Single CSV written by ``permutation_importance_single_feature()`` in ``src/explainability.py`` when the call succeeds.

---

## File

| File | Role |
| --- | --- |
| ``permutation_importance_single_feature.csv`` | One row per target: Monte Carlo mean/std of $\Delta R^2$ from shuffling $x$ |

---

## Columns

| Column | Meaning |
| --- | --- |
| ``target`` | Target column name |
| ``feature`` | Shuffled column (always the thickness feature, first column of $X$) |
| ``r2_drop_mean`` | Mean of $R^2_{\text{full}} - R^2_{\text{permuted}}$ over repeats |
| ``r2_drop_std`` | Sample std of that drop (``ddof=1``) |
| ``n_repeats`` | Number of permutations (``run_all`` uses 120) |

---

## Definition

For target $j$,

$$
\Delta R^2_j = R^2_j - R^2_j(\pi),
$$

with $\pi$ a random permutation of the thickness column.

---

## How to read

| $\Delta R^2_j$ | Reading |
| --- | --- |
| Large | Fit leans on authentic ordering of $x$ |
| Tiny | Thickness weak in-sample or noise-dominated |

Pair with PDP/ICE and (if present) SHAP $|\phi|$ --- tables encode **stability**, curves encode **shape**.

---

## Connecting table values to plots

| CSV signal | Where to look |
| --- | --- |
| Large ``r2_drop_mean`` for target $j$ | ``../plots/PartialDependence/`` and ``../plots/Sensitivity/`` for that target |
| Small drop for every target | Check whether base $R^2$ in ``outputs/models/tables/`` was already modest |
| High ``r2_drop_std`` | Uncertain importance; read ICE / bootstrap ribbons as **intervals**, not point truth |

---

## Statistical intuition

Permutation destroys **joint structure** $(x, y)$ while preserving the **marginal** histogram of $x$. If predictions barely change, the fitted map did not rely on which row carried which thickness --- either the signal is weak or the estimator is too rigid to use $x$.
