# Bivariate Plots

Bivariate views emphasize thickness response behavior for each target using a consistent PERO format. Every figure uses the same dark background, major and minor grids, smoothed curves where appropriate, and mandatory shaded uncertainty regions. Because thickness is highly discrete and many points overlap at the same thickness level, these plots emphasize interpretable structure such as cohort bands and a single linear response rather than stacking many competing trend families.

## Contents And File Types

This folder contains one directory per target. Inside each target directory, the following plots are exported in a fixed order.

- **Scatter With Trends**: jittered scatter for visibility plus a single linear trend. A shaded interquartile cohort band is shown across thickness levels, and an additional shaded band is drawn around the linear trend using residual spread.
- **Sorted Profile**: line only profile ordered by thickness with no markers. The curve is smoothed and accompanied by a shaded interquartile band and boundary lines so the distributional spread remains visible without clutter.
- **Residual Pattern**: residual structure view to detect thickness dependent error patterns and to reveal possible threshold like behavior.

## Interpretation Guidance

For thickness response style plots, interpret the linear trend as a conservative summary of \(\hat{y}(x)\). The cohort band is often more informative than the raw scatter in a discrete design because it shows how the middle half of the distribution shifts with thickness. When the cohort band is wide at a given thickness level, that is evidence of high within cohort variability and should reduce confidence in fine grained thickness optimization.

These plots are in sample descriptive diagnostics and do not prove causality. They are intended to support scientific reasoning about whether the dataset supports linear behavior, weakly nonlinear behavior, or a threshold like effect dominated by the zero thickness cohort. Use the grouped summaries and model diagnostics to corroborate any claim suggested by these bivariate views.

All legend boxes are placed outside the axes region so that shaded bands and curves remain visible. Plot text avoids parentheses and uses Title Case. Scientific quantities use LaTeX style mathtext such as \(R_{\mathrm{ct}}\) and \(Q_{\mathrm{rev}}\) where it improves clarity.
