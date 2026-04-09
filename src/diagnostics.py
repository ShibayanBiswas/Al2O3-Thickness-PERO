from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

from .plots import savefig, scatter_with_marginals, with_axes
from .utils import ensure_dir, safe_filename, smooth_curve_1d, strip_parentheses_text, to_title_case
from .viz_style import PERO, get_display_labels, legend_outside_top_right, polish_axes, set_dark_background


def qqplot_residuals(ax, residuals: np.ndarray, title: str) -> None:
    sm = None
    try:
        import statsmodels.api as sm  # type: ignore
    except Exception:
        sm = None

    if sm is None:
        # Fallback: simple quantile-quantile against normal via scipy
        try:
            from scipy import stats

            r = residuals[np.isfinite(residuals)]
            if r.size < 3:
                ax.text(0.5, 0.5, "Qq Plot Unavailable", ha="center", va="center")
                ax.set_title(title)
                return
            (osm, osr), (slope, intercept, r_) = stats.probplot(r, dist="norm")
            ax.scatter(osm, osr, s=30, alpha=0.8, label="Empirical quantiles")
            x = np.asarray(osm)
            yref = slope * x + intercept
            yref_s = smooth_curve_1d(yref) if yref.size >= 5 else yref
            ax.fill_between(x, yref_s - 0.02 * np.nanstd(osr), yref_s + 0.02 * np.nanstd(osr), color=PERO.qq_ref, alpha=0.12, label="Reference Band")
            ax.plot(x, yref_s, color=PERO.qq_ref, linewidth=2.4, label="Smoothed Reference")
            ax.set_title(title)
            ax.set_xlabel("Theoretical Quantiles")
            ax.set_ylabel("Ordered Residuals")
            legend_outside_top_right(ax, title="Normal QQ")
            return
        except Exception:
            ax.text(0.5, 0.5, "Qq Plot Unavailable", ha="center", va="center")
            ax.set_title(title)
            return

    r = residuals[np.isfinite(residuals)]
    if r.size < 3:
        ax.text(0.5, 0.5, "Qq Plot Unavailable", ha="center", va="center")
        ax.set_title(title)
        return
    sm.qqplot(r, line="45", ax=ax)
    ax.set_title(title)
    ax.set_xlabel("Theoretical quantiles")
    ax.set_ylabel("Ordered residuals")
    legend_outside_top_right(
        ax,
        handles=[
            Line2D(
                [0],
                [0],
                marker="o",
                color="w",
                markerfacecolor=PERO.sky,
                markeredgecolor=PERO.ink,
                markersize=7,
                linestyle="",
                label="Empirical quantiles",
            ),
            Line2D([0], [0], color=PERO.text, linestyle="--", linewidth=2.2, label="Theoretical normal reference"),
        ],
        title="QQ diagnostic",
    )


def diagnostic_plots_per_target(
    model_name: str,
    x: np.ndarray,
    y_true: np.ndarray,
    y_pred: np.ndarray,
    target_name: str,
    out_dir: Path,
    cfg: object,
) -> list[Path]:
    import seaborn as sns

    # One more folder depth for compact organization
    calib_dir = ensure_dir(out_dir / "Calibration")
    resid_dir = ensure_dir(out_dir / "Residuals")
    dist_dir = ensure_dir(out_dir / "Distributions")
    x = np.asarray(x, dtype=float).ravel()
    y_true = np.asarray(y_true, dtype=float).ravel()
    y_pred = np.asarray(y_pred, dtype=float).ravel()
    resid = y_true - y_pred
    abs_err = np.abs(resid)

    saved: list[Path] = []
    # Do not place model name inside plot text (user requested no punctuation clutter).
    base = f"{safe_filename(model_name)}__{safe_filename(target_name)}"

    labels = get_display_labels(x_col="Al2O3 Thickness_nm", y_cols=[target_name])
    target_title = labels.target_title_map.get(target_name, to_title_case(strip_parentheses_text(target_name)))
    y_label = labels.y_label_map.get(target_name, to_title_case(strip_parentheses_text(target_name)))

    # Actual vs Predicted (parity)
    fig, ax = with_axes(figsize=(7.5, 7.5))
    set_dark_background(fig, ax)
    ax.scatter(y_true, y_pred, s=64, alpha=0.88, edgecolor=PERO.ink, linewidth=0.75, color=PERO.sky, label="In-sample pairs")
    lims = [float(min(y_true.min(), y_pred.min())), float(max(y_true.max(), y_pred.max()))]
    xs_p = np.linspace(lims[0], lims[1], 200)
    ax.plot(xs_p, xs_p, linestyle="--", linewidth=2.2, color=PERO.text, alpha=0.9, label="Parity Reference")
    band = float(np.nanstd(resid, ddof=1)) if np.isfinite(np.nanstd(resid, ddof=1)) else 0.0
    if band > 0:
        ax.fill_between(xs_p, xs_p - band, xs_p + band, color=PERO.text, alpha=0.08, label="Parity Band")
        ax.plot(xs_p, xs_p - band, color=PERO.text, linewidth=1.0, linestyle=":", alpha=0.55, label="Parity Lower Boundary")
        ax.plot(xs_p, xs_p + band, color=PERO.text, linewidth=1.0, linestyle=":", alpha=0.55, label="Parity Upper Boundary")
    ax.set_xlim(lims)
    ax.set_ylim(lims)
    ax.set_title(f"{target_title} Parity Plot")
    ax.set_xlabel("Actual")
    ax.set_ylabel("Predicted")
    legend_outside_top_right(ax, ncol=1)
    polish_axes(ax)
    saved.append(savefig(fig, calib_dir, f"Parity Plot__{base}", dpi=cfg.figure_dpi, fmt=cfg.figure_format))

    # Residuals vs predicted
    fig, ax = with_axes(figsize=(7.5, 7.5))
    set_dark_background(fig, ax)
    ax.scatter(y_pred, resid, s=58, alpha=0.84, edgecolor=PERO.ink, linewidth=0.65, color=PERO.orange, label=r"Residuals $\hat\varepsilon$")
    ax.axhline(0, color=PERO.text, linewidth=1.15, alpha=0.88)
    ax.set_title(f"{target_title} Residuals Versus Predicted")
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Residual")
    legend_outside_top_right(ax, title="Diagnostics")
    polish_axes(ax)
    saved.append(savefig(fig, resid_dir, f"Residuals Versus Predicted__{base}", dpi=cfg.figure_dpi, fmt=cfg.figure_format))

    # Residuals vs actual
    fig, ax = with_axes(figsize=(7.5, 7.5))
    set_dark_background(fig, ax)
    ax.scatter(y_true, resid, s=58, alpha=0.84, edgecolor=PERO.ink, linewidth=0.65, color=PERO.orange, label=r"Residuals $\hat\varepsilon$")
    ax.axhline(0, color=PERO.text, linewidth=1.15, alpha=0.88)
    ax.set_title(f"{target_title} Residuals Versus Actual")
    ax.set_xlabel("Actual")
    ax.set_ylabel("Residual")
    legend_outside_top_right(ax, title="Diagnostics")
    polish_axes(ax)
    saved.append(savefig(fig, resid_dir, f"Residuals Versus Actual__{base}", dpi=cfg.figure_dpi, fmt=cfg.figure_format))

    # Residuals vs thickness (detect structure)
    fig, ax = with_axes(figsize=(7.5, 7.5))
    set_dark_background(fig, ax)
    ax.scatter(x, resid, s=58, alpha=0.84, edgecolor=PERO.ink, linewidth=0.65, color=PERO.orange, label=r"Residuals $\hat\varepsilon$")
    ax.axhline(0, color=PERO.text, linewidth=1.15, alpha=0.88)
    ax.set_title(f"{target_title} Residuals Versus Thickness")
    ax.set_xlabel(labels.x_label)
    ax.set_ylabel("Residual")
    legend_outside_top_right(ax, title="Diagnostics")
    polish_axes(ax)
    saved.append(savefig(fig, resid_dir, f"Residuals Versus Thickness__{base}", dpi=cfg.figure_dpi, fmt=cfg.figure_format))

    # Residual distribution hist + KDE
    fig, ax = with_axes(figsize=(7.5, 7.5))
    set_dark_background(fig, ax)
    sns.histplot(resid, stat="density", kde=False, ax=ax, color=PERO.sky, edgecolor=PERO.ink, alpha=0.88, label="Histogram")
    sns.kdeplot(resid, ax=ax, color=PERO.orange, linewidth=2.45, warn_singular=False, label="Kernel density")
    ax.set_title(f"{target_title} Residual Distribution")
    ax.set_xlabel(r"Residual $\hat\varepsilon$")
    ax.set_ylabel("Density")
    legend_outside_top_right(ax, title="Density")
    polish_axes(ax)
    saved.append(savefig(fig, dist_dir, f"Residual Distribution__{base}", dpi=cfg.figure_dpi, fmt=cfg.figure_format))

    # Residual box
    fig, ax = with_axes(figsize=(7.5, 7.5))
    set_dark_background(fig, ax)
    sns.boxplot(x=resid, ax=ax, color=PERO.green)
    ax.set_title(f"{target_title} Residual Box Plot")
    ax.set_xlabel(r"Residual $\hat\varepsilon$")
    legend_outside_top_right(
        ax,
        handles=[Patch(facecolor=PERO.green, edgecolor=PERO.ink, linewidth=0.9, label="Box summary")],
        title="Spread",
    )
    polish_axes(ax)
    saved.append(savefig(fig, dist_dir, f"Residual Box Plot__{base}", dpi=cfg.figure_dpi, fmt=cfg.figure_format))

    # QQ plot
    fig, ax = with_axes(figsize=(7.5, 7.5))
    set_dark_background(fig, ax)
    qqplot_residuals(ax, resid, title=f"{target_title} QQ Plot")
    polish_axes(ax)
    saved.append(savefig(fig, dist_dir, f"QQ Plot__{base}", dpi=cfg.figure_dpi, fmt=cfg.figure_format))

    # Error magnitude vs thickness
    fig, ax = with_axes(figsize=(7.5, 7.5))
    set_dark_background(fig, ax)
    ax.scatter(x, abs_err, s=58, alpha=0.88, edgecolor=PERO.ink, linewidth=0.65, color=PERO.red, label=r"$|\hat\varepsilon|$")
    ax.set_title(f"{target_title} Absolute Error Versus Thickness")
    ax.set_xlabel(labels.x_label)
    ax.set_ylabel(r"Absolute error $|\hat\varepsilon|$")
    legend_outside_top_right(ax, title="Magnitude")
    polish_axes(ax)
    saved.append(savefig(fig, resid_dir, f"Absolute Error Versus Thickness__{base}", dpi=cfg.figure_dpi, fmt=cfg.figure_format))

    # Sorted actual vs sorted predicted (distributional calibration)
    fig, ax = with_axes(figsize=(7.5, 7.5))
    set_dark_background(fig, ax)
    n_s = y_true.size
    idx = np.arange(n_s, dtype=float)
    ya = np.sort(y_true)
    yp = np.sort(y_pred)
    ya_s = smooth_curve_1d(ya)
    yp_s = smooth_curve_1d(yp)
    lo = np.minimum(ya_s, yp_s)
    hi = np.maximum(ya_s, yp_s)
    ax.fill_between(idx, lo, hi, color=PERO.text, alpha=0.10, label="Between Curves Area")
    ax.plot(idx, ya_s, label="Sorted Actual", linewidth=2.05, color=PERO.green)
    ax.plot(idx, yp_s, label="Sorted Predicted", linewidth=2.05, color=PERO.sky)
    ax.set_title(f"{target_title} Sorted Actual And Predicted")
    ax.set_xlabel("Sorted Index")
    ax.set_ylabel(y_label)
    legend_outside_top_right(ax, ncol=1)
    polish_axes(ax)
    saved.append(savefig(fig, calib_dir, f"Sorted Actual And Predicted__{base}", dpi=cfg.figure_dpi, fmt=cfg.figure_format))

    # Predicted distribution vs actual distribution
    fig, ax = with_axes(figsize=(7.5, 7.5))
    set_dark_background(fig, ax)
    try:
        sns.kdeplot(y_true, ax=ax, linewidth=2.2, label="Actual", warn_singular=False)
        sns.kdeplot(y_pred, ax=ax, linewidth=2.2, label="Predicted", warn_singular=False)
    except Exception:
        ax.hist(y_true, bins=min(20, max(5, y_true.size // 2)), alpha=0.45, label="Actual", color=PERO.sky)
        ax.hist(y_pred, bins=min(20, max(5, y_pred.size // 2)), alpha=0.45, label="Predicted", color=PERO.orange)
    ax.set_title(f"{target_title} Predicted And Actual Density")
    ax.set_xlabel(y_label)
    legend_outside_top_right(ax, ncol=1)
    polish_axes(ax)
    saved.append(savefig(fig, dist_dir, f"Predicted And Actual Density__{base}", dpi=cfg.figure_dpi, fmt=cfg.figure_format))

    return saved


def consolidated_model_comparison_plot(
    comp_table: pd.DataFrame,
    out_dir: Path,
    cfg: object,
) -> Path:
    import matplotlib.pyplot as plt

    ensure_dir(out_dir)
    top = comp_table.head(min(12, comp_table.shape[0])).copy()
    fig, ax = with_axes(figsize=(7.5, 7.5))
    set_dark_background(fig, ax)
    ax.barh(top["model"][::-1], top["OVERALL_RMSE"][::-1], color=PERO.bar, edgecolor=PERO.ink, linewidth=0.55)
    ax.set_title(r"Model comparison: mean $\mathrm{RMSE}$ across targets")
    ax.set_xlabel(r"Overall $\mathrm{RMSE}$")
    legend_outside_top_right(
        ax,
        handles=[Patch(facecolor=PERO.bar, edgecolor=PERO.ink, linewidth=0.8, label=r"Lower is better $\rightarrow$")],
        title="Leaderboard",
    )
    polish_axes(ax)
    out = savefig(fig, out_dir, "Model Comparison Overall Error", dpi=cfg.figure_dpi, fmt=cfg.figure_format)
    return out

