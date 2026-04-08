# Source Code Index

This directory contains all reusable Python modules for the PERO style analysis. The design goal is modularity and reproducibility: each module has a well defined responsibility, and the end to end pipeline in `run_all.py` composes these modules without duplicating logic. The project uses a single feature design, so the code avoids inventing additional physical features and restricts any engineered transformations to mathematically derived forms of thickness.

The architecture separates data integrity work from visualization and modeling work. Data loading and validation are handled once at the beginning of the pipeline so that all downstream analysis operates on a clean numeric dataframe with known column semantics. Plotting code is centralized so that styling, export behavior, and naming rules remain consistent across hundreds of figures and many tables.

The modeling stack is built for multi output regression with a single input feature. Estimators that do not support multi output natively are wrapped so that a single fit call yields predictions for all targets. Where scaling is required for numerical stability or distance based behavior, a Standard Scaler stage is applied in a pipeline so that the workflow is robust and reproducible.

Mathematical notation is rendered using LaTeX style mathtext where it improves scientific clarity. For example charge transfer resistance is represented as \(R_{\mathrm{ct}}\), and reversible capacity is represented as \(Q_{\mathrm{rev}}\). This improves readability without requiring an external LaTeX installation and ensures consistent symbol formatting across all exported figures.

## Module Inventory

- **`config.py`**: Project paths, column specification, and run configuration parameters.
- **`io_data.py`**: Excel loading from the correct sheet, strict numeric coercion, and integrity validation.
- **`audit.py`**: Data audit table construction and thickness value concentration summaries.
- **`viz_style.py`**: Global PERO style and axis polish helpers.
- **`plots.py`**: Figure creation and saving helpers with consistent export behavior.
- **`eda.py`**: Deep EDA plots and tables, including raincloud plots and scaling comparison views.
- **`models.py`**: Model suite for multi output regression with scaling where appropriate.
- **`model_eval.py`**: Metric computation per target and overall model ranking.
- **`diagnostics.py`**: In sample diagnostics exported into calibration, residual, and distribution subfolders.
- **`explainability.py`**: Permutation importance, PDP and ICE, sensitivity curves, and SHAP exports when compatible.
- **`report.py`**: Summary report generator and Markdown table formatting utilities.
- **`utils.py`**: Filenames, robust statistics helpers, and Excel export helpers.

