# Exploratory Tables Index

This tables directory contains export ready CSV and Excel outputs that support the EDA narrative. The tables are designed to be compact but complete, allowing direct insertion into a manuscript or appendix. Because the dataset is small, these tables provide transparent visibility into value ranges and thickness level balance.

The data audit tables provide dtype verification, missingness confirmation, unique counts, and both classical and robust summary statistics. Robust summaries include median and interquartile range, which are helpful when a few extreme points exist. Thickness value counts explicitly quantify how much mass sits at the zero thickness level, which is central to interpreting all downstream trends.

Grouped summary tables report thickness cohort statistics across all targets, including count, mean, median, standard deviation, and extrema. These tables are the backbone of discrete level comparison and are especially important when scatter plots contain heavy overlap. A separate comparison table contrasts the zero thickness cohort against the pooled non zero cohort as a diagnostic of threshold like behavior.

Correlation tables are provided for Pearson and Spearman metrics. In a discrete one dimensional setting, these are treated as descriptive diagnostics rather than definitive claims. Use them alongside the plots and the grouped tables to form a consistent scientific interpretation of thickness response behavior.
