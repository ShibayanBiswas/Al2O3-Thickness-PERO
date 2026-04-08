# Exploratory Plots Index

This plots directory is the visual record of the one dimensional thickness response study. All figures are saved at high resolution using a unified PERO theme that emphasizes contrast, consistent typography, and careful grid treatment. The dataset contains repeated thickness levels, so many plots are designed to reveal overlap and to separate within level variability from between level differences.

The **Univariate** subdirectory contains distribution focused plots for the thickness feature and each target. These include histograms with smooth density overlays, empirical cumulative distribution curves, and robust shape summaries such as box and violin views. The purpose is to understand skewness, tail weight, and whether a small number of extreme observations dominate apparent trends.

The **Bivariate** subdirectory contains thickness response plots for each target. These plots include observed scatter with jittered thickness and a single linear trend line as a conservative summary of \(\hat{y}(x)\). Where appropriate, area fills are used as visual strips to guide the eye without cluttering the central signal.

The **Grouped** and **Relationships** subdirectories summarize cohort behavior and multivariate association diagnostics. Grouped plots treat each discrete thickness value as a cohort and display mean response with uncertainty bands. Relationship plots include correlation heatmaps and optional pair plots for numeric variables, which are diagnostics to complement the one dimensional response narrative rather than replacements for it.
