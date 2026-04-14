from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

from .plots import save_plot_csv, savefig, with_axes
from .utils import ensure_dir, safe_filename, smooth_curve_1d, strip_parentheses_text, to_title_case
from .viz_style import PERO, get_display_labels, legend_outside_top_right, polish_axes, set_dark_background


def qqplot_residuals(ax, residuals: np.ndarray, title: str) -> None:
    # We implement QQ directly so we can add a proper quantile-confidence "area strip".
    # Band construction: p_i ~ Beta(i, n+1-i) (order-statistic CIs), mapped through N(0,1).
    try:
        from scipy import stats
    except Exception:
        stats = None

    r = residuals[np.isfinite(residuals)]
    if r.size < 3 or stats is None:
        ax.text(0.5, 0.5, "QQ Plot Unavailable", ha="center", va="center")
        ax.set_title(title)
        return

    r = np.sort(np.asarray(r, dtype=float))
    n = int(r.size)
    i = np.arange(1, n + 1, dtype=float)
    p = (i - 0.5) / n
    osm = stats.norm.ppf(p)
    osr = r

    # Fit the reference line (least squares) in QQ space.
    slope, intercept = np.polyfit(osm, osr, deg=1)
    yref = slope * osm + intercept

    # Quantile band ("area strip") via Beta order-statistic confidence limits.
    alpha = 0.10  # 90% pointwise envelope; stable at n≈50 without being overly wide.
    p_lo = stats.beta.ppf(alpha / 2, i, n + 1 - i)
    p_hi = stats.beta.ppf(1 - alpha / 2, i, n + 1 - i)
    x_lo = stats.norm.ppf(p_lo)
    x_hi = stats.norm.ppf(p_hi)
    y_lo = slope * x_lo + intercept
    y_hi = slope * x_hi + intercept

    ax.fill_between(osm, y_lo, y_hi, color=PERO.qq_ref, alpha=0.14, label="Quantile Band (90%)")
    ax.plot(osm, yref, color=PERO.qq_ref, linewidth=1.5, label="Normal Reference")
    ax.scatter(osm, osr, s=30, alpha=0.82, color=PERO.sky, edgecolor=PERO.ink, linewidth=0.6, label="Empirical quantiles")

    ax.set_title(title)
    ax.set_xlabel("Theoretical quantiles")
    ax.set_ylabel("Ordered residuals")
    legend_outside_top_right(ax, title="QQ diagnostic")


def _qq_plot_csv_rows(residuals: np.ndarray) -> list[dict]:
    """Same geometry as ``qqplot_residuals`` for tidy CSV export."""
    try:
        from scipy import stats
    except Exception:
        return []
    r = residuals[np.isfinite(residuals)]
    if r.size < 3:
        return []
    r = np.sort(np.asarray(r, dtype=float))
    n = int(r.size)
    i = np.arange(1, n + 1, dtype=float)
    p = (i - 0.5) / n
    osm = stats.norm.ppf(p)
    osr = r
    slope, intercept = np.polyfit(osm, osr, deg=1)
    yref = slope * osm + intercept
    alpha = 0.10
    p_lo = stats.beta.ppf(alpha / 2, i, n + 1 - i)
    p_hi = stats.beta.ppf(1 - alpha / 2, i, n + 1 - i)
    x_lo = stats.norm.ppf(p_lo)
    x_hi = stats.norm.ppf(p_hi)
    y_lo = slope * x_lo + intercept
    y_hi = slope * x_hi + intercept
    rows: list[dict] = []
    for k in range(n):
        rows.append(
            {
                "series": "empirical_quantile",
                "rank": k + 1,
                "theoretical_quantile": float(osm[k]),
                "ordered_residual": float(osr[k]),
            }
        )
    for k in range(n):
        rows.append({"series": "normal_reference", "rank": k + 1, "x": float(osm[k]), "y": float(yref[k])})
    for k in range(n):
        rows.append({"series": "quantile_band_lower", "rank": k + 1, "x": float(osm[k]), "y": float(y_lo[k])})
        rows.append({"series": "quantile_band_upper", "rank": k + 1, "x": float(osm[k]), "y": float(y_hi[k])})
    return rows


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
    ax.plot(xs_p, xs_p, linestyle="--", linewidth=1.5, color=PERO.text, alpha=0.9, label="Parity Reference")
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
    _parity_rows: list[dict] = [
        {"series": "point", "actual": float(a), "predicted": float(p)} for a, p in zip(y_true, y_pred, strict=False)
    ]
    for xp in xs_p:
        _parity_rows.append({"series": "parity_reference", "actual": float(xp), "predicted": float(xp)})
    if band > 0:
        for xp in xs_p:
            _parity_rows.append({"series": "parity_band_upper", "actual": float(xp), "predicted": float(xp + band)})
            _parity_rows.append({"series": "parity_band_lower", "actual": float(xp), "predicted": float(xp - band)})
    save_plot_csv(calib_dir, f"Parity Plot__{base}", _parity_rows)

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
    save_plot_csv(
        resid_dir,
        f"Residuals Versus Predicted__{base}",
        [{"series": "point", "predicted": float(p), "residual": float(r)} for p, r in zip(y_pred, resid, strict=False)],
    )

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
    save_plot_csv(
        resid_dir,
        f"Residuals Versus Actual__{base}",
        [{"series": "point", "actual": float(a), "residual": float(r)} for a, r in zip(y_true, resid, strict=False)],
    )

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
    save_plot_csv(
        resid_dir,
        f"Residuals Versus Thickness__{base}",
        [{"series": "point", "thickness_nm": float(xi), "residual": float(r)} for xi, r in zip(x, resid, strict=False)],
    )

    # Residual distribution hist + KDE
    fig, ax = with_axes(figsize=(7.5, 7.5))
    set_dark_background(fig, ax)
    sns.histplot(resid, stat="density", kde=False, ax=ax, color=PERO.sky, edgecolor=PERO.ink, alpha=0.88, label="Histogram")
    sns.kdeplot(resid, ax=ax, color=PERO.orange, linewidth=1.4, warn_singular=False, label="Kernel density")
    ax.set_title(f"{target_title} Residual Distribution")
    ax.set_xlabel(r"Residual $\hat\varepsilon$")
    ax.set_ylabel("Density")
    legend_outside_top_right(ax, title="Density")
    polish_axes(ax)
    saved.append(savefig(fig, dist_dir, f"Residual Distribution__{base}", dpi=cfg.figure_dpi, fmt=cfg.figure_format))
    _rd_rows = [{"series": "residual_sample", "residual": float(r)} for r in resid if np.isfinite(r)]
    try:
        from scipy.stats import gaussian_kde

        rr = resid[np.isfinite(resid)]
        if rr.size >= 2 and np.nanstd(rr, ddof=1) > 0:
            kde = gaussian_kde(rr)
            g = np.linspace(float(np.min(rr)), float(np.max(rr)), 200)
            for xi, di in zip(g, kde(g), strict=False):
                _rd_rows.append({"series": "kde", "kde_x": float(xi), "kde_density": float(di)})
    except Exception:
        pass
    save_plot_csv(dist_dir, f"Residual Distribution__{base}", _rd_rows)

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
    save_plot_csv(
        dist_dir,
        f"Residual Box Plot__{base}",
        [{"series": "residual_sample", "residual": float(r)} for r in resid if np.isfinite(r)],
    )

    # QQ plot
    fig, ax = with_axes(figsize=(7.5, 7.5))
    set_dark_background(fig, ax)
    qqplot_residuals(ax, resid, title=f"{target_title} QQ Plot")
    polish_axes(ax)
    saved.append(savefig(fig, dist_dir, f"QQ Plot__{base}", dpi=cfg.figure_dpi, fmt=cfg.figure_format))
    save_plot_csv(dist_dir, f"QQ Plot__{base}", _qq_plot_csv_rows(resid))

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
    save_plot_csv(
        resid_dir,
        f"Absolute Error Versus Thickness__{base}",
        [{"series": "point", "thickness_nm": float(xi), "absolute_error": float(e)} for xi, e in zip(x, abs_err, strict=False)],
    )

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
    ax.plot(idx, ya_s, label="Sorted Actual", linewidth=1.55, color=PERO.green)
    ax.plot(idx, yp_s, label="Sorted Predicted", linewidth=1.55, color=PERO.sky)
    ax.set_title(f"{target_title} Sorted Actual And Predicted")
    ax.set_xlabel("Sorted Index")
    ax.set_ylabel(y_label)
    legend_outside_top_right(ax, ncol=1)
    polish_axes(ax)
    saved.append(savefig(fig, calib_dir, f"Sorted Actual And Predicted__{base}", dpi=cfg.figure_dpi, fmt=cfg.figure_format))
    _sap_rows: list[dict] = []
    for k in range(n_s):
        _sap_rows.append(
            {
                "series": "sorted_curves",
                "sorted_index": float(idx[k]),
                "sorted_actual": float(ya[k]),
                "sorted_predicted": float(yp[k]),
                "smoothed_actual": float(ya_s[k]),
                "smoothed_predicted": float(yp_s[k]),
                "between_curves_lo": float(lo[k]),
                "between_curves_hi": float(hi[k]),
            }
        )
    save_plot_csv(calib_dir, f"Sorted Actual And Predicted__{base}", _sap_rows)

    # Predicted distribution vs actual distribution
    fig, ax = with_axes(figsize=(7.5, 7.5))
    set_dark_background(fig, ax)
    try:
        sns.kdeplot(y_true, ax=ax, linewidth=1.4, label="Actual", warn_singular=False)
        sns.kdeplot(y_pred, ax=ax, linewidth=1.4, label="Predicted", warn_singular=False)
    except Exception:
        ax.hist(y_true, bins=min(20, max(5, y_true.size // 2)), alpha=0.45, label="Actual", color=PERO.sky)
        ax.hist(y_pred, bins=min(20, max(5, y_pred.size // 2)), alpha=0.45, label="Predicted", color=PERO.orange)
    ax.set_title(f"{target_title} Predicted And Actual Density")
    ax.set_xlabel(y_label)
    legend_outside_top_right(ax, ncol=1)
    polish_axes(ax)
    saved.append(savefig(fig, dist_dir, f"Predicted And Actual Density__{base}", dpi=cfg.figure_dpi, fmt=cfg.figure_format))
    _pad_rows: list[dict] = []
    try:
        from scipy.stats import gaussian_kde

        lo_b = float(min(y_true.min(), y_pred.min()))
        hi_b = float(max(y_true.max(), y_pred.max()))
        if hi_b > lo_b:
            grid_d = np.linspace(lo_b, hi_b, 200)
            for lab, arr in (("actual", y_true), ("predicted", y_pred)):
                a = np.asarray(arr, dtype=float)
                a = a[np.isfinite(a)]
                if a.size >= 2 and np.nanstd(a, ddof=1) > 0:
                    kde = gaussian_kde(a)
                    for xi, di in zip(grid_d, kde(grid_d), strict=False):
                        _pad_rows.append({"series": f"{lab}_kde", "value": float(xi), "density": float(di)})
    except Exception:
        pass
    for v in y_true:
        if np.isfinite(v):
            _pad_rows.append({"series": "actual_sample", "value": float(v)})
    for v in y_pred:
        if np.isfinite(v):
            _pad_rows.append({"series": "predicted_sample", "value": float(v)})
    save_plot_csv(dist_dir, f"Predicted And Actual Density__{base}", _pad_rows)

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
    mc_rows = [
        {
            "series": "bar",
            "model": str(r["model"]),
            "overall_rmse": float(r["OVERALL_RMSE"]),
            "overall_mae": float(r["OVERALL_MAE"]),
            "overall_r2": float(r["OVERALL_R2"]),
        }
        for _, r in top.iterrows()
    ]
    save_plot_csv(out_dir, "Model Comparison Overall Error", mc_rows)
    return out

