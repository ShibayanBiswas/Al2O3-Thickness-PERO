# Plot Notes — `eda/plots/Relationships`

This file is auto-written by the pipeline to describe what each figure in this folder is intended to communicate. All statements are *interpretive guides* to the plotted objects (curves, residuals, densities), not guarantees of causal mechanism.

## Notation

- Thickness: $x$ (nm)
- Target: $Y_j$
- Prediction: $\hat y_j(x)$
- Residual: $\hat\varepsilon_i = y_i-\hat y_i$

## Figures in this folder

### `Correlation Heatmap Pearson.png`

**Type**: Correlation heatmap (association screen)

**What it is saying**: Displays the association matrix among numeric variables. Pearson captures linear association; Spearman captures monotone rank association. Use as a screening tool; always validate shape with bivariate plots and residual diagnostics.

### `Correlation Heatmap Spearman.png`

**Type**: Correlation heatmap (association screen)

**What it is saying**: Displays the association matrix among numeric variables. Pearson captures linear association; Spearman captures monotone rank association. Use as a screening tool; always validate shape with bivariate plots and residual diagnostics.

### `Pair Plot Numeric Variables.png`

**Type**: Pair plot (optional multivariate view)

**What it is saying**: Shows pairwise scatter/density among numeric columns. With small $n$, treat fine structure as suggestive; look for gross nonlinearity and outliers.
