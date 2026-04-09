# Explainability Outputs

Interpretation of how **$\mathrm{Al}_{2}\mathrm{O}_{3}$ thickness** $x$ (``Al2O3 Thickness_nm``) steers the **best-overall** model (lowest mean RMSE across targets), refit on the full sample in ``run_all.py`` via ``run_explainability()`` (``src/explainability.py``).

---

## Layout under ``outputs/explainability/``

```
explainability/
├── README.md           (this file)
├── plots/
│   ├── README.md
│   ├── PartialDependence/
│   ├── Sensitivity/
│   └── Shap/           (optional; requires `shap` + compatible estimator)
└── tables/
    └── README.md
```

---

## Objects

**Permutation importance** -- positive drop in $R^2$ when $x$ is shuffled:

$$
\Delta R^2 = R^2(\text{data}) - R^2(\pi \circ x).
$$

**PDP / ICE** -- mean response vs $x$ plus bootstrap ensemble of univariate prediction curves (ICE band).

**Sensitivity** -- $\hat{y}(x)$ and numerical $\mathrm{d}\hat{y}/\mathrm{d}x$ on a dense grid.

---

## SHAP (optional): no waterfalls

When SHAP applies,

$$
\hat{y}(x) \approx \mathbb{E}[\hat{y}] + \phi(x).
$$

We export **beeswarm**, **bar**, **dependence** only -- **no waterfall figures**. Per-target clones are fit for multi-output models. All SHAP panels use **outside legends** (PERO theme).

---

## Why explainability still matters when $p=1$

With only one feature, some global methods (SHAP for many inputs) collapse to triviality, but **curve-based** views remain essential:

- **PDP / ICE** show how the **fitted** response $\hat{y}_j(x)$ changes along the measured thickness range, including **uncertainty ribbons** from bootstrap refits.  
- **Sensitivity** plots expose $\mathrm{d}\hat{y}_j/\mathrm{d}x$, highlighting regions where the learned map is **steep** (small nm changes imply large predicted response changes).  
- **Permutation importance** asks whether **destroying** the ordering of $x$ while keeping its marginal values collapses $R^2$; large drops mean the model relied on the actual pairing $(x, y)$ in the spreadsheet.

These tools describe the **trained estimator**, not necessarily a physical mechanism.

---

## Relationship to modelling outputs

Explainability is run for the **best overall** model (lowest mean RMSE across targets) after refitting on all data. For other models, use **their** diagnostics under ``outputs/models/diagnostics_plots/<ModelSafe>/`` and compare PDP shapes mentally or re-run a custom script if needed.
