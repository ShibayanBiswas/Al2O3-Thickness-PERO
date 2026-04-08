# Exploratory Tables Index

Numeric companion to the figure tree: CSV + XLSX tables that tabulate the empirical law of $x$ (thickness) and the joint law of $(x, Y_j)$. Each frame is sized for thesis appendices—dense but legible, with moments that behave well under heavy tails.

Data audits enumerate dtypes, missingness, cardinalities, medians, and IQRs. Thickness frequency tables quantify the atom at $x=0$ versus sparse nonzero nm levels—the single most important structural fact for every downstream statistic.

Cohort summaries stratify by each observed $x$: $n$, $\bar Y_j$, $\mathrm{median}(Y_j)$, $s$, and extrema. A pooled contrast (`0` nm vs. $\{x > 0\}$) formalizes threshold narratives without asserting causality.

Bivariate summaries list Pearson $\rho$ and Spearman $r_s$ between $x$ and each $Y_j$. In this quasi-factorial 1D design they are **descriptive** alignment scores, not substitutes for inspecting $\mathbb{E}[Y_j \mid x]$ nonlinearity.
