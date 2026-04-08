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
                "This directory contains a complete exploratory analysis of a single scalar design variable, the aluminum oxide thickness $x$ (nm), mapped to four electrochemical responses. The figures are publication oriented: unified typography, restrained grids, and contrast sufficient for projection or print. The EDA is deliberately deep because $n$ is modest and $x$ is highly discrete, so distributional shape and cohort overlap carry more information than any lone summary statistic.",
                "",
                "The **Plots** folder is organized into univariate, bivariate, grouped, and relationship views. Univariate work characterizes marginal laws of $x$ and of each target: histograms with smooth density overlays, empirical CDFs, and robust box and violin summaries. Bivariate work estimates the conditional mean trend $ \\mathbb{E}[Y \\mid x] $ from scatter, smoothers, and low-order polynomials, with explicit handling of repeated $x$. Grouped views treat each thickness atom as a cohort and visualize means with uncertainty tubes so within-level noise is visible.",
                "",
                "The **Tables** folder contains audit and summary exports suitable for direct appendix insertion: dtypes, missingness, medians, IQRs, thickness concentration, and cohort-wise moments (count, mean, median, standard deviation, extrema) for each target. Pearson and Spearman coefficients between $x$ and each $Y_j$ are **descriptive** in this quasi-factorial one dimensional design; they do not, by themselves, identify nonlinear or threshold mechanistics.",
                "",
                "Symbols follow standard electrochemical usage where helpful: $R_{\\mathrm{ct}}$ (charge-transfer resistance) and $Q_{\\mathrm{rev}}$ (reversible capacity). Every conclusion here is a statement about the thickness response manifold in one dimension, not about latent multivariate structure. Treat this folder as an evidentiary appendix: what the measurements admit, and what they do not.",
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
                "This plots directory is the visual record of a controlled **1D response surface** study: one continuous nominal input (thickness) against four outputs. Figures are high-resolution exports under a single PERO visual system—contrast, type rhythm, and grid discipline held constant. Because many specimens share the same $x$, jitter, cohort strips, and transparency encode overlap rather than hiding it.",
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
                    "On response panels, smooth traces are **estimators** of $ \\hat{y}(x) $, not causal claims. They surface monotonicity, saturation, or threshold phenomenology; polynomial overlays provide an ordered family of curvature tests up to cubic order—often the decisive modeling degree of freedom when $p=1$.",
                    "",
                    "Annotation rules: Title Case labels, no gratuitous parentheses in display text, and Matplotlib mathtext for electrochemical symbols ($R_{\\mathrm{ct}}$, $Q_{\\mathrm{rev}}$). Companion Markdown in this repository uses GitHub `$...$` delimiters so the same expressions render in-browser without a LaTeX engine.",
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
                "Numeric companion to the figure tree: CSV + XLSX tables that tabulate the empirical law of $x$ (thickness) and the joint law of $(x, Y_j)$. Each frame is sized for thesis appendices—dense but legible, with moments that behave well under heavy tails.",
                "",
                "Data audits enumerate dtypes, missingness, cardinalities, medians, and IQRs. Thickness frequency tables quantify the atom at $x=0$ versus sparse nonzero nm levels—the single most important structural fact for every downstream statistic.",
                "",
                "Cohort summaries stratify by each observed $x$: $n$, $\\bar Y_j$, $\\mathrm{median}(Y_j)$, $s$, and extrema. A pooled contrast (`0` nm vs. $\\{x > 0\\}$) formalizes threshold narratives without asserting causality.",
                "",
                "Bivariate summaries list Pearson $\\rho$ and Spearman $r_s$ between $x$ and each $Y_j$. In this quasi-factorial 1D design they are **descriptive** alignment scores, not substitutes for inspecting $\\mathbb{E}[Y_j \\mid x]$ nonlinearity.",
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
                "This directory stores **multi-output regressors** $ \\hat{\\mathbf{y}}(x) \\in \\mathbb{R}^4 $ fitted on the full sample (no routine holdout), per project specification. Consequently every $R^2$, MAE, or RMSE is an **in-sample** adequacy measure—a check of how closely the learned map reproduces the given $ (x, \\mathbf{y}) $ pairs—not a de novo generalization certificate.",
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
                "Because metrics are in-sample, **near-saturated** $R^2$ is compatible with cohort memorization at the discrete $x$ atoms. The residual-vs-$x$ panel is therefore primary: ideally residuals are mean-centered with no systematic thickness trend, while $ \\hat{y}(x) $ remains smooth enough to interpolate scientifically between measured levels.",
                "",
                "All figures share a consistent PERO visual language: Title Case, minimal decorative punctuation, and Matplotlib mathtext for standard electrochemical symbols. Treat this tree as camera-ready without manual restyling.",
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
                "This directory explains how $x$ enters the **selected** best-overall model for each target. With $p=1$, explainability collapses to geometry: the graph of $ \\hat{y}(x) $, its local stability, and perturbation sensitivity—not Shapley-style competition among many inputs.",
                "",
                "Permutation importance is reported as the drop in $R^2$ when $x$ is randomly shuffled within target. Large collapses imply the fit leans hard on thickness ordering; near-zero drops suggest noise dominance or an already flat ridge along $x$. The statistic is model-agnostic and pairs naturally with the curve plots.",
                "",
                "When libraries permit, **PDP** and **ICE** curves are exported. In 1D, the PDP traces a marginal average of $ \\hat{y}(x) $ while ICE ribbons reveal unit-level deviations. A **sensitivity** overlay estimates $ \\frac{\\mathrm{d}\\hat{y}}{\\mathrm{d}x} $ via local differencing—useful for highlighting nm regimes where deposition control would move predictions fastest.",
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
                "These plots dissect the **learned response** $ \\hat{y}(x) $ for the champion model: shape, curvature, cohort stratification, and where local slope is steepest.",
                "",
                "Partial dependence and individual conditional expectation plots are exported when supported. In one dimension, PDP acts as a smoothed estimate of the mean response curve, while ICE shows individual trajectories around that curve. These plots are valuable for detecting heterogeneity and for spotting cases where the model response is driven by a small number of thickness cohorts.",
                "",
                "Each target includes a sensitivity trace approximating $ \\frac{\\mathrm{d}\\hat{y}}{\\mathrm{d}x} $ beside $ \\hat{y}(x) $, flagging nm windows where incremental thickness shifts explode or compress the predicted electrochemical figure of merit.",
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
                "Permutation importance tabulates the positive decrement in $R^2$ when $x$ is permuted; large values mean the in-sample fit is brittle without correct thickness ordering. Bootstrap dispersion across repeats quantifies Monte Carlo noise.",
                "",
                "These values should be interpreted together with the response curve plots. A model can show importance even when the response shape is not monotonic, which may indicate nonlinear or threshold like behavior. Conversely, a smooth response curve with low importance may indicate that the variation is small relative to measurement noise at the thickness levels available.",
                "",
                "Tables ship with explicit column semantics and stable target keys. Companion prose uses GitHub-flavored `$...$` math so coefficients and symbols stay legible on GitHub without a LaTeX toolchain—**PERO** appendix hygiene.",
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
                "Notational hygiene: Markdown uses `$...$` / `$$...$$` for GitHub; figures lean on Matplotlib mathtext ($R_{\\mathrm{ct}}$, $Q_{\\mathrm{rev}}$, etc.). Headings stay Title Case. **PERO** means polished, export-ready, reproducible, organized—each artifact with a named place and a stated inferential role.",
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

