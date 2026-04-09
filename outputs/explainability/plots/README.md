# Explainability Plots Index

Each graphic studies $\hat{y}:\mathbb{R}_{\ge0}\to\mathbb{R}$ **per target** for the champion model. Stems are built in ``src/explainability.py`` and saved with ``savefig()``, so the **full stem** (including the target suffix) is normalized by ``safe_filename()``.

Convention below: ``<TargetRaw>`` is the **exact** target column string from the dataset; on disk it appears as ``safe_filename("...__" + <TargetRaw>)`` merged into one stem.

---

## ``PartialDependence/`` (from ``pdp_ice_1d``)

| File stem pattern (``*.png``) | Role |
| --- | --- |
| ``Partial Dependence And ICE__<TargetRaw>`` | Solid PDP line, optional ICE quantile band from bootstrap refits, filled response area |

Legend title: **PDP / ICE**.

---

## ``Sensitivity/`` (from ``local_sensitivity_curve``)

| File stem pattern | Role |
| --- | --- |
| ``Sensitivity Curve__<TargetRaw>`` | Upper: $\hat{y}(x)$ with optional bootstrap ribbon; lower: $\mathrm{d}\hat{y}/\mathrm{d}x$ |

Legend titles: **Response** (top), **Sensitivity** (bottom).

---

## ``Shap/`` (from ``shap_explain_1d_single_output``; may be empty)

| File stem pattern | Role |
| --- | --- |
| ``shap_beeswarm__<TargetRaw>`` | Jittered $x$ vs SHAP $\phi$, smoothed trend |
| ``shap_bar__<TargetRaw>`` | Single bar: $\mathbb{E}[|\phi|]$ for the one feature |
| ``shap_dependence__<TargetRaw>`` | Dependence-style $\phi$ vs $x$ |

Legend title: **Attribution**. **No waterfall plots.**

---

## How to read each graphic type

- **PDP line** -- the fitted model's prediction $\hat{y}_j(x)$ on a dense thickness grid (smoothed for display).  
- **ICE band** -- quantiles of **bootstrap-refitted** prediction curves; wide bands mean the map is **sensitive** to which rows are in the training draw (interpret cautiously at $n=51$).  
- **Sensitivity** -- derivative of the **smooth** prediction curve; spikes may sit where support is thin.  
- **SHAP panels** -- attribute **local** deviations from the baseline prediction to the single feature; with $p=1$, dependence and beeswarm largely **re-express** $\hat{y}(x)$ and residuals of the explainer.

---

## Note on filenames

If a target name contains parentheses or special characters, compare against the **actual** files on disk --- ``safe_filename`` maps those to spaces/underscores while keeping the stem human-readable.
