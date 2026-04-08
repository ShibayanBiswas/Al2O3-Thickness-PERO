# Data Directory

This directory contains the single authoritative dataset used by the analysis. The pipeline is intentionally strict about data provenance and will only read the Excel file from this location. This ensures that results are reproducible and that accidental copies of the workbook do not silently change the analysis.

The workbook is expected to contain a sheet named `Dataset`, which is treated as the only real data source. The code ignores any accidental header like content in other sheets and it ignores the `Sample` column completely so that the analysis remains a single feature regression study. The feature used is thickness, and all other specified numeric columns are treated strictly as targets.

The dataset is small and thickness values are discrete with a heavy concentration at the zero thickness level. This structure is important for interpretation because it can create visual overlap and cohort like behavior rather than a smooth continuous design. The analysis therefore includes grouped thickness cohort plots and uncertainty bands to respect the true structure of the dataset.

All numeric values are coerced with strict typing rules and validated for missingness. If the file contents change in a way that violates the expected schema, the pipeline will raise an informative error rather than continuing with incorrect assumptions. This makes the PERO style deliverable robust for research workflows.

## Files

- **`Data.xlsx`**: The dataset workbook. The analysis uses only the `Dataset` sheet.

