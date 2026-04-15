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
from src.tuning import build_cv_strategies, tune_estimator
from src.utils import ensure_dir, safe_filename, set_global_plot_style, write_tables_excel
from src.logging_config import configure_matplotlib_backends, setup_pipeline_logging
from src.viz_style import apply_pero_theme
from src.output_readmes import write_output_readme_files
from src.plot_notes import write_plot_notes


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

    # Train-only policy (per requirement): all plots and model selection use training data only.
    # With very small n, we treat the full dataset as "training"; hyperparameter search still
    # uses cross-validation inside ``tune_estimator`` (primary CV split).
    df_train, df_test = df, df.iloc[0:0].copy()

    # Data audit
    audit = audit_dataset(df_train, x_col=bundle.x_col)
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
        df=df_train,
        x_col=bundle.x_col,
        y_cols=list(bundle.y_cols),
        out_plots=paths.eda_plots,
        out_tables=paths.eda_tables,
        cfg=cfg,
    )
    log.info("Deep exploratory analysis completed")

    # 3) Modeling (train-only)
    X = df_train[[bundle.x_col]].copy()
    Y = df_train[list(bundle.y_cols)].copy()
    model_suite = build_model_suite(random_seed=cfg.random_seed)
    log.info("Model fitting started: %s candidate models", len(model_suite))

    # Clarify why optional boosters might be missing from outputs/models/diagnostics_plots/.
    # These are disabled by default (Windows native deps can be fragile).
    try:
        import os

        from src.utils import optional_import

        enable_optional = os.environ.get("PERO_ENABLE_OPTIONAL_BOOSTERS", "").strip() in {"1", "true", "True", "YES", "yes"}
        if not enable_optional:
            log.info(
                "Optional external boosters are disabled. Set PERO_ENABLE_OPTIONAL_BOOSTERS=1 to enable XGBoost/LightGBM/CatBoost "
                "(if installed)."
            )
        else:
            log.info(
                "Optional external boosters enabled. Availability: xgboost=%s lightgbm=%s catboost=%s",
                bool(optional_import("xgboost")),
                bool(optional_import("lightgbm")),
                bool(optional_import("catboost")),
            )
    except Exception:
        pass

    all_metric_tables = []
    model_names = []
    per_model_metrics_paths = []
    per_model_params: list[dict] = []
    tuned_by_name: dict[str, object] = {}

    cv_strats = build_cv_strategies(n=int(X.shape[0]), random_seed=cfg.random_seed)
    cv_primary = list(cv_strats.values())[0]

    for ms in model_suite:
        try:
            log.info("Tuning+fitting model (train): %s", ms.name)

            # Lightweight model-specific tuning spaces (all models get at least a pass).
            # Param names follow sklearn's nested estimator convention.
            params = None
            if ms.name == "Ridge Regression":
                params = {"model__alpha": np.logspace(-4, 4, 60)}
            elif ms.name == "Lasso Regression":
                params = {"model__alpha": np.logspace(-5, 1, 80)}
            elif ms.name == "Elastic Net Regression":
                params = {"model__alpha": np.logspace(-5, 1, 80), "model__l1_ratio": np.linspace(0.05, 0.95, 20)}
            elif ms.name.startswith("Polynomial Ridge Degree"):
                params = {"ridge__alpha": np.logspace(-4, 4, 60)}
            elif ms.name.startswith("Polynomial Regression Degree"):
                # No meaningful hyperparameters for LinearRegression in this pipeline.
                params = None
            elif ms.name == "Stochastic Gradient Regression":
                params = {
                    "estimator__sgd__alpha": np.logspace(-6, -1, 60),
                    "estimator__sgd__epsilon": np.linspace(0.02, 0.25, 20),
                }
            elif ms.name == "Decision Tree":
                params = {
                    "max_depth": [None, 2, 3, 4, 5, 6, 8],
                    "min_samples_leaf": [1, 2, 3, 4],
                    "min_samples_split": [2, 3, 4, 6],
                }
            elif ms.name == "Random Forest":
                params = {
                    "n_estimators": [200, 300, 450, 700],
                    "max_depth": [None, 3, 4, 5, 6, 8],
                    "min_samples_leaf": [1, 2, 3],
                    "min_samples_split": [2, 3, 4, 6],
                    "max_features": [1.0, "sqrt"],
                }
            elif ms.name == "Extra Trees":
                params = {
                    "n_estimators": [200, 300, 450, 700],
                    "max_depth": [None, 3, 4, 5, 6, 8],
                    "min_samples_leaf": [1, 2, 3],
                    "min_samples_split": [2, 3, 4, 6],
                    "max_features": [1.0, "sqrt"],
                }
            elif ms.name in {"Gradient Boosting", "Adaptive Boosting", "Histogram Gradient Boosting", "Bagging Regressor"}:
                # These are wrapped in MultiOutputRegressor in build_model_suite; tune via estimator__ prefix.
                if ms.name == "Gradient Boosting":
                    params = {
                        "estimator__n_estimators": [100, 200, 350, 600],
                        "estimator__learning_rate": np.logspace(-2.5, -0.2, 30),
                        "estimator__max_depth": [2, 3, 4],
                        "estimator__subsample": [0.7, 0.85, 1.0],
                    }
                elif ms.name == "Adaptive Boosting":
                    params = {
                        "estimator__n_estimators": [80, 150, 250, 400],
                        "estimator__learning_rate": np.logspace(-2.5, -0.2, 30),
                    }
                elif ms.name == "Histogram Gradient Boosting":
                    params = {
                        "estimator__learning_rate": np.logspace(-2.5, -0.2, 30),
                        "estimator__max_depth": [2, 3, 4, 5, None],
                        "estimator__max_leaf_nodes": [15, 31, 63],
                    }
                else:
                    params = {
                        "estimator__n_estimators": [40, 80, 150, 250],
                        "estimator__max_samples": [0.6, 0.8, 1.0],
                    }
            elif ms.name.startswith("K Nearest Neighbors"):
                params = {"model__n_neighbors": [1, 2, 3, 4, 5, 7, 9]}
            elif ms.name == "Support Vector Regression":
                params = {
                    "estimator__svr__C": np.logspace(-1, 3, 60),
                    "estimator__svr__epsilon": np.linspace(0.01, 0.25, 25),
                    "estimator__svr__gamma": ["scale", "auto"],
                }
            elif ms.name == "Gaussian Process Regression":
                params = {"estimator__alpha": np.logspace(-10, -2, 60)}
            elif ms.name == "Extreme Gradient Boosting":
                params = {
                    "estimator__n_estimators": [250, 400, 700],
                    "estimator__learning_rate": np.logspace(-2.5, -0.2, 30),
                    "estimator__max_depth": [2, 3, 4, 5],
                    "estimator__subsample": [0.7, 0.85, 1.0],
                    "estimator__colsample_bytree": [0.7, 0.85, 1.0],
                    "estimator__reg_lambda": np.logspace(-3, 1.2, 25),
                }
            elif ms.name == "Light Gradient Boosting":
                params = {
                    "estimator__n_estimators": [250, 400, 700],
                    "estimator__learning_rate": np.logspace(-2.5, -0.2, 30),
                    "estimator__num_leaves": [7, 15, 31, 63],
                    "estimator__min_child_samples": [3, 5, 10, 20],
                }
            elif ms.name == "Categorical Boosting":
                params = {
                    "estimator__iterations": [250, 450, 800],
                    "estimator__learning_rate": np.logspace(-2.5, -0.2, 30),
                    "estimator__depth": [2, 3, 4, 5, 6],
                    "estimator__l2_leaf_reg": np.logspace(-2, 1.5, 30),
                }

            tuned_est, best_params, best_cv_r2 = tune_estimator(
                ms.name, ms.estimator, params, X, Y, random_seed=cfg.random_seed, cv_primary=cv_primary, n_iter=18
            )
            tuned_by_name[ms.name] = tuned_est
            per_model_params.append({"model": ms.name, "best_cv_r2_primary": best_cv_r2, **best_params})
            # Persist tuning progress so partial runs still leave evidence.
            try:
                pd.DataFrame(per_model_params).to_csv(paths.models_tables / "tuning_best_params.csv", index=False)
            except Exception:
                pass

            fitted, pred = fit_predict(tuned_est, X, Y)
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

        # Diagnostics plots per target (training)
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

    if per_model_params:
        tuning_tbl = pd.DataFrame(per_model_params)
        tuning_tbl.to_csv(paths.models_tables / "tuning_best_params.csv", index=False)
        # A simple CV-centric comparison: rank by primary CV mean R2 (descending).
        if "best_cv_r2_primary" in tuning_tbl.columns:
            comp_cv = tuning_tbl[["model", "best_cv_r2_primary"]].copy()
            comp_cv = comp_cv.sort_values(
                "best_cv_r2_primary", ascending=False, na_position="last"
            ).reset_index(drop=True)
            comp_cv["rank_by_cv_r2"] = np.arange(1, comp_cv.shape[0] + 1)
            comp_cv.to_csv(paths.models_tables / "model_comparison_cv_r2.csv", index=False)

    # Best overall model: prefer CV ranking if available (more honest for tuning).
    best_overall_name = comp.iloc[0]["model"]
    try:
        comp_cv_path = paths.models_tables / "model_comparison_cv_r2.csv"
        if comp_cv_path.exists():
            comp_cv = pd.read_csv(comp_cv_path)
            if comp_cv.shape[0] > 0 and "model" in comp_cv.columns:
                if "best_cv_r2_primary" in comp_cv.columns:
                    cv_scores = pd.to_numeric(comp_cv["best_cv_r2_primary"], errors="coerce")
                    finite = comp_cv[np.isfinite(cv_scores.to_numpy(dtype=float))]
                    if finite.shape[0] > 0:
                        best_overall_name = str(finite.iloc[0]["model"])
                    else:
                        best_overall_name = str(comp_cv.iloc[0]["model"])
                else:
                    best_overall_name = str(comp_cv.iloc[0]["model"])
    except Exception:
        pass

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

    # Fit best overall model again for explainability (training only)
    best_spec = None
    for ms in model_suite:
        if ms.name == best_overall_name:
            best_spec = ms
            break
    if best_spec is None:
        # fallback: first in list
        best_spec = model_suite[0]

    best_est = tuned_by_name.get(best_overall_name, best_spec.estimator)
    fitted_best, pred_best = fit_predict(best_est, X, Y)

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

    # 8) Plot notes (per-folder interpretation guides)
    try:
        written = write_plot_notes(paths.outputs_root)
        log.info("Plot notes written: %s files", len(written))
    except Exception:
        log.warning("Plot notes writer failed", exc_info=True)

    log.info("Pipeline finished OK.")
    log.info("Outputs root: %s", paths.outputs_root)
    log.info("EDA plots: %s", paths.eda_plots)
    log.info("Model diagnostics plots: %s", paths.models_diagnostics_plots)
    log.info("Explainability plots: %s", paths.explain_plots)
    log.info("Debug log file: %s", project_root / "logs" / "pipeline.log")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

