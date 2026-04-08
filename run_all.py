from __future__ import annotations

import sys
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
from src.viz_style import apply_pero_theme


def main() -> int:
    project_root = Path(__file__).parent
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
        paths.eda_plots,
        paths.eda_tables,
        paths.models_tables,
        paths.models_diagnostics_plots,
        paths.explain_plots,
        paths.explain_tables,
        paths.reports_root,
    ]:
        ensure_dir(d)

    # Detailed PERO-style READMEs (four paragraphs minimum each)
    (paths.eda_root / "README.md").write_text(
        "\n".join(
            [
                "# Exploratory Data Analysis Outputs",
                "",
                "This directory contains a complete exploratory analysis of the one dimensional input variable that represents the aluminum oxide thickness and the four electrochemical targets. The figures are designed to be publication ready, with consistent typography, grid treatment, and color contrast. The EDA is intentionally deep because the dataset is small and thickness values are discrete, which makes visual diagnostics more important than relying on a single summary statistic.",
                "",
                "The **Plots** folder is organized into univariate, bivariate, grouped, and relationship views. Univariate views describe distributional shape, tail behavior, and outlier structure using histograms with smooth density overlays, empirical cumulative distributions, and robust box and violin summaries. Bivariate views focus on how the response changes with thickness using observed scatter, smooth trends, and polynomial trends, with careful attention to overlapping points created by repeated thickness levels. Grouped views treat each thickness level as a cohort and visualize mean behavior with uncertainty bands to help separate signal from repeated measurement variation.",
                "",
                "The **Tables** folder contains audit and summary tables that are export friendly. The audit includes dtype checks, missingness verification, and robust statistics such as median and interquartile range. Thickness concentration is explicitly quantified, and thickness level grouping tables report count, mean, median, standard deviation, and extrema for each target. Correlation tables include Pearson and Spearman measures and are intended as diagnostics rather than causal claims in a discrete one dimensional design.",
                "",
                "Mathematical notation in plots uses LaTeX style mathtext where it improves clarity, such as \(R_{\\mathrm{ct}}\) for charge transfer resistance and \(Q_{\\mathrm{rev}}\) for reversible capacity. Because the feature space is one dimensional, all conclusions should be interpreted as thickness response behavior rather than multivariate effects. Use these exports as a thesis appendix grade record of what the dataset supports and what it does not support.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    # Subfolder READMEs for plots and tables with detailed guidance
    ensure_dir(paths.eda_plots)
    ensure_dir(paths.eda_tables)
    (paths.eda_plots / "README.md").write_text(
        "\n".join(
            [
                "# Exploratory Plots Index",
                "",
                "This plots directory is the visual record of the one dimensional thickness response study. All figures are saved at high resolution using a unified PERO theme that emphasizes contrast, consistent typography, and careful grid treatment. The dataset contains repeated thickness levels, so many plots are designed to reveal overlap and to separate within level variability from between level differences.",
                "",
                "The **Univariate** subdirectory contains distribution focused plots for the thickness feature and each target. These include histograms with smooth density overlays, empirical cumulative distribution curves, and robust shape summaries such as box and violin views. The purpose is to understand skewness, tail weight, and whether a small number of extreme observations dominate apparent trends.",
                "",
                "The **Bivariate** subdirectory contains thickness response plots for each target. These plots include observed scatter with jittered thickness, smooth trends, and polynomial trend families that help assess whether the data supports linear, weakly nonlinear, or strongly nonlinear behavior. Where appropriate, area fills are used as visual strips to guide the eye without cluttering the central signal.",
                "",
                "The **Grouped** and **Relationships** subdirectories summarize cohort behavior and multivariate association diagnostics. Grouped plots treat each discrete thickness value as a cohort and display mean response with uncertainty bands. Relationship plots include correlation heatmaps and optional pair plots for numeric variables, which are diagnostics to complement the one dimensional response narrative rather than replacements for it.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    for sub_name, sub_desc in [
        ("Univariate", "Univariate views emphasize distributional shape, robust spread, and tail structure for each variable."),
        ("Bivariate", "Bivariate views emphasize thickness response behavior for each target using trends and uncertainty aware overlays."),
        ("Grouped", "Grouped views emphasize cohort comparisons across discrete thickness levels with uncertainty bands."),
        ("Relationships", "Relationship views emphasize correlation diagnostics among numeric variables as complementary context."),
    ]:
        sub_dir = paths.eda_plots / sub_name
        ensure_dir(sub_dir)
        (sub_dir / "README.md").write_text(
            "\n".join(
                [
                    f"# {sub_name} Plots",
                    "",
                    f"{sub_desc} Each figure is exported with consistent background and grid styling to support direct insertion into a report. Because the dataset is small, these plots are intentionally clean and avoid excessive panel counts that would reduce interpretability.",
                    "",
                    "For distribution style plots, focus on whether the observed values cluster tightly at a small set of levels or whether the variable behaves continuously. For thickness, the concentration at the zero level is expected to be dominant, so plots should be interpreted in a mixed discrete and continuous sense. The goal is not to force a continuous narrative but to represent what the experiment actually provides.",
                    "",
                    "For response style plots, interpret trends as hypotheses about \(\\hat{y}(x)\) rather than as proofs of causality. Smooth curves are included to reveal potential monotonic or threshold like patterns, while polynomial trends provide a controlled way to test curvature up to cubic behavior. In a one dimensional design, curvature is the main model choice dimension.",
                    "",
                    "All plot text follows a strict formatting rule to avoid parentheses and to keep labels in Title Case. Mathematical terms use LaTeX style mathtext when it improves scientific clarity, such as \(R_{\\mathrm{ct}}\) and \(Q_{\\mathrm{rev}}\). This keeps the visuals both professional and mathematically correct without requiring a full LaTeX installation.",
                    "",
                ]
            ),
            encoding="utf-8",
        )

    (paths.eda_tables / "README.md").write_text(
        "\n".join(
            [
                "# Exploratory Tables Index",
                "",
                "This tables directory contains export ready CSV and Excel outputs that support the EDA narrative. The tables are designed to be compact but complete, allowing direct insertion into a manuscript or appendix. Because the dataset is small, these tables provide transparent visibility into value ranges and thickness level balance.",
                "",
                "The data audit tables provide dtype verification, missingness confirmation, unique counts, and both classical and robust summary statistics. Robust summaries include median and interquartile range, which are helpful when a few extreme points exist. Thickness value counts explicitly quantify how much mass sits at the zero thickness level, which is central to interpreting all downstream trends.",
                "",
                "Grouped summary tables report thickness cohort statistics across all targets, including count, mean, median, standard deviation, and extrema. These tables are the backbone of discrete level comparison and are especially important when scatter plots contain heavy overlap. A separate comparison table contrasts the zero thickness cohort against the pooled non zero cohort as a diagnostic of threshold like behavior.",
                "",
                "Correlation tables are provided for Pearson and Spearman metrics. In a discrete one dimensional setting, these are treated as descriptive diagnostics rather than definitive claims. Use them alongside the plots and the grouped tables to form a consistent scientific interpretation of thickness response behavior.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    (paths.models_root / "README.md").write_text(
        "\n".join(
            [
                "# Modeling Outputs And Diagnostics",
                "",
                "This directory contains multi output regression models that map thickness to four targets. All models are fitted on the full dataset by requirement, meaning every metric and every diagnostic plot is an in sample fit diagnostic. This is appropriate for a tiny dataset where reserving a holdout set would reduce already limited information, but it also means performance values should be interpreted as calibration of fit rather than guaranteed out of sample accuracy.",
                "",
                "The **Tables** subdirectory includes per model per target error metrics such as mean absolute error, root mean squared error, and coefficient of determination, plus a compact overall comparison leaderboard created by averaging across targets. A separate selection table identifies the best model per target based on error ranking. The Excel export consolidates all metric tables into a single workbook for easy reporting and cross checking.",
                "",
                "The **Diagnostics Plots** subdirectory contains a complete set of residual and calibration views for every model and every target. Parity plots visualize alignment between predicted and observed values, while residual plots against predicted values, observed values, and thickness reveal structured error that suggests underfitting or overfitting. Distribution checks include residual histograms with smooth density overlays and Qq plots that assess departures from normal error assumptions when such assumptions are relevant to interpretation.",
                "",
                "Because the feature space has only one variable, many complex models can memorize discrete thickness levels. The diagnostics are therefore designed to expose this behavior through residual structure and predicted distribution collapse. Use these plots as a scientific honesty layer: a model with a very small residual may still be unreliable if it only interpolates a sparse set of non zero thickness levels. The most useful model is the one that fits well while remaining interpretable in a thickness response context.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    ensure_dir(paths.models_tables)
    ensure_dir(paths.models_diagnostics_plots)
    (paths.models_tables / "README.md").write_text(
        "\n".join(
            [
                "# Modeling Tables Index",
                "",
                "This directory contains all model evaluation tables for the multi output regression suite. Every model is fitted on the full dataset and evaluated in sample, which makes the tables primarily diagnostic. The intent is to rank model families by their ability to represent thickness response structure while remaining scientifically interpretable.",
                "",
                "Per model metric tables include target wise error measures and a single overall mean row that summarizes performance across targets. The comparison table aggregates these overall rows to form a leaderboard. A best model per target table is included to reflect that different targets may respond to thickness with different functional shapes.",
                "",
                "An Excel workbook export consolidates the full set of metric tables into one file for reporting convenience. This is useful for generating manuscript tables, reviewing model tradeoffs, and verifying that model selection is not driven by a single target at the expense of the others.",
                "",
                "All tables are named in a consistent way and avoid parentheses in visible report text. When you cite results, emphasize that the values are in sample diagnostics. Use residual structure plots to validate that an apparently strong metric corresponds to a scientifically plausible response curve rather than to memorization of discrete thickness levels.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    (paths.models_diagnostics_plots / "README.md").write_text(
        "\n".join(
            [
                "# Modeling Diagnostics Plots Index",
                "",
                "This directory contains the full diagnostics set for every model and every target. Plots are organized into a hierarchy by model name and then by target name. This structure makes it easy to audit a single target across models or to audit a single model across all targets without mixing files in one flat folder.",
                "",
                "The core diagnostics include parity plots, residuals versus predicted, residuals versus actual, residuals versus thickness, residual distribution views, and Qq plots. These diagnostics reveal underfitting as structured residual patterns and overfitting as unnatural collapse of the predicted distribution. In one dimensional discrete input settings, these visuals are essential for scientific honesty.",
                "",
                "Because metrics are in sample, a very high \(R^2\) can occur when a model effectively memorizes thickness cohorts. The residuals versus thickness plot is therefore treated as a primary diagnostic. A good model will show residuals that are centered without strong thickness dependent structure, while still producing a smooth and plausible response curve.",
                "",
                "All figures share a consistent PERO visual language. Titles and labels are written in Title Case and avoid parentheses, while mathematical notation uses LaTeX style mathtext for scientifically standard symbols. This directory is intended to be directly usable for report figures without further manual styling edits.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    (paths.explain_root / "README.md").write_text(
        "\n".join(
            [
                "# Explainability Outputs",
                "",
                "This directory explains how thickness influences each target for the selected best overall model. Since the feature space is one dimensional, explainability is fundamentally a study of a response curve rather than attribution across many inputs. The goal is to provide interpretable, export ready visual evidence for whether thickness has a monotonic effect, a threshold effect, or a more complex nonlinear pattern for each electrochemical outcome.",
                "",
                "Permutation importance is reported per target as a drop in \(R^2\) when thickness is randomly permuted. In a single feature setting this becomes a sensitivity diagnostic: if permuting thickness collapses \(R^2\), the model is relying strongly on thickness; if the drop is small, thickness may be weakly informative relative to noise. This table is robust and model agnostic and complements shape based plots.",
                "",
                "Where supported, partial dependence and individual conditional expectation plots are exported. In one dimension, PDP becomes a smoothed estimate of \(\\hat{y}(x)\) while ICE shows how individual observations follow that curve. These plots are paired with a sensitivity curve that overlays the predicted response with a local slope estimate, which is a practical approximation of \(\\frac{d\\hat{y}}{dx}\) for identifying thickness ranges where the response is most sensitive.",
                "",
                "SHAP exports are included when the installed SHAP library supports the selected estimator. In one dimension, SHAP values primarily reflect how the prediction shifts as thickness moves away from the reference distribution. These plots should be interpreted as a consistent explanation of a one dimensional response function rather than as a competition among multiple inputs. All exports are formatted for integration into a research report without additional manual styling work.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    ensure_dir(paths.explain_plots)
    ensure_dir(paths.explain_tables)
    (paths.explain_plots / "README.md").write_text(
        "\n".join(
            [
                "# Explainability Plots Index",
                "",
                "This directory contains plots that explain how thickness influences each target for the selected best overall model. In a one dimensional feature space, explainability focuses on the shape of the learned response function \(\\hat{y}(x)\) and on how predictions change as thickness varies. These plots are designed to support mechanistic discussion, such as monotonic trends, threshold like behavior, or localized sensitivity ranges.",
                "",
                "Partial dependence and individual conditional expectation plots are exported when supported. In one dimension, PDP acts as a smoothed estimate of the mean response curve, while ICE shows individual trajectories around that curve. These plots are valuable for detecting heterogeneity and for spotting cases where the model response is driven by a small number of thickness cohorts.",
                "",
                "A sensitivity curve is included for each target and overlays the predicted response with a local slope diagnostic that approximates \(\\frac{d\\hat{y}}{dx}\). This helps identify thickness regimes where small thickness changes are associated with large predicted changes in the target. Such regimes are scientifically important because they indicate where deposition control would matter most in practice.",
                "",
                "SHAP plots are included when the SHAP library can explain the fitted estimator efficiently. In a one dimensional setting, SHAP values provide a consistent signed explanation of how thickness shifts the prediction relative to a background distribution. These plots are intended as interpretability evidence rather than as proof of causality, and they are formatted for direct inclusion in a research report.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    (paths.explain_tables / "README.md").write_text(
        "\n".join(
            [
                "# Explainability Tables Index",
                "",
                "This directory contains export ready tables that quantify the importance and sensitivity of the thickness feature for each target. In a single feature setting, importance is not a competition among many inputs. Instead, it provides a stability oriented measure of whether the fitted model meaningfully relies on thickness to explain variance in each electrochemical outcome.",
                "",
                "Permutation importance is reported as a drop in \(R^2\) when thickness values are permuted. A large positive drop indicates that thickness is essential for explaining the target in the fitted model, while a small drop suggests that thickness has limited explanatory power in that target. Standard deviation across repeats is also reported to reflect sensitivity to resampling of the permutation process.",
                "",
                "These values should be interpreted together with the response curve plots. A model can show importance even when the response shape is not monotonic, which may indicate nonlinear or threshold like behavior. Conversely, a smooth response curve with low importance may indicate that the variation is small relative to measurement noise at the thickness levels available.",
                "",
                "All tables are designed for reporting and include clear column names and consistent target naming. Mathematical expressions are provided in documentation using LaTeX style mathtext. The goal is a PERO style output that is polished, reproducible, and ready for a thesis appendix without manual cleanup.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    (paths.reports_root / "README.md").write_text(
        "\n".join(
            [
                "# Reports",
                "",
                "This directory contains narrative summaries designed to be copied into a thesis appendix or technical report. The reports emphasize that models are trained on the full dataset by requirement and that all performance values are in sample diagnostics. The writing is intended to connect exported tables and figures to scientific interpretation of thickness response behavior across multiple electrochemical outcomes.",
                "",
                "The main artifact is the summary report in Markdown format, which consolidates thickness concentration, correlation diagnostics, model rankings, and per target best model selection. Tables are rendered directly in Markdown so they can be viewed in any editor and committed into report workflows. The report avoids assuming a second feature or a hidden design variable and treats thickness as the only controllable input in the analysis.",
                "",
                "When interpreting results, the report highlights the discrete nature of thickness and the heavy concentration at zero thickness. This structure can create apparent step changes that are really group differences rather than smooth continuous trends. The report therefore encourages using grouped summaries, uncertainty bands, and residual structure plots to judge whether observed patterns are robust within thickness levels.",
                "",
                "Mathematical notation is expressed using LaTeX style mathtext such as \(R_{\\mathrm{ct}}\) and \(Q_{\\mathrm{rev}}\) when appropriate, while keeping the prose in consistent Title Case headings. The intention is a PERO style deliverable: polished, export ready, reproducible, and organized so that every plot and table has a clear home and a clear purpose.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    # 1) Load + clean
    if not paths.data_xlsx.exists():
        raise FileNotFoundError(f"Expected dataset not found at: {paths.data_xlsx}")

    bundle = prepare_data(str(paths.data_xlsx), colspec=colspec)
    df = bundle.df
    print("Data Loaded And Validated", flush=True)

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
    print("Deep Exploratory Analysis Started", flush=True)
    eda_art = run_deep_eda(
        df=df,
        x_col=bundle.x_col,
        y_cols=list(bundle.y_cols),
        out_plots=paths.eda_plots,
        out_tables=paths.eda_tables,
        cfg=cfg,
    )
    print("Deep Exploratory Analysis Completed", flush=True)

    # 3) Modeling (full-data fit)
    X = bundle.X
    Y = bundle.Y
    model_suite = build_model_suite(random_seed=cfg.random_seed)
    print("Model Fitting And Diagnostics Started", flush=True)

    all_metric_tables = []
    model_names = []
    per_model_metrics_paths = []

    for ms in model_suite:
        try:
            print(f"Fitting Model {ms.name}", flush=True)
            fitted, pred = fit_predict(ms.estimator, X, Y)
        except Exception:
            # Skip models that fail on this environment/dataset
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
    print("Model Fitting And Diagnostics Completed", flush=True)

    if not all_metric_tables:
        raise RuntimeError("No models could be fit successfully. Please ensure scikit-learn is installed correctly.")

    # Model comparison table
    print("Model Comparison And Selection Started", flush=True)
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
    print("Explainability Started", flush=True)
    run_explainability(
        model=fitted_best,
        X=X,
        Y=Y,
        y_cols=list(bundle.y_cols),
        out_plots=paths.explain_plots,
        out_tables=paths.explain_tables,
        cfg=cfg,
    )
    print("Explainability Completed", flush=True)

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
    print("Summary Report Written", flush=True)

    # Print compact progress pointers (console)
    print("DONE.")
    print(f"Outputs root: {paths.outputs_root}")
    print(f"EDA plots: {paths.eda_plots}")
    print(f"Model diagnostics plots: {paths.models_diagnostics_plots}")
    print(f"Explainability plots: {paths.explain_plots}")
    print(f"Summary report: {paths.reports_root / 'summary_report.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

