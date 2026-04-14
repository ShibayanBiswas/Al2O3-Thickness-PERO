# Modeling Diagnostics Plots Index

**Layout:** ``diagnostics_plots/<ModelSafe>/<TargetSafe>/`` with three subfolders --- **Calibration**, **Residuals**, **Distributions** --- plus one **flat** leaderboard figure at the root of ``diagnostics_plots/``.

Naming: each figure stem is passed through ``safe_filename()`` in ``savefig()`` (``src/plots.py``). Below, ``__<base>`` means ``__`` concatenated with ``<ModelSafe>__<TargetSafe>`` as built in ``diagnostic_plots_per_target()`` (``src/diagnostics.py``).

For every exported ``*.png`` in this tree, the pipeline also writes a **matching ``*.csv``** (same stem, tidy long rows) next to the figure via ``save_plot_csv()`` --- use it to rebuild tables or overlay data in another tool.

---

## Root of ``diagnostics_plots/`` (flat)

| File stem (``*.png`` / ``*.csv``) | Content |
| --- | --- |
| ``Model Comparison Overall Error`` | Horizontal bar chart of top models by ``OVERALL_RMSE`` (from ``consolidated_model_comparison_plot``); CSV lists the same bar series. |

---

## Under ``<ModelSafe>/<TargetSafe>/Calibration/``

| File stem pattern | Content |
| --- | --- |
| ``Parity Plot__<ModelSafe>__<TargetSafe>`` | Actual vs predicted; parity line + optional $\pm$std band |
| ``Sorted Actual And Predicted__<ModelSafe>__<TargetSafe>`` | Order statistics of $y$ vs $\hat{y}$ (distributional alignment) |

---

## Under ``.../Residuals/``

| File stem pattern | Content |
| --- | --- |
| ``Residuals Versus Predicted__...`` | $\hat\varepsilon$ vs $\hat{y}$ |
| ``Residuals Versus Actual__...`` | $\hat\varepsilon$ vs $y$ |
| ``Residuals Versus Thickness__...`` | $\hat\varepsilon$ vs $x$ (primary stress test for 1D design) |
| ``Absolute Error Versus Thickness__...`` | $|\hat\varepsilon|$ vs $x$ |

---

## Under ``.../Distributions/``

| File stem pattern | Content |
| --- | --- |
| ``Residual Distribution__...`` | Histogram + KDE of $\hat\varepsilon$ |
| ``Residual Box Plot__...`` | Box summary of $\hat\varepsilon$ |
| ``QQ Plot__...`` | Normal QQ (statsmodels or scipy fallback) |
| ``Predicted And Actual Density__...`` | Overlaid KDE (or histogram fallback) of $y$ vs $\hat{y}$ |

---

## Reading guide

**Parity** --- $\hat{y}$ vs $y$; reference line and band.

**Residuals vs $x$** --- any trend with thickness flags curvature / cohort effects not absorbed by the fit.

**QQ** --- gentle read at $n=51$.

All multi-series panels use **outside legends** (PERO theme).

---

## Diagnostic catalogue (what each plot type teaches)

| Category | Plot family | Ideal (simplified) appearance | Red flag |
| --- | --- | --- | --- |
| Calibration | Parity | Points hug the **diagonal** | Systematic curve above/below diagonal |
| Calibration | Sorted actual vs predicted | Two curves **track** each other | Growing gap vs sorted index |
| Residuals | vs predicted / actual | **Cloud** centred on 0 | Funnel shape (heteroscedasticity) |
| Residuals | vs thickness $x$ | No **trend** | Smooth trend $\Rightarrow$ structure unexplained by model |
| Magnitude | $|\hat\varepsilon|$ vs $x$ | Flat or random | Certain thicknesses always worse |
| Distribution | Residual KDE / QQ | QQ roughly on reference | Heavy tails or skew in residuals |
| Distribution | Predicted vs actual KDE | Overlapping modes | Systematic shift or width mismatch |

At $n=51$, treat QQ and fine-grained density features as **suggestive**, not definitive; thickness-residual plots carry more design-specific weight.

---

## Colour cues (aligned with ``PERO``)

- **Sky** scatter: paired $(y, \hat{y})$ or primary series.  
- **Orange**: residual clouds vs fitted values or $x$.  
- **Red**: absolute error emphasis vs $x$.  
- **Green / sky** pairing: sorted actual vs sorted predicted curves.
