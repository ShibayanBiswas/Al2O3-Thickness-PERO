from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ProjectPaths:
    project_root: Path
    data_xlsx: Path
    outputs_root: Path

    # EDA
    eda_root: Path
    eda_plots: Path
    eda_tables: Path

    # Modeling
    models_root: Path
    models_tables: Path
    models_diagnostics_plots: Path

    # Explainability
    explain_root: Path
    explain_plots: Path
    explain_tables: Path

    # Reports
    reports_root: Path


def get_paths(project_root: Path) -> ProjectPaths:
    project_root = project_root.resolve()
    outputs_root = project_root / "outputs"
    eda_root = outputs_root / "eda"
    models_root = outputs_root / "models"
    explain_root = outputs_root / "explainability"
    reports_root = outputs_root / "reports"

    return ProjectPaths(
        project_root=project_root,
        data_xlsx=project_root / "Data" / "Data.xlsx",
        outputs_root=outputs_root,
        eda_root=eda_root,
        eda_plots=eda_root / "plots",
        eda_tables=eda_root / "tables",
        models_root=models_root,
        models_tables=models_root / "tables",
        models_diagnostics_plots=models_root / "diagnostics_plots",
        explain_root=explain_root,
        explain_plots=explain_root / "plots",
        explain_tables=explain_root / "tables",
        reports_root=reports_root,
    )


@dataclass(frozen=True)
class ColumnSpec:
    sheet_name: str = "Dataset"
    ignore_columns: tuple[str, ...] = ("Sample",)
    x_col: str = "Al2O3 Thickness_nm"
    y_cols: tuple[str, ...] = (
        "Rct_initial_ohm",
        "ICE_percent",
        "Initial Reversible Capacity_mAh_g at 0.1C",
        "Highest Capacity Retention_percent",
    )


@dataclass(frozen=True)
class RunConfig:
    random_seed: int = 42
    figure_dpi: int = 220
    figure_format: str = "png"
    seaborn_theme: str = "whitegrid"
    seaborn_context: str = "talk"
    seaborn_palette: str = "deep"

    # For discrete X (many duplicates), jitter helps reveal overlap
    jitter_strength: float = 0.08

    # Binning for group summaries (kept simple because X is already discrete)
    min_points_per_bin: int = 3

