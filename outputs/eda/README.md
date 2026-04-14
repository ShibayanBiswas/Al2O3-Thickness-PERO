# Exploratory Data Analysis Outputs

Exploratory Data Analysis (EDA) answers: **what does the dataset actually look like** before we commit to a parametric model? Here the experimental design is unusually simple: one controlled input (**Al₂O₃ thickness** $x\ge 0$ nm, column ``Al2O3 Thickness_nm``) and **four** measured outputs (charge-transfer resistance, coulombic efficiency, reversible capacity, capacity retention). EDA therefore focuses on (i) **where data mass lives** (especially $x=0$ vs sparse positive thicknesses), (ii) **how each $Y_j$ varies with $x$** when many points share the same $x$, and (iii) **linear vs rank association** as a first-pass summary, *not* as a substitute for plotting conditional means.

---

## Layout under ``outputs/eda/``

```
eda/
├── README.md                 (this file)
├── plots/                    (see ``plots/README.md`` + branch READMEs)
│   ├── Univariate/
│   ├── Bivariate/
│   ├── Grouped/
│   └── Relationships/
└── tables/                   (see ``tables/README.md``)
```

---

## Working model (descriptive only)

```math
Y_j = g_j(x) + \eta_j,\qquad j=1,\ldots,4,
```

$g_j$ might be smooth, piecewise, or **cohort-dominated** (almost constant within each discrete $x_k$). $\eta_j$ is everything else (measurement noise, batch effects, unmodeled factors). **EDA does not assume** $\mathbb{E}[\eta_j\mid x]=0$; that is a **modeling** assumption diagnosed later under ``outputs/models/diagnostics_plots/``.

---

## Why discrete $x$ matters pedagogically

When many cells share the same thickness, scatter plots **stack vertically**. The pipeline uses **horizontal jitter** so you can see density; a **trend line** or **IQR band by $x$** is then a visual estimate of central tendency and spread *within this sample*, not proof of a physical law. Always cross-check **grouped tables** (``05_...``, ``group_by_thickness__...``) with **Bivariate** and **Grouped** plots.

---

## Pipeline mapping (code references)

| Stage | Source module | What is written |
| --- | --- | --- |
| Audit (00\_\*) | ``run_all.py`` + ``src/audit.py`` | Early tables + ``00_data_audit.xlsx`` |
| Deep EDA | ``src/eda.py`` ``run_deep_eda()`` | ``01``--``09`` CSVs + full plot hierarchy |

---

## How plots and tables reinforce each other

| Question | Start with table | Then open plot folder |
| --- | --- | --- |
| How many rows per thickness? | ``00_`` / ``03_thickness_value_counts.csv`` | (counts are tabular) |
| Pearson/Spearman vs $x$? | ``04_thickness_target_correlations.csv`` | **Bivariate** / **Relationships** |
| Moments by thickness | ``05_...``, ``group_by_thickness__*.csv`` | **Grouped**, **Bivariate** (IQR bands) |
| Full association matrix | ``07_`` / ``08_`` | **Relationships** heatmaps |

---

## Electrochemical shorthand

Figures use mathtext: $R_{\mathrm{ct}}$, $Q_{\mathrm{rev}}$, etc. Markdown in these READMEs uses GitHub ``$...$`` for inline math and fenced math blocks (three backticks + ``math``) for display.
