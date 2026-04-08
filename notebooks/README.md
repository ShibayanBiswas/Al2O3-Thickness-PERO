# Notebooks Directory

This directory contains notebook level entry points that are suitable for interactive exploration and for creating a report like narrative. The notebook is designed to be a thin wrapper around the modular pipeline so that the primary logic remains in versionable Python modules under `src`. This prevents the common research failure mode where analysis logic is duplicated across notebook cells and becomes difficult to reproduce.

The notebook follows the same strict data rules as the pipeline: it reads only the `Dataset` sheet from the workbook, ignores the sample column, treats thickness as the single input feature, and fits final models on the full dataset. All exports are written to the `outputs` directory so that figures and tables are easy to reference in a manuscript without manual copy steps.

Because the dataset is small and thickness values are discrete, the notebook emphasizes visual diagnostics and careful interpretation. It does not create a train test split by default. Instead it produces in sample diagnostics and allows you to use secondary stability methods if desired without reserving a final holdout set.

Mathematical notation used in figures is rendered with LaTeX style mathtext. This allows consistent representation of scientific quantities such as \(R_{\mathrm{ct}}\) and \(Q_{\mathrm{rev}}\) across notebook displays and exported images. The overall goal is a polished PERO style artifact that can serve as a thesis appendix or technical report supplement.

## Files

- **`Al2O3_Thickness_PERO.ipynb`**: Runs the full pipeline and points to exported outputs.

