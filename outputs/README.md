# Outputs -- Full Layout And Contents

Everything here is produced by ``py run_all.py`` (or refreshed in part by ``py postprocess.py``). This README is the **top-level index**: it lists the tree, links to deeper guides, and explains how figures and tables fit into a coherent scientific story.

---

## Suggested reading order (for learning the results)

1. **``eda/tables/README.md``** plus **``eda/plots/README.md``** -- understand the *empirical* thickness--response structure (counts, correlations, cohort summaries, and graphics).  
2. **``models/tables/README.md``** -- scalar fit quality (in-sample) for every candidate model.  
3. **``models/diagnostics_plots/README.md``** -- *shape* of errors (parity, residuals vs thickness, QQ).  
4. **``explainability/``** -- how the **chosen** best-overall model maps thickness to predictions (PDP/ICE, sensitivity, optional SHAP, permutation table).  
5. **``reports/summary_report.md``** -- compact narrative with the same tables embedded.

Each subdirectory README is written to **teach** what the files mean, not only where they sit on disk.

---

## Visual style (figures)

All Matplotlib exports share the **PERO dark theme** configured in ``src/viz_style.py``:

- **Background** deep navy (``PERO.bg``), **axes** and **grid** tuned for contrast without clutter.  
- **Semantic colours** (also ``PeroPalette`` / ``PERO``): e.g. **sky** for primary data traces, **orange** for residuals and KDE overlays, **green** for cohort / median summaries, **red** for magnitude-of-error emphasis, **text** (mist white) for reference lines and ICE/uncertainty ribbons.  
- **Legends** sit **outside** the plotting region when multiple series appear, so points and bands stay visible.  
- **Mathtext** (STIX) for chemistry and symbols on axes (e.g. $\mathrm{Al}_{2}\mathrm{O}_{3}$, $R_{\mathrm{ct}}$).  
- Default **PNG**, **220 DPI** (``RunConfig.figure_format``, ``RunConfig.figure_dpi`` in ``src/config.py``).

EDA heatmaps use the ``vlag`` diverging map with thin **cell outlines** so tiles read clearly on dark backgrounds.

**Filenames** are sanitized with ``safe_filename()`` so paths are portable; compare stems to this documentation if a column name contained special characters.

---

## Directory tree (canonical)

```
outputs/
├── README.md                          (this file)
├── eda/
│   ├── README.md
│   ├── plots/
│   │   ├── README.md
│   │   ├── Univariate/<VariableTitle>/   (1 folder per feature + each target)
│   │   ├── Bivariate/<TargetTitle>/      (1 folder per electrochemical target)
│   │   ├── Grouped/<TargetTitle>/
│   │   └── Relationships/                (heatmaps + optional pair plot)
│   └── tables/                           (CSV, XLSX, one audit TXT)
├── models/
│   ├── README.md
│   ├── tables/
│   │   └── README.md
│   └── diagnostics_plots/
│       ├── README.md
│       ├── Model Comparison Overall Error.png
│       └── <ModelSafeName>/<TargetSafeName>/
│           ├── Calibration/
│           ├── Residuals/
│           └── Distributions/
├── explainability/
│   ├── README.md
│   ├── plots/
│   │   ├── README.md
│   │   ├── PartialDependence/
│   │   ├── Sensitivity/
│   │   └── Shap/                         (optional; requires SHAP + compatible estimator)
│   └── tables/
│       └── README.md
└── reports/
    ├── README.md
    └── summary_report.md                 (data-driven narrative + tables)
```

---

## Cross-links

| If you need... | Go to |
| --- | --- |
| Raw audit + correlation CSVs | ``eda/tables/README.md`` |
| Plot naming per EDA branch | ``eda/plots/README.md`` and subfolder READMEs |
| Per-model CSV metrics + XLSX | ``models/tables/README.md`` |
| Parity / residual file names | ``models/diagnostics_plots/README.md`` |
| PDP, sensitivity, SHAP file stems | ``explainability/plots/README.md`` |
| Permutation CSV columns | ``explainability/tables/README.md`` |
| Single-report PDF-style summary | ``reports/summary_report.md`` |

---

## Regeneration note

``run_all.py`` **deletes** the previous ``outputs/`` tree before rebuilding. Commit or copy anything you need to keep before re-running.
