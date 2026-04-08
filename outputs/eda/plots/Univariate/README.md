# Univariate Plots

Univariate views emphasize distributional shape, robust spread, and tail structure for each variable. Each figure is exported with consistent background and grid styling to support direct insertion into a report. Because the dataset is small and many thickness values are repeated, the univariate suite is designed to show both smooth distributional behavior and discrete clustering.

## Folder Structure

This directory contains one subfolder per variable. Each variable subfolder contains a consistent set of images. This design keeps file names short and prevents Windows path issues while also making it easy to cite a specific variable in a report.

## Contents In Each Variable Folder

- **Histogram And Kernel Density**: a distribution overview with a smooth density curve.
- **Box And Violin**: robust summaries of central tendency and spread. These are useful when the distribution is skewed or has heavy tails.
- **Raincloud Plot**: a compact combined view that overlays a violin density, a box summary, and a jittered strip of points to reveal discrete stacking.
- **Empirical Cumulative Distribution**: a marker free line style cumulative distribution with a shaded area under the curve.
- **Scaling Comparison Density**: a multi scaler comparison that overlays density curves for Original Scale, Standard Scale, Min Max Scale, Robust Scale, Max Abs Scale, Quantile Normal Scale, Quantile Uniform Scale, and Power Yeo Johnson Scale.

## Style Guarantees

All plots in this directory use the PERO dark background, major and minor grids, smoothed lines for curve style plots, and shaded areas where appropriate. Legends are placed outside the axes region when multiple curves are present so that the distribution shapes remain readable. Plot text avoids parentheses and uses Title Case. Mathematical notation uses LaTeX style mathtext where it improves scientific clarity.
