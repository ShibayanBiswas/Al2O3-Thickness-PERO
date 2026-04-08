from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.config import ColumnSpec, RunConfig, get_paths
from src.explainability import run_explainability
from src.io_data import prepare_data
from src.model_eval import rank_models
from src.models import build_model_suite, fit_predict
from src.report import ReportInputs, write_summary_report_md
from src.utils import ensure_dir, safe_filename, write_tables_excel


def main() -> int:
    project_root = Path(__file__).parent
    paths = get_paths(project_root)
    colspec = ColumnSpec()
    cfg = RunConfig()

    ensure_dir(paths.models_tables)
    ensure_dir(paths.explain_plots)
    ensure_dir(paths.explain_tables)
    ensure_dir(paths.reports_root)

    # Load per-model metric CSVs created by run_all
    metric_files = sorted(paths.models_tables.glob("metrics__*.csv"))
    if not metric_files:
        raise FileNotFoundError("No metrics__*.csv files found. Run run_all.py first.")

    model_names: list[str] = []
    model_tables: list[pd.DataFrame] = []
    for f in metric_files:
        name = f.stem.replace("metrics__", "")
        tbl = pd.read_csv(f)
        model_names.append(name)
        model_tables.append(tbl)

    comp = rank_models(model_tables, model_names=model_names)
    comp.to_csv(paths.models_tables / "model_comparison_overall.csv", index=False)

    # Best model per target by RMSE
    y_cols = list(colspec.y_cols)
    best_rows = []
    for target in y_cols:
        rmse_by_model = []
        for name, tbl in zip(model_names, model_tables, strict=True):
            row = tbl.loc[tbl["target"] == target].iloc[0]
            rmse_by_model.append((name, float(row["RMSE"]), float(row["R2"])))
        rmse_by_model.sort(key=lambda t: t[1])
        best_rows.append(
            {
                "target": target,
                "best_model_by_rmse": rmse_by_model[0][0],
                "RMSE": rmse_by_model[0][1],
                "R2": rmse_by_model[0][2],
            }
        )
    best_per_target = pd.DataFrame(best_rows)
    best_per_target.to_csv(paths.models_tables / "best_model_per_target.csv", index=False)

    # Excel workbook containing all metrics and selection tables
    sheets = {"model_comparison_overall": comp, "best_model_per_target": best_per_target}
    for name, tbl in zip(model_names, model_tables, strict=True):
        sheets[f"metrics__{name}"] = tbl
    write_tables_excel(paths.models_tables / "all_model_metrics.xlsx", sheets)

    # Fit the best overall model for explainability
    best_overall_name = str(comp.iloc[0]["model"])
    suite = build_model_suite(random_seed=cfg.random_seed)
    best_spec = next((ms for ms in suite if ms.name == best_overall_name), None)
    if best_spec is None:
        # fallback to first in suite
        best_spec = suite[0]

    bundle = prepare_data(str(paths.data_xlsx), colspec=colspec)
    fitted_best, _ = fit_predict(best_spec.estimator, bundle.X, bundle.Y)

    run_explainability(
        model=fitted_best,
        X=bundle.X,
        Y=bundle.Y,
        y_cols=list(bundle.y_cols),
        out_plots=paths.explain_plots,
        out_tables=paths.explain_tables,
        cfg=cfg,
    )

    # Summary report
    thickness = pd.read_csv(paths.eda_tables / "00_thickness_value_counts.csv")
    corr = pd.read_csv(paths.eda_tables / "04_thickness_target_correlations.csv")
    zvs = pd.read_csv(paths.eda_tables / "06_zero_vs_nonzero_comparison.csv")
    write_summary_report_md(
        paths.reports_root / "summary_report.md",
        ReportInputs(
            x_col=colspec.x_col,
            y_cols=y_cols,
            thickness_counts=thickness,
            model_comparison=comp,
            best_model_overall=best_overall_name,
            best_model_per_target=best_per_target,
            corr_table=corr,
            zero_vs_nonzero=zvs,
        ),
    )

    print("Postprocess Completed", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

