# Modeling Tables Index

This directory contains all model evaluation tables for the multi output regression suite. Every model is fitted on the full dataset and evaluated in sample, which makes the tables primarily diagnostic. The intent is to rank model families by their ability to represent thickness response structure while remaining scientifically interpretable.

Per model metric tables include target wise error measures and a single overall mean row that summarizes performance across targets. The comparison table aggregates these overall rows to form a leaderboard. A best model per target table is included to reflect that different targets may respond to thickness with different functional shapes.

An Excel workbook export consolidates the full set of metric tables into one file for reporting convenience. This is useful for generating manuscript tables, reviewing model tradeoffs, and verifying that model selection is not driven by a single target at the expense of the others.

All tables are named in a consistent way and avoid parentheses in visible report text. When you cite results, emphasize that the values are in sample diagnostics. Use residual structure plots to validate that an apparently strong metric corresponds to a scientifically plausible response curve rather than to memorization of discrete thickness levels.
