from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from .plots import savefig, with_axes
from .utils import ensure_dir, safe_filename, smooth_curve_1d, strip_parentheses_text, to_title_case
from .viz_style import get_display_labels, legend_outside_top_right, polish_axes, set_dark_background


def qqplot_residuals(ax, residuals: np.ndarray, title: str):
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
            ax.scatter(osm, osr, s=30, alpha=0.8)
            x = np.asarray(osm)
            yref = slope * x + intercept
            yref_s = smooth_curve_1d(yref) if yref.size >= 5 else yref
            ax.fill_between(x, yref_s - 0.02 * np.nanstd(osr), yref_s + 0.02 * np.nanstd(osr), color="#D7263D", alpha=0.12, label="Reference Band")
            ax.plot(x, yref_s, color="#D7263D", linewidth=2.4, label="Smoothed Reference")
            ax.set_title(title)
            ax.set_xlabel("Theoretical Quantiles")
            ax.set_ylabel("Ordered Residuals")
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
    fig, ax = with_axes(figsize=(7, 7))
    set_dark_background(fig, ax)
    ax.scatter(y_true, y_pred, s=62, alpha=0.86, edgecolor="#0B0F1A", linewidth=0.8, color="#5BC0EB")
    lims = [float(min(y_true.min(), y_pred.min())), float(max(y_true.max(), y_pred.max()))]
    xs_p = np.linspace(lims[0], lims[1], 200)
    ax.plot(xs_p, xs_p, linestyle="--", linewidth=2.2, color="#EAF0FF", alpha=0.9, label="Parity Reference")
    band = float(np.nanstd(resid, ddof=1)) if np.isfinite(np.nanstd(resid, ddof=1)) else 0.0
    if band > 0:
        ax.fill_between(xs_p, xs_p - band, xs_p + band, color="#EAF0FF", alpha=0.08, label="Parity Band")
        ax.plot(xs_p, xs_p - band, color="#EAF0FF", linewidth=1.0, linestyle=":", alpha=0.55, label="Parity Lower Boundary")
        ax.plot(xs_p, xs_p + band, color="#EAF0FF", linewidth=1.0, linestyle=":", alpha=0.55, label="Parity Upper Boundary")
    ax.set_xlim(lims)
    ax.set_ylim(lims)
    ax.set_title(f"{target_title} Parity Plot")
    ax.set_xlabel("Actual")
    ax.set_ylabel("Predicted")
    legend_outside_top_right(ax, ncol=1)
    polish_axes(ax)
    saved.append(savefig(fig, calib_dir, f"Parity Plot__{base}", dpi=cfg.figure_dpi, fmt=cfg.figure_format))

    # Residuals vs predicted
    fig, ax = with_axes(figsize=(9, 6))
    ax.scatter(y_pred, resid, s=58, alpha=0.82, edgecolor="#0B0F1A", linewidth=0.7, color="#FF9F1C")
    ax.axhline(0, color="#EAF0FF", linewidth=1.2, alpha=0.85)
    ax.set_title(f"{target_title} Residuals Versus Predicted")
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Residual")
    polish_axes(ax)
    saved.append(savefig(fig, resid_dir, f"Residuals Versus Predicted__{base}", dpi=cfg.figure_dpi, fmt=cfg.figure_format))

    # Residuals vs actual
    fig, ax = with_axes(figsize=(9, 6))
    ax.scatter(y_true, resid, s=58, alpha=0.82, edgecolor="#0B0F1A", linewidth=0.7, color="#FF9F1C")
    ax.axhline(0, color="#EAF0FF", linewidth=1.2, alpha=0.85)
    ax.set_title(f"{target_title} Residuals Versus Actual")
    ax.set_xlabel("Actual")
    ax.set_ylabel("Residual")
    polish_axes(ax)
    saved.append(savefig(fig, resid_dir, f"Residuals Versus Actual__{base}", dpi=cfg.figure_dpi, fmt=cfg.figure_format))

    # Residuals vs thickness (detect structure)
    fig, ax = with_axes(figsize=(9, 6))
    ax.scatter(x, resid, s=58, alpha=0.82, edgecolor="#0B0F1A", linewidth=0.7, color="#FF9F1C")
    ax.axhline(0, color="#EAF0FF", linewidth=1.2, alpha=0.85)
    ax.set_title(f"{target_title} Residuals Versus Thickness")
    ax.set_xlabel(labels.x_label)
    ax.set_ylabel("Residual")
    polish_axes(ax)
    saved.append(savefig(fig, resid_dir, f"Residuals Versus Thickness__{base}", dpi=cfg.figure_dpi, fmt=cfg.figure_format))

    # Residual distribution hist + KDE
    fig, ax = with_axes(figsize=(9, 6))
    sns.histplot(resid, kde=True, ax=ax, color="#5BC0EB", edgecolor="#0B0F1A", alpha=0.92)
    ax.set_title(f"{target_title} Residual Distribution")
    ax.set_xlabel("Residual")
    ax.set_ylabel("Density")
    polish_axes(ax)
    saved.append(savefig(fig, dist_dir, f"Residual Distribution__{base}", dpi=cfg.figure_dpi, fmt=cfg.figure_format))

    # Residual box
    fig, ax = with_axes(figsize=(7, 4))
    sns.boxplot(x=resid, ax=ax, color="#9FD356")
    ax.set_title(f"{target_title} Residual Box Plot")
    ax.set_xlabel("Residual")
    polish_axes(ax)
    saved.append(savefig(fig, dist_dir, f"Residual Box Plot__{base}", dpi=cfg.figure_dpi, fmt=cfg.figure_format))

    # QQ plot
    fig, ax = with_axes(figsize=(7, 7))
    qqplot_residuals(ax, resid, title=f"{target_title} QQ Plot")
    polish_axes(ax)
    saved.append(savefig(fig, dist_dir, f"QQ Plot__{base}", dpi=cfg.figure_dpi, fmt=cfg.figure_format))

    # Error magnitude vs thickness
    fig, ax = with_axes(figsize=(9, 6))
    ax.scatter(x, abs_err, s=58, alpha=0.86, edgecolor="#0B0F1A", linewidth=0.7, color="#D7263D")
    ax.set_title(f"{target_title} Absolute Error Versus Thickness")
    ax.set_xlabel(labels.x_label)
    ax.set_ylabel("Absolute Error")
    polish_axes(ax)
    saved.append(savefig(fig, resid_dir, f"Absolute Error Versus Thickness__{base}", dpi=cfg.figure_dpi, fmt=cfg.figure_format))

    # Sorted actual vs sorted predicted (distributional calibration)
    fig, ax = with_axes(figsize=(10, 6))
    set_dark_background(fig, ax)
    n_s = y_true.size
    idx = np.arange(n_s, dtype=float)
    ya = np.sort(y_true)
    yp = np.sort(y_pred)
    ya_s = smooth_curve_1d(ya)
    yp_s = smooth_curve_1d(yp)
    lo = np.minimum(ya_s, yp_s)
    hi = np.maximum(ya_s, yp_s)
    ax.fill_between(idx, lo, hi, color="#EAF0FF", alpha=0.10, label="Between Curves Area")
    ax.plot(idx, ya_s, label="Sorted Actual", linewidth=2.8, color="#9FD356")
    ax.plot(idx, yp_s, label="Sorted Predicted", linewidth=2.8, color="#5BC0EB")
    ax.set_title(f"{target_title} Sorted Actual And Predicted")
    ax.set_xlabel("Sorted Index")
    ax.set_ylabel(y_label)
    legend_outside_top_right(ax, ncol=1)
    polish_axes(ax)
    saved.append(savefig(fig, calib_dir, f"Sorted Actual And Predicted__{base}", dpi=cfg.figure_dpi, fmt=cfg.figure_format))

    # Predicted distribution vs actual distribution
    fig, ax = with_axes(figsize=(10, 6))
    sns.kdeplot(y_true, ax=ax, linewidth=2.2, label="Actual")
    sns.kdeplot(y_pred, ax=ax, linewidth=2.2, label="Predicted")
    ax.set_title(f"{target_title} Predicted And Actual Density")
    ax.set_xlabel(y_label)
    ax.legend(loc="best")
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
    fig, ax = with_axes(figsize=(12, 7))
    ax.barh(top["model"][::-1], top["OVERALL_RMSE"][::-1], color="#2E86AB")
    ax.set_title("Model Comparison Overall Error")
    ax.set_xlabel("Overall Root Mean Squared Error")
    polish_axes(ax)
    out = savefig(fig, out_dir, "Model Comparison Overall Error", dpi=cfg.figure_dpi, fmt=cfg.figure_format)
    return out

