from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class PlotNoteRule:
    """
    Map a plot filename stem to an interpretation blurb.

    Rules are matched against the *stem* (filename without extension).
    """

    pattern: re.Pattern[str]
    title: str
    meaning_md: str


def _default_rules() -> list[PlotNoteRule]:
    # NOTE: Keep math GitHub-friendly: $...$ for inline, $$...$$ for display.
    return [
        # --- EDA ---
        PlotNoteRule(
            re.compile(r"^Histogram And Kernel Density$", re.I),
            "Histogram + KDE (univariate density)",
            "Shows the empirical distribution of a single variable. The histogram approximates the density; the KDE is a smoothed estimate. "
            "Use it to see skew, heavy tails, multi-modality, and whether a few points dominate the range.",
        ),
        PlotNoteRule(
            re.compile(r"^Box And Violin$", re.I),
            "Box/violin summary (univariate spread)",
            "Summarizes median, quartiles, and distribution shape. Use it to compare spread across variables and to detect outliers or strong asymmetry.",
        ),
        PlotNoteRule(
            re.compile(r"^Empirical Cumulative Distribution$", re.I),
            "ECDF (univariate cumulative mass)",
            "Shows $F(t)=\\mathbb{P}(X\\le t)$ directly. Useful for reading quantiles without binning choices and for seeing how quickly mass accumulates near key values.",
        ),
        PlotNoteRule(
            re.compile(r"^Raincloud Plot$", re.I),
            "Raincloud-style view (univariate)",
            "Combines a density impression with a point-level view, making it easier to see sample size and discrete clumping.",
        ),
        PlotNoteRule(
            re.compile(r"^Scaling Comparison Density$", re.I),
            "Scaling comparison (diagnostic density overlay)",
            "Overlays density under multiple rescalings/transforms (when available) to illustrate how scale choices change visual interpretation. "
            "This is a plotting/EDA diagnostic, not a modeling claim.",
        ),
        PlotNoteRule(
            re.compile(r"^Scatter With Trends$", re.I),
            "Scatter with trend overlays (bivariate $x$ vs $Y$)",
            "Plots observed pairs $(x_i, y_i)$ (with optional jitter for repeated $x$), plus smooth/parametric trend overlays and an IQR band by thickness. "
            "Interpret as a *sample description* of $\\mathbb{E}[Y\\mid x]$ shape and within-thickness spread, not as a causal law.",
        ),
        PlotNoteRule(
            re.compile(r"^Sorted Profile$", re.I),
            "Sorted-by-thickness profile (ordered response curve)",
            "Orders rows by thickness and plots a smoothed response profile. Use it to see whether the response is monotone, step-like, or cohort-dominated.",
        ),
        PlotNoteRule(
            re.compile(r"^Residual Pattern$", re.I),
            "EDA residual-pattern probe (shape check)",
            "A diagnostic-style view computed during EDA to highlight curvature or heteroscedasticity patterns versus thickness. "
            "If strong structure is present here, expect simple linear models to leave thickness-structured residuals later.",
        ),
        PlotNoteRule(
            re.compile(r"^Group Mean With Uncertainty$", re.I),
            "Grouped means with uncertainty (cohort geometry)",
            "Shows cohort summaries by discrete thickness levels: typically mean/median with an uncertainty band (e.g. standard error or IQR/quantile ribbon). "
            "This is often the clearest view when $x$ takes only a few repeated values.",
        ),
        PlotNoteRule(
            re.compile(r"^Correlation Heatmap (Pearson|Spearman)$", re.I),
            "Correlation heatmap (association screen)",
            "Displays the association matrix among numeric variables. Pearson captures linear association; Spearman captures monotone rank association. "
            "Use as a screening tool; always validate shape with bivariate plots and residual diagnostics.",
        ),
        PlotNoteRule(
            re.compile(r"^Pair Plot Numeric Variables$", re.I),
            "Pair plot (optional multivariate view)",
            "Shows pairwise scatter/density among numeric columns. With small $n$, treat fine structure as suggestive; look for gross nonlinearity and outliers.",
        ),
        # --- Modeling diagnostics ---
        PlotNoteRule(
            re.compile(r"^Model Comparison Overall Error$", re.I),
            "Leaderboard (overall error comparison)",
            "Ranks models using an overall in-sample error summary (see `outputs/models/tables/README.md` for the exact aggregation). "
            "Use it to shortlist, then validate with residual structure vs thickness.",
        ),
        PlotNoteRule(
            re.compile(r"^Parity Plot__.*$", re.I),
            "Parity plot (calibration: $y$ vs $\\hat y$)",
            "Plots $(y_i, \\hat y_i)$ with the parity line $y=\\hat y$. Systematic curvature away from the diagonal indicates bias; "
            "fan-shapes indicate heteroscedasticity. Parity can look good even when errors are thickness-structured, so also inspect residuals vs thickness.",
        ),
        PlotNoteRule(
            re.compile(r"^Sorted Actual And Predicted__.*$", re.I),
            "Sorted actual vs sorted predicted (distributional alignment)",
            "Compares order statistics of $y$ and $\\hat y$. If curves track closely, predicted and actual distributions align in bulk; "
            "persistent gaps indicate distribution shift (e.g. variance under/over-estimation).",
        ),
        PlotNoteRule(
            re.compile(r"^Residuals Versus Predicted__.*$", re.I),
            "Residuals vs predicted (heteroscedasticity probe)",
            "Plots residuals $\\hat\\varepsilon_i=y_i-\\hat y_i$ against $\\hat y_i$. A random cloud around 0 is desirable. "
            "Funnels or curvature suggest variance changes or missing nonlinear structure.",
        ),
        PlotNoteRule(
            re.compile(r"^Residuals Versus Actual__.*$", re.I),
            "Residuals vs actual (symmetry / model mismatch)",
            "Plots residuals against the true response. Look for systematic trends indicating bias across the response range.",
        ),
        PlotNoteRule(
            re.compile(r"^Residuals Versus Thickness__.*$", re.I),
            "Residuals vs thickness (design-axis stress test)",
            "Plots residuals against thickness $x$. This is the primary diagnostic in a $p=1$ project: any trend with $x$ "
            "means the model has not captured structure tied to the design variable.",
        ),
        PlotNoteRule(
            re.compile(r"^Absolute Error Versus Thickness__.*$", re.I),
            "Absolute error vs thickness (where the model fails)",
            "Plots $|\\hat\\varepsilon|$ against $x$. Use it to see whether certain thickness cohorts are consistently harder to predict.",
        ),
        PlotNoteRule(
            re.compile(r"^Residual Distribution__.*$", re.I),
            "Residual distribution (shape of errors)",
            "Histogram + KDE of residuals. Center near 0 is ideal; skew or heavy tails indicate systematic bias or outlier-driven error.",
        ),
        PlotNoteRule(
            re.compile(r"^Residual Box Plot__.*$", re.I),
            "Residual box plot (robust spread)",
            "Box summary of residuals. Large IQR or extreme whiskers indicate error dispersion; median offset from 0 indicates bias.",
        ),
        PlotNoteRule(
            re.compile(r"^QQ Plot__.*$", re.I),
            "QQ plot (normality screen)",
            "Compares residual quantiles to a normal reference. With $n=51$, treat as a gentle screen: large tail deviations suggest heavy-tailed errors.",
        ),
        PlotNoteRule(
            re.compile(r"^Predicted And Actual Density__.*$", re.I),
            "Predicted vs actual density (distribution match)",
            "Overlaid densities of $y$ and $\\hat y$. Systematic shifts indicate bias; width mismatch indicates under/over-estimated variance.",
        ),
        # --- Explainability ---
        PlotNoteRule(
            re.compile(r"^Partial Dependence And ICE__.*$", re.I),
            "PDP + ICE (model response curve)",
            "Shows the fitted response curve $\\hat y_j(x)$ along a dense thickness grid (PDP) with bootstrap/ICE variability. "
            "Large bands indicate instability under resampling (important at small $n$).",
        ),
        PlotNoteRule(
            re.compile(r"^Sensitivity Curve__.*$", re.I),
            "Sensitivity curve ($\\hat y$ and $d\\hat y/dx$)",
            "Upper panel: response curve $\\hat y_j(x)$. Lower panel: numerical slope $d\\hat y_j/dx$. "
            "Spikes often occur where support is sparse; interpret alongside thickness counts.",
        ),
        PlotNoteRule(
            re.compile(r"^shap_beeswarm__.*$", re.I),
            "SHAP beeswarm (1D attribution cloud)",
            "In 1D, SHAP values $\\phi(x)$ largely re-express deviations from the baseline prediction. "
            "Use it as a consistency view: does attribution vary smoothly with thickness, or is it cohort-stepped?",
        ),
        PlotNoteRule(
            re.compile(r"^shap_dependence__.*$", re.I),
            "SHAP dependence (attribution vs thickness)",
            "Plots SHAP value $\\phi(x)$ against thickness. In a single-feature project, this often mirrors the fitted response shape "
            "and can highlight thickness regions where the model’s contribution changes fastest.",
        ),
        PlotNoteRule(
            re.compile(r"^shap_bar__.*$", re.I),
            "SHAP bar (mean absolute attribution)",
            "Reports $\\mathbb{E}[|\\phi|]$ for the single feature. With $p=1$, it is a magnitude summary, not a ranking among many features.",
        ),
    ]


def _describe_stem(stem: str, rules: list[PlotNoteRule]) -> tuple[str, str]:
    for rule in rules:
        if rule.pattern.match(stem):
            return rule.title, rule.meaning_md
    # Fallback: still provide something useful.
    return "Plot interpretation", (
        "This plot was generated by the pipeline, but its filename does not match a known stem pattern in the plot-notes writer. "
        "Interpret it by locating the producing module under `src/` and cross-referencing the nearest `README.md` index in this directory."
    )


def write_plot_notes(outputs_root: Path) -> list[Path]:
    """
    Write one `PLOT_NOTES.md` per directory that contains PNG figures.

    This keeps interpretation close to the artifacts without exploding into one .md per figure.
    """
    rules = _default_rules()
    written: list[Path] = []

    for d in sorted([p for p in outputs_root.rglob("*") if p.is_dir()]):
        pngs = sorted([p for p in d.glob("*.png") if p.is_file()])
        if not pngs:
            continue

        lines: list[str] = []
        rel_dir = d.relative_to(outputs_root)
        lines.append(f"# Plot Notes — `{rel_dir.as_posix()}`")
        lines.append("")
        lines.append(
            "This file is auto-written by the pipeline to describe what each figure in this folder is intended to communicate. "
            "All statements are *interpretive guides* to the plotted objects (curves, residuals, densities), not guarantees of causal mechanism."
        )
        lines.append("")
        lines.append("## Notation")
        lines.append("")
        lines.append("- Thickness: $x$ (nm)")
        lines.append("- Target: $Y_j$")
        lines.append("- Prediction: $\\hat y_j(x)$")
        lines.append("- Residual: $\\hat\\varepsilon_i = y_i-\\hat y_i$")
        lines.append("")

        lines.append("## Figures in this folder")
        lines.append("")

        for p in pngs:
            stem = p.stem
            title, meaning = _describe_stem(stem, rules)
            lines.append(f"### `{p.name}`")
            lines.append("")
            lines.append(f"**Type**: {title}")
            lines.append("")
            lines.append(f"**What it is saying**: {meaning}")
            lines.append("")

        out_path = d / "PLOT_NOTES.md"
        out_path.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")
        written.append(out_path)

    return written

