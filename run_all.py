from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from src.audit import audit_dataset
from src.config import ColumnSpec, RunConfig, get_paths
from src.diagnostics import consolidated_model_comparison_plot, diagnostic_plots_per_target
from src.eda import run_deep_eda
from src.explainability import run_explainability
from src.io_data import prepare_data
from src.model_eval import compute_metrics_per_target, rank_models, summarize_overall
from src.models import build_model_suite, fit_predict
from src.report import ReportInputs, write_summary_report_md
from src.utils import ensure_dir, safe_filename, set_global_plot_style, write_tables_excel
from src.logging_config import configure_matplotlib_backends, setup_pipeline_logging
from src.viz_style import apply_pero_theme
from src.output_readmes import write_output_readme_files


def main() -> int:
    project_root = Path(__file__).parent
    log = setup_pipeline_logging(project_root)
    configure_matplotlib_backends()

    paths = get_paths(project_root)
    colspec = ColumnSpec()
    cfg = RunConfig()

    # Plot styling
    try:
        import seaborn as sns

        set_global_plot_style(sns, cfg)
    except Exception:
        pass
    apply_pero_theme(cfg)

    # Delete previous outputs fully then recreate clean hierarchy
    if paths.outputs_root.exists():
        import shutil

        shutil.rmtree(paths.outputs_root, ignore_errors=True)

    # Create output dirs
    for d in [
        paths.outputs_root,
        paths.eda_root,
        paths.eda_plots,
        paths.eda_tables,
        paths.models_root,
        paths.models_tables,
        paths.models_diagnostics_plots,
        paths.explain_root,
        paths.explain_plots,
        paths.explain_tables,
        paths.reports_root,
    ]:
        ensure_dir(d)

    write_output_readme_files(paths)

    # 1) Load + clean
    if not paths.data_xlsx.exists():
        raise FileNotFoundError(f"Expected dataset not found at: {paths.data_xlsx}")

    bundle = prepare_data(str(paths.data_xlsx), colspec=colspec)
    df = bundle.df
    log.info("Data loaded and validated: shape=%s x_col=%s targets=%s", df.shape, bundle.x_col, len(bundle.y_cols))

    # Data audit
    audit = audit_dataset(df, x_col=bundle.x_col)
    audit.audit_table.to_csv(paths.eda_tables / "00_data_audit_table.csv", index=False)
    audit.thickness_value_counts.to_csv(paths.eda_tables / "00_thickness_value_counts.csv", index=False)
    (paths.eda_tables / "00_duplicates_count.txt").write_text(str(audit.duplicates_count), encoding="utf-8")

    # Also export compact audit to Excel
    write_tables_excel(
        paths.eda_tables / "00_data_audit.xlsx",
        {
            "data_audit": audit.audit_table,
            "thickness_value_counts": audit.thickness_value_counts,
        },
    )

    # 2) Deep EDA
    log.info("Deep exploratory analysis started")
    eda_art = run_deep_eda(
        df=df,
        x_col=bundle.x_col,
        y_cols=list(bundle.y_cols),
        out_plots=paths.eda_plots,
        out_tables=paths.eda_tables,
        cfg=cfg,
    )
    log.info("Deep exploratory analysis completed")

    # 3) Modeling (full-data fit)
    X = bundle.X
    Y = bundle.Y
    model_suite = build_model_suite(random_seed=cfg.random_seed)
    log.info("Model fitting started: %s candidate models", len(model_suite))

    all_metric_tables = []
    model_names = []
    per_model_metrics_paths = []

    for ms in model_suite:
        try:
            log.info("Fitting model: %s", ms.name)
            fitted, pred = fit_predict(ms.estimator, X, Y)
        except Exception:
            log.warning("Model skipped after fit failure: %s", ms.name, exc_info=True)
            continue

        per_target, metrics_tbl = compute_metrics_per_target(
            y_true=Y.to_numpy(dtype=float),
            y_pred=pred,
            y_cols=list(bundle.y_cols),
            n_features_effective=ms.n_features_effective,
        )
        metrics_tbl2 = summarize_overall(metrics_tbl)
        model_names.append(ms.name)
        all_metric_tables.append(metrics_tbl2)

        # Save per-model metrics table
        out_csv = paths.models_tables / f"metrics__{safe_filename(ms.name)}.csv"
        metrics_tbl2.to_csv(out_csv, index=False)
        per_model_metrics_paths.append(out_csv)

        # Diagnostics plots per target (in-sample)
        x_arr = X.iloc[:, 0].to_numpy(dtype=float)
        for j, t in enumerate(bundle.y_cols):
            diagnostic_plots_per_target(
                model_name=ms.name,
                x=x_arr,
                y_true=Y.iloc[:, j].to_numpy(dtype=float),
                y_pred=pred[:, j],
                target_name=t,
                out_dir=paths.models_diagnostics_plots / safe_filename(ms.name) / safe_filename(t),
                cfg=cfg,
            )
    log.info("Model fitting completed: %s models succeeded", len(all_metric_tables))

    if not all_metric_tables:
        log.error("No models produced metrics.")
        raise RuntimeError("No models could be fit successfully. Please ensure scikit-learn is installed correctly.")

    # Model comparison table
    log.info("Model comparison and selection")
    comp = rank_models(all_metric_tables, model_names=model_names)
    comp.to_csv(paths.models_tables / "model_comparison_overall.csv", index=False)
    consolidated_model_comparison_plot(comp, out_dir=paths.models_diagnostics_plots, cfg=cfg)

    # Best overall model
    best_overall_name = comp.iloc[0]["model"]

    # Best model per target (by RMSE)
    best_rows = []
    for target in bundle.y_cols:
        rmse_by_model = []
        for name, tbl in zip(model_names, all_metric_tables, strict=True):
            row = tbl.loc[tbl["target"] == target].iloc[0]
            rmse_by_model.append((name, float(row["RMSE"]), float(row["R2"])))
        rmse_by_model.sort(key=lambda t: t[1])
        best_rows.append({"target": target, "best_model_by_rmse": rmse_by_model[0][0], "RMSE": rmse_by_model[0][1], "R2": rmse_by_model[0][2]})
    best_per_target = pd.DataFrame(best_rows)
    best_per_target.to_csv(paths.models_tables / "best_model_per_target.csv", index=False)

    # Fit best overall model again for explainability (full dataset)
    best_spec = None
    for ms in model_suite:
        if ms.name == best_overall_name:
            best_spec = ms
            break
    if best_spec is None:
        # fallback: first in list
        best_spec = model_suite[0]

    fitted_best, pred_best = fit_predict(best_spec.estimator, X, Y)

    # 5) Explainability
    log.info("Explainability started; best overall=%s", best_overall_name)
    run_explainability(
        model=fitted_best,
        X=X,
        Y=Y,
        y_cols=list(bundle.y_cols),
        out_plots=paths.explain_plots,
        out_tables=paths.explain_tables,
        cfg=cfg,
    )
    log.info("Explainability completed")

    # Export modeling tables to a single Excel
    sheets = {"model_comparison_overall": comp, "best_model_per_target": best_per_target}
    for name, tbl in zip(model_names, all_metric_tables, strict=True):
        sheets[f"metrics__{name}"] = tbl
    write_tables_excel(paths.models_tables / "all_model_metrics.xlsx", sheets)

    # 7) Summary report (Markdown)
    # Correlation table comes from EDA export (thickness vs targets)
    corr_tbl = pd.read_csv(paths.eda_tables / "04_thickness_target_correlations.csv")
    zero_vs_nonzero = pd.read_csv(paths.eda_tables / "06_zero_vs_nonzero_comparison.csv")

    write_summary_report_md(
        paths.reports_root / "summary_report.md",
        ReportInputs(
            x_col=bundle.x_col,
            y_cols=list(bundle.y_cols),
            thickness_counts=audit.thickness_value_counts,
            model_comparison=comp,
            best_model_overall=str(best_overall_name),
            best_model_per_target=best_per_target,
            corr_table=corr_tbl,
            zero_vs_nonzero=zero_vs_nonzero,
        ),
    )
    log.info("Summary report written: %s", paths.reports_root / "summary_report.md")

    log.info("Pipeline finished OK.")
    log.info("Outputs root: %s", paths.outputs_root)
    log.info("EDA plots: %s", paths.eda_plots)
    log.info("Model diagnostics plots: %s", paths.models_diagnostics_plots)
    log.info("Explainability plots: %s", paths.explain_plots)
    log.info("Debug log file: %s", project_root / "logs" / "pipeline.log")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

