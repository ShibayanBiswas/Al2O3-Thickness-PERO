from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

from .utils import ensure_dir


@dataclass(frozen=True)
class ReportInputs:
    x_col: str
    y_cols: list[str]
    thickness_counts: pd.DataFrame
    model_comparison: pd.DataFrame
    best_model_overall: str
    best_model_per_target: pd.DataFrame
    corr_table: pd.DataFrame
    zero_vs_nonzero: pd.DataFrame


def df_to_markdown_table(df: pd.DataFrame, max_rows: int | None = None) -> str:
    """
    Minimal dependency-free GitHub-flavored Markdown table renderer.
    Avoids pandas.DataFrame.to_markdown() so the pipeline never depends on `tabulate`.
    """
    if max_rows is not None and df.shape[0] > max_rows:
        df = df.head(max_rows).copy()

    # Convert to strings for stable formatting
    df2 = df.copy()
    for c in df2.columns:
        df2[c] = df2[c].map(lambda v: "" if pd.isna(v) else str(v))

    headers = list(df2.columns)
    lines = []
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
    for _, row in df2.iterrows():
        lines.append("| " + " | ".join(row.tolist()) + " |")
    return "\n".join(lines)


def _strength_word(r: float) -> str:
    ar = abs(r)
    if ar >= 0.8:
        return "strong"
    if ar >= 0.5:
        return "moderate"
    if ar >= 0.3:
        return "weak-to-moderate"
    return "weak"


def write_summary_report_md(out_path: Path, ri: ReportInputs) -> None:
    ensure_dir(out_path.parent)

    lines: list[str] = []
    lines.append("# PERO Summary Report: Al₂O₃ thickness → multi-output response")
    lines.append("")
    lines.append("## Notation")
    lines.append("")
    lines.append(
        "Let $x \\in \\mathbb{R}_{\\ge 0}$ denote the single engineered input (Al₂O₃ thickness, nm), stored in the dataset as the column "
        "`Al2O3 Thickness_nm`. Targets form $\\mathbf{y} = (y_1,\\dots,y_4)^\\top$ over the four electrochemical metrics named below. "
        "Each fitted model implements a map $\\hat{\\mathbf{f}} : x \\mapsto \\widehat{\\mathbf{y}}$ trained on the full tabulated sample; every scalar error metric is therefore **in-sample** unless stated otherwise."
    )
    lines.append("")
    lines.append("## Data integrity snapshot")
    lines.append(f"- **Feature (only input)**: `{ri.x_col}`")
    lines.append("- **Targets**:")
    for t in ri.y_cols:
        lines.append(f"  - `{t}`")
    lines.append("")
    lines.append("### Thickness discreteness & concentration")
    top_counts = ri.thickness_counts.sort_values("count", ascending=False).head(10)
    lines.append(df_to_markdown_table(top_counts))
    lines.append("")
    if (ri.thickness_counts[ri.x_col] == 0.0).any():
        z = ri.thickness_counts.loc[ri.thickness_counts[ri.x_col] == 0.0].iloc[0]
        lines.append(f"- **Zero-thickness group**: {int(z['count'])} rows ({float(z['fraction'])*100:.1f}% of dataset)")
    lines.append("")

    lines.append("## EDA: thickness ↔ target association (1D setting)")
    lines.append("Correlation is only a **first-pass** indicator in a highly discrete single-feature dataset; nonlinearity/thresholds can matter more than a single coefficient.")
    lines.append("")
    lines.append("### Pearson & Spearman (thickness vs each target)")
    lines.append(df_to_markdown_table(ri.corr_table))
    lines.append("")

    lines.append("### 0.0 nm vs non-zero thickness comparison")
    lines.append("This contrasts the large `0.0 nm` cluster against the pooled non-zero thicknesses (diagnostic; not causal).")
    lines.append("")
    lines.append(df_to_markdown_table(ri.zero_vs_nonzero))
    lines.append("")

    lines.append("## Modeling (in-sample / full-data fit by requirement)")
    lines.append("- No normal train/test split was used; final models are fitted on **all 51 rows**.")
    lines.append("- Metrics and residual diagnostics are **in-sample** and should be read as *fit/diagnostic* rather than generalization guarantees.")
    lines.append("")

    lines.append("### Overall model leaderboard (mean across targets)")
    lines.append(df_to_markdown_table(ri.model_comparison.head(15)))
    lines.append("")
    lines.append(f"- **Best overall model (by overall mean RMSE)**: `{ri.best_model_overall}`")
    lines.append("")

    lines.append("### Best model per target (by RMSE)")
    lines.append(df_to_markdown_table(ri.best_model_per_target))
    lines.append("")

    lines.append("## Scientific interpretation (1D thickness-response)")
    lines.append("")
    lines.append(
        "With $p=1$, estimator flexibility governs how $\\mathbb{E}[Y_j \\mid x]$ is approximated: **affine**, "
        "**smooth nonlinear** ($\\hat{y}_j \\in C^k$ for low $k$), or **threshold / cohort-segmented** behavior at the discrete support of $x$. "
        "In-sample $R^2$ can rise via interpolation of thickness cohorts; the decisive diagnostic is residual structure **vs.** $x$ "
        "and the plausibility of $\\mathrm{d}\\hat{y}_j/\\mathrm{d}x$ on the nm axis."
    )
    lines.append("")
    lines.append(
        "Consult `outputs/eda/plots/` and `outputs/models/diagnostics_plots/` for overlap-aware scatter, parity lines, "
        "and residual sweeps keyed to thickness."
    )
    lines.append("")
    lines.append("## Metric definitions (in-sample)")
    lines.append("")
    lines.append("Residuals $\\hat{\\varepsilon}_{ij} = y_{ij} - \\hat{y}_{ij}$. For each target $j$:")
    lines.append("")
    # Fenced math block (GitHub-flavored Markdown) for reliable display rendering.
    lines.append("```math")
    lines.append(
        "\\mathrm{MAE}_j = \\frac{1}{n}\\sum_{i=1}^{n}\\bigl|\\hat{\\varepsilon}_{ij}\\bigr|,\\qquad "
        "\\mathrm{RMSE}_j = \\sqrt{\\frac{1}{n}\\sum_{i=1}^{n}\\hat{\\varepsilon}_{ij}^{2}},\\qquad "
        "R^{2}_j = 1 - \\frac{\\sum_i \\hat{\\varepsilon}_{ij}^{2}}{\\sum_i (y_{ij}-\\bar{y}_j)^{2}}."
    )
    lines.append("```")
    lines.append("")

    out_path.write_text("\n".join(lines), encoding="utf-8")

