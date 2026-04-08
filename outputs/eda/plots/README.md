# Exploratory Plots Index

This plots directory is the visual record of the one dimensional thickness response study. All figures are saved at high resolution using a unified PERO theme that emphasizes contrast, consistent typography, and careful grid treatment. The dataset contains repeated thickness levels, so many plots are designed to reveal overlap and to separate within level variability from between level differences.

The **Univariate** subdirectory contains distribution focused plots for the thickness feature and each target. These include histograms with smooth density overlays, empirical cumulative distribution curves, and robust shape summaries such as box and violin views. The purpose is to understand skewness, tail weight, and whether a small number of extreme observations dominate apparent trends.

The **Bivariate** subdirectory contains thickness response plots for each target. These plots include observed scatter with jittered thickness, a single linear trend line, and mandatory shaded bands such as interquartile envelopes across thickness cohorts and trend bands around the fitted linear response. Because thickness is discrete, shaded cohort bands are often more informative than dense point clouds. Legends are placed outside the axes region to prevent overlap with data and uncertainty bands.

The **Grouped** and **Relationships** subdirectories summarize cohort behavior and multivariate association diagnostics. Grouped plots treat each discrete thickness value as a cohort and display mean response with uncertainty bands. Relationship plots include correlation heatmaps and optional pair plots for numeric variables, which are diagnostics to complement the one dimensional response narrative rather than replacements for it.

All curve style plots in this directory are exported as smooth lines without markers unless the plot type inherently requires point glyphs. Shaded area fills and boundary lines are used to improve readability and to highlight uncertainty or distributional spread. Grid styling uses both major and minor grids so that values can be read precisely without turning the plot into visual noise.
