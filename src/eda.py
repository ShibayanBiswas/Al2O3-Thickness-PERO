from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

from .plots import annotate_extremes, save_plot_csv, savefig, scatter_with_marginals, with_axes
from .utils import (
    ensure_dir,
    iqr_outliers,
    optional_import,
    safe_filename,
    smooth_curve_1d,
    strip_parentheses_text,
    to_title_case,
    zscore_outliers,
)
from .viz_style import PERO, get_display_labels, legend_outside_top_right, polish_axes, set_dark_background


@dataclass(frozen=True)
class EDAArtifacts:
    group_summary: pd.DataFrame
    pearson_corr: pd.DataFrame
    spearman_corr: pd.DataFrame


def _ecdf(values: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    v = np.asarray(values, dtype=float)
    v = v[np.isfinite(v)]
    if v.size == 0:
        return np.array([]), np.array([])
    x = np.sort(v)
    y = np.arange(1, x.size + 1) / x.size
    return x, y


def _lowess_xy(x: np.ndarray, y: np.ndarray, frac: float = 0.6) -> tuple[np.ndarray, np.ndarray] | None:
    sm = optional_import("statsmodels.api")
    if sm is None:
        return None
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    order = np.argsort(x)
    x_s = x[order]
    y_s = y[order]
    try:
        low = sm.nonparametric.lowess(y_s, x_s, frac=frac, return_sorted=True)
        return low[:, 0], low[:, 1]
    except Exception:
        return None


def _polynomial_fit(x: np.ndarray, y: np.ndarray, degree: int) -> tuple[np.ndarray, np.ndarray]:
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    # For stability with discrete x, use unique x grid for plotting
    grid = np.linspace(float(np.min(x)), float(np.max(x)), 250)
    coefs = np.polyfit(x, y, deg=degree)
    pred = np.polyval(coefs, grid)
    return grid, pred


def _linear_fit_with_residual_quantile_band(
    x: np.ndarray,
    y: np.ndarray,
    q_lo: float = 0.10,
    q_hi: float = 0.90,
) -> tuple[np.ndarray, np.ndarray, float, float] | None:
    """
    Linear fit plus a quantile "area strip" in y induced by residual quantiles.

    Returns (grid_x, y_hat_on_grid, resid_q_lo, resid_q_hi) where the band is
    y_hat(x) + [resid_q_lo, resid_q_hi].
    """
    x = np.asarray(x, dtype=float).ravel()
    y = np.asarray(y, dtype=float).ravel()
    m = np.isfinite(x) & np.isfinite(y)
    x = x[m]
    y = y[m]
    if x.size < 3:
        return None
    coefs = np.polyfit(x, y, deg=1)
    grid = np.linspace(float(np.min(x)), float(np.max(x)), 250)
    yhat_grid = np.polyval(coefs, grid)
    resid = y - np.polyval(coefs, x)
    rq_lo = float(np.nanquantile(resid, q_lo))
    rq_hi = float(np.nanquantile(resid, q_hi))
    if not (np.isfinite(rq_lo) and np.isfinite(rq_hi)):
        return None
    return grid, yhat_grid, rq_lo, rq_hi


def _group_quantiles_by_x(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    qs: tuple[float, ...] = (0.10, 0.50, 0.90),
) -> tuple[np.ndarray, dict[float, np.ndarray]] | None:
    """
    Per-thickness quantiles for discrete x, returned as sorted arrays.
    """
    try:
        gq = df.groupby(x_col)[y_col].quantile(list(qs)).unstack()
        gx = gq.index.to_numpy(dtype=float)
        order = np.argsort(gx)
        gx = gx[order]
        out: dict[float, np.ndarray] = {}
        for q in qs:
            out[q] = gq[q].to_numpy(dtype=float)[order]
        return gx, out
    except Exception:
        return None


def run_deep_eda(
    df: pd.DataFrame,
    x_col: str,
    y_cols: list[str],
    out_plots: Path,
    out_tables: Path,
    cfg: object,
) -> EDAArtifacts:
    import seaborn as sns
    import matplotlib.pyplot as plt

    # Hierarchical plot folders with one more depth level
    out_uni = ensure_dir(out_plots / "Univariate")
    out_bi = ensure_dir(out_plots / "Bivariate")
    out_grp = ensure_dir(out_plots / "Grouped")
    out_rel = ensure_dir(out_plots / "Relationships")
    ensure_dir(out_tables)

    labels = get_display_labels(x_col=x_col, y_cols=y_cols)

    # 2.1 Overview tables
    overview = pd.DataFrame(
        {
            "role": ["feature"] + ["target"] * len(y_cols),
            "name": [x_col] + y_cols,
        }
    )
    overview.to_csv(out_tables / "01_feature_target_definitions.csv", index=False)

    # Distribution summary table for targets
    desc = df[[x_col, *y_cols]].describe(percentiles=[0.05, 0.25, 0.5, 0.75, 0.95]).T
    desc.to_csv(out_tables / "02_describe_numeric.csv")

    # Repeated thickness values
    thickness_counts = df[x_col].value_counts().sort_index()
    thickness_tbl = thickness_counts.reset_index()
    thickness_tbl.columns = [x_col, "count"]
    thickness_tbl["fraction"] = thickness_tbl["count"] / thickness_tbl["count"].sum()
    thickness_tbl.to_csv(out_tables / "03_thickness_value_counts.csv", index=False)

    # 2.2 Univariate plots (feature + each target)
    def univariate_suite(series: pd.Series, name: str):
        vals = series.to_numpy(dtype=float)
        skew = float(pd.Series(vals).skew())
        kurt = float(pd.Series(vals).kurt())
        display = labels.y_label_map.get(name, to_title_case(strip_parentheses_text(name)))
        title = to_title_case(strip_parentheses_text(name))

        var_dir = ensure_dir(out_uni / safe_filename(to_title_case(strip_parentheses_text(name))))

        # Histogram + KDE (explicit series so legend entries always resolve)
        fig, ax = with_axes(figsize=(7.5, 7.5))
        set_dark_background(fig, ax)
        sns.histplot(vals, stat="density", kde=False, ax=ax, color=PERO.sky, edgecolor=PERO.ink, alpha=0.88, label="Histogram")
        sns.kdeplot(vals, ax=ax, color=PERO.orange, linewidth=1.4, warn_singular=False, label="Kernel density")
        ax.set_title(f"{title} Distribution")
        ax.set_xlabel(display)
        ax.set_ylabel("Density")
        legend_outside_top_right(ax, ncol=1, title="Density")
        polish_axes(ax)
        savefig(fig, var_dir, f"Histogram And Kernel Density", dpi=cfg.figure_dpi, fmt=cfg.figure_format)
        save_plot_csv(
            var_dir,
            "Histogram And Kernel Density",
            [{"series": "raw_sample", "value": float(v)} for v in vals if np.isfinite(v)],
        )

        # Box + Violin
        fig, axes = plt.subplots(1, 2, figsize=(7.5, 7.5))
        set_dark_background(fig, axes)
        sns.boxplot(x=vals, ax=axes[0], color=PERO.green)
        axes[0].set_title(f"{title} Box Plot")
        axes[0].set_xlabel(display)
        legend_outside_top_right(
            axes[0],
            handles=[Patch(facecolor=PERO.green, edgecolor=PERO.ink, linewidth=0.9, label="Box quartiles")],
            title="Summary",
        )
        polish_axes(axes[0])
        sns.violinplot(x=vals, ax=axes[1], color=PERO.orange, inner="quartile")
        axes[1].set_title(f"{title} Violin Plot")
        axes[1].set_xlabel(display)
        legend_outside_top_right(
            axes[1],
            handles=[Patch(facecolor=PERO.orange, edgecolor=PERO.ink, linewidth=0.9, label="Kernel + quartiles")],
            title="Summary",
        )
        polish_axes(axes[1])
        savefig(fig, var_dir, f"Box And Violin", dpi=cfg.figure_dpi, fmt=cfg.figure_format)
        save_plot_csv(
            var_dir,
            "Box And Violin",
            [{"series": "raw_sample", "value": float(v)} for v in vals if np.isfinite(v)],
        )

        # Raincloud Style Plot
        try:
            fig, ax = with_axes(figsize=(7.5, 7.5))
            set_dark_background(fig, ax)
            sns.violinplot(x=vals, ax=ax, color=PERO.sky, inner=None, cut=0, linewidth=0)
            sns.boxplot(x=vals, ax=ax, width=0.22, color=PERO.green, fliersize=0)
            sns.stripplot(x=vals, ax=ax, color=PERO.text, alpha=0.65, jitter=0.18, size=5)
            ax.set_title(f"{title} Raincloud Plot")
            ax.set_xlabel(display)
            ax.set_ylabel("")
            legend_outside_top_right(
                ax,
                handles=[
                    Patch(facecolor=PERO.sky, edgecolor=PERO.ink, linewidth=0.6, label="Violin"),
                    Patch(facecolor=PERO.green, edgecolor=PERO.ink, linewidth=0.6, label="Box"),
                    Line2D(
                        [0],
                        [0],
                        marker="o",
                        color="w",
                        markerfacecolor=PERO.text,
                        markeredgecolor=PERO.ink,
                        markersize=7,
                        linestyle="",
                        label="Points",
                    ),
                ],
                title="Layers",
            )
            polish_axes(ax)
            savefig(fig, var_dir, "Raincloud Plot", dpi=cfg.figure_dpi, fmt=cfg.figure_format)
            save_plot_csv(
                var_dir,
                "Raincloud Plot",
                [{"series": "raw_sample", "value": float(v)} for v in vals if np.isfinite(v)],
            )
        except Exception:
            pass

        # ECDF
        x_ecdf, y_ecdf = _ecdf(vals)
        fig, ax = with_axes(figsize=(7.5, 7.5))
        set_dark_background(fig, ax)
        y_ecdf_s = smooth_curve_1d(y_ecdf) if x_ecdf.size >= 3 else y_ecdf
        ax.fill_between(x_ecdf, 0, y_ecdf_s, alpha=0.12, color=PERO.gold, label="Cumulative Area")
        ax.plot(x_ecdf, y_ecdf_s, linestyle="-", alpha=0.92, linewidth=1.5, color=PERO.gold, label="Smoothed ECDF")
        ax.set_title(f"{title} Empirical Cumulative Distribution")
        ax.set_xlabel(display)
        ax.set_ylabel("Cumulative Probability")
        legend_outside_top_right(ax, ncol=1)
        polish_axes(ax)
        savefig(fig, var_dir, f"Empirical Cumulative Distribution", dpi=cfg.figure_dpi, fmt=cfg.figure_format)
        _ecdf_rows = []
        if x_ecdf.size:
            for xa, ya, ys in zip(x_ecdf, y_ecdf, y_ecdf_s, strict=False):
                _ecdf_rows.append(
                    {
                        "series": "ecdf",
                        "x": float(xa),
                        "cumulative_probability": float(ya),
                        "cumulative_smoothed": float(ys),
                    }
                )
        save_plot_csv(var_dir, "Empirical Cumulative Distribution", _ecdf_rows)

        # Scaling Comparison Plot
        try:
            v = pd.Series(vals).dropna().to_numpy(dtype=float)
            if v.size > 2:
                # Multiple scaling algorithms for 1D comparison
                Xv = v.reshape(-1, 1)
                z = (v - np.mean(v)) / (np.std(v, ddof=1) if np.std(v, ddof=1) > 0 else 1.0)
                mm = (v - np.min(v)) / (np.max(v) - np.min(v) if np.max(v) > np.min(v) else 1.0)
                scalers = {}
                try:
                    from sklearn.preprocessing import MaxAbsScaler, PowerTransformer, QuantileTransformer, RobustScaler

                    n_quantiles = min(1000, max(2, int(v.size)))
                    scalers["Robust Scale"] = RobustScaler().fit_transform(Xv).ravel()
                    scalers["Max Abs Scale"] = MaxAbsScaler().fit_transform(Xv).ravel()
                    scalers["Quantile Normal Scale"] = QuantileTransformer(
                        output_distribution="normal", n_quantiles=n_quantiles, random_state=cfg.random_seed
                    ).fit_transform(Xv).ravel()
                    scalers["Quantile Uniform Scale"] = QuantileTransformer(
                        output_distribution="uniform", n_quantiles=n_quantiles, random_state=cfg.random_seed
                    ).fit_transform(Xv).ravel()
                    scalers["Power Yeo Johnson Scale"] = PowerTransformer(method="yeo-johnson", standardize=True).fit_transform(Xv).ravel()
                except Exception:
                    scalers = {}
                fig, ax = with_axes(figsize=(7.5, 7.5))
                set_dark_background(fig, ax)
                sns.kdeplot(v, ax=ax, linewidth=1.4, label="Original Scale", color=PERO.sky, warn_singular=False)
                sns.kdeplot(z, ax=ax, linewidth=1.4, label="Standard Scale", color=PERO.green, warn_singular=False)
                sns.kdeplot(mm, ax=ax, linewidth=1.4, label="Min Max Scale", color=PERO.orange, warn_singular=False)
                palette = PERO.multiline_series()
                for (lab, arr), col in zip(scalers.items(), palette, strict=False):
                    try:
                        sns.kdeplot(arr, ax=ax, linewidth=1.6, label=lab, color=col, warn_singular=False)
                    except Exception:
                        continue
                ax.set_title(f"{title} Scaling Comparison Density")
                ax.set_xlabel(display)
                ax.set_ylabel("Density")
                legend_outside_top_right(ax, ncol=1)
                polish_axes(ax)
                savefig(fig, var_dir, "Scaling Comparison Density", dpi=cfg.figure_dpi, fmt=cfg.figure_format)
                _sc_rows: list[dict] = [{"series": "original_sample", "value": float(t)} for t in v if np.isfinite(t)]
                _sc_rows.extend({"series": "standard_scaled_sample", "value": float(t)} for t in z if np.isfinite(t))
                _sc_rows.extend({"series": "minmax_scaled_sample", "value": float(t)} for t in mm if np.isfinite(t))
                for lab, arr in scalers.items():
                    for t in np.asarray(arr, dtype=float).ravel():
                        if np.isfinite(t):
                            _sc_rows.append({"series": f"scaled::{lab}", "value": float(t)})
                try:
                    from scipy.stats import gaussian_kde

                    lo_g = float(np.min(v))
                    hi_g = float(np.max(v))
                    if hi_g > lo_g:
                        grid_g = np.linspace(lo_g, hi_g, 150)
                        for lab2, arr2 in (
                            ("original_kde", v),
                            ("standard_kde", z),
                            ("minmax_kde", mm),
                            *[(f"kde::{k}", np.asarray(a, dtype=float)) for k, a in scalers.items()],
                        ):
                            a2 = np.asarray(arr2, dtype=float)
                            a2 = a2[np.isfinite(a2)]
                            if a2.size >= 2 and np.nanstd(a2, ddof=1) > 0:
                                kde = gaussian_kde(a2)
                                for xi, di in zip(grid_g, kde(grid_g), strict=False):
                                    _sc_rows.append({"series": lab2, "grid_x": float(xi), "density": float(di)})
                except Exception:
                    pass
                save_plot_csv(var_dir, "Scaling Comparison Density", _sc_rows)
        except Exception:
            pass

        # Outlier reporting
        out_iqr = iqr_outliers(vals)
        out_z = zscore_outliers(vals, threshold=3.0)
        out_tbl = pd.DataFrame(
            {
                "name": [name],
                "n": [int(np.isfinite(vals).sum())],
                "iqr_outliers_count": [int(out_iqr.sum())],
                "zscore_outliers_count": [int(out_z.sum())],
                "skew": [skew],
                "kurtosis": [kurt],
            }
        )
        out_tbl.to_csv(out_tables / f"outliers__{safe_filename(name)}.csv", index=False)

    # Feature is special
    univariate_suite(df[x_col], x_col)
    for y in y_cols:
        univariate_suite(df[y], y)

    # 2.3 Single-feature vs target analysis (scatter + lowess + poly overlays, residual-like)
    x = df[x_col].to_numpy(dtype=float)
    x_j = x + np.random.default_rng(cfg.random_seed).normal(0, cfg.jitter_strength, size=x.shape)

    corr_rows = []
    for y in y_cols:
        yv = df[y].to_numpy(dtype=float)
        y_label = labels.y_label_map.get(y, to_title_case(strip_parentheses_text(y)))
        y_title = labels.target_title_map.get(y, to_title_case(strip_parentheses_text(y)))

        y_dir = ensure_dir(out_bi / safe_filename(y_title))

        # Scatter + jitter + trends
        fig, ax = with_axes(figsize=(7.5, 7.5))
        set_dark_background(fig, ax)
        ax.scatter(x_j, yv, alpha=0.82, s=64, edgecolor=PERO.ink, linewidth=0.8, label="Observed Points", color=PERO.sky)

        plot_rows: list[dict] = []
        for xi, yi in zip(x, yv, strict=False):
            plot_rows.append({"layer": "points", "x": float(xi), "y": float(yi)})

        # Mandatory area shade based on thickness-level quartiles
        try:
            gq = df.groupby(x_col)[y].quantile([0.25, 0.5, 0.75]).unstack()
            gx = gq.index.to_numpy(dtype=float)
            q25 = gq[0.25].to_numpy(dtype=float)
            q50 = gq[0.5].to_numpy(dtype=float)
            q75 = gq[0.75].to_numpy(dtype=float)
            order = np.argsort(gx)
            q25s = smooth_curve_1d(q25[order])
            q75s = smooth_curve_1d(q75[order])
            q50s = smooth_curve_1d(q50[order])
            gxo = gx[order]
            ax.fill_between(gxo, q25s, q75s, color=PERO.text, alpha=0.08, label="_nolegend_")
            ax.plot(gxo, q50s, color=PERO.green, linewidth=1.20, label="Median By Thickness")
            ax.plot(gxo, q25s, color=PERO.green, linewidth=0.85, linestyle="--", alpha=0.45, label="_nolegend_")
            ax.plot(gxo, q75s, color=PERO.green, linewidth=0.85, linestyle="--", alpha=0.45, label="_nolegend_")
            for xi, lo, mid, hi in zip(gxo, q25s, q50s, q75s, strict=False):
                plot_rows.append({"layer": "x_iqr_band", "x": float(xi), "y_lo": float(lo), "y_hi": float(hi)})
                plot_rows.append({"layer": "x_median", "x": float(xi), "y": float(mid)})
        except Exception:
            pass

        # Reference y-range helpers (for area fills / rugs)
        try:
            yv_f = yv[np.isfinite(yv)]
            y_lo = float(np.min(yv_f)) if yv_f.size else 0.0
            y_hi = float(np.max(yv_f)) if yv_f.size else 1.0
            y_span = float(y_hi - y_lo + 1e-9)
        except Exception:
            y_lo, y_hi, y_span = 0.0, 1.0, 1.0

        # Linear trend + quantile area strip (residual-quantile band)
        try:
            fit = _linear_fit_with_residual_quantile_band(x, yv, q_lo=0.10, q_hi=0.90)
            if fit is not None:
                gx, gp, rq_lo, rq_hi = fit
                ax.fill_between(gx, gp + rq_lo, gp + rq_hi, color=PERO.orange, alpha=0.10, label="_nolegend_")
                ax.plot(gx, gp, color=PERO.orange, linewidth=1.25, label="Linear Trend")
                for xi, yi in zip(gx, gp, strict=False):
                    plot_rows.append({"layer": "linear_trend", "x": float(xi), "y": float(yi)})
                for xi, lo, hi in zip(gx, gp + rq_lo, gp + rq_hi, strict=False):
                    plot_rows.append({"layer": "linear_trend_band_10_90", "x": float(xi), "y_lo": float(lo), "y_hi": float(hi)})
        except Exception:
            pass

        # Thickness rug (shows discrete support without cluttering the y-scale)
        try:
            rug_y = y_lo - 0.04 * y_span
            ax.scatter(x, np.full_like(x, rug_y, dtype=float), s=14, alpha=0.30, color=PERO.text, edgecolor=PERO.ink, linewidth=0.35, label="_nolegend_")
        except Exception:
            pass

        # User requirement: do not label individual points inside scatter plots.
        ax.set_title(f"{y_title} Versus Thickness")
        ax.set_xlabel(labels.x_label)
        ax.set_ylabel(y_label)
        legend_outside_top_right(ax, ncol=1)
        polish_axes(ax)
        save_plot_csv(y_dir, "Scatter With Trends", plot_rows)
        savefig(fig, y_dir, "Scatter With Trends", dpi=cfg.figure_dpi, fmt=cfg.figure_format)

        # Sorted-by-thickness line plot
        order = np.argsort(x)
        fig, ax = with_axes(figsize=(7.5, 7.5))
        set_dark_background(fig, ax)
        xs = x[order]
        ys = yv[order]
        ys_s = smooth_curve_1d(ys)
        ax.plot(xs, ys_s, linewidth=1.35, color=PERO.sky, label="Smoothed Profile")
        span = float(np.nanmax(ys_s) - np.nanmin(ys_s) + 1e-9)
        y_floor = float(np.nanmin(ys_s) - 0.03 * span)
        ax.fill_between(xs, y_floor, ys_s, color=PERO.sky, alpha=0.08, label="Profile Area")
        try:
            s = pd.Series(ys)
            win = min(9, max(3, ys.size // 5))
            q25 = s.rolling(window=win, center=True, min_periods=1).quantile(0.25).to_numpy()
            q75 = s.rolling(window=win, center=True, min_periods=1).quantile(0.75).to_numpy()
            med = s.rolling(window=win, center=True, min_periods=1).median().to_numpy()
            q25s = smooth_curve_1d(q25)
            q75s = smooth_curve_1d(q75)
            meds = smooth_curve_1d(med)
            ax.fill_between(xs, q25s, q75s, color=PERO.text, alpha=0.10, label="_nolegend_")
            ax.plot(xs, meds, color=PERO.green, linewidth=1.25, label="Rolling Median")
            ax.plot(xs, q25s, color=PERO.green, linewidth=1.0, linestyle="--", alpha=0.4, label="Rolling Lower")
            ax.plot(xs, q75s, color=PERO.green, linewidth=1.0, linestyle="--", alpha=0.4, label="Rolling Upper")
        except Exception:
            pass
        ax.set_title(f"{y_title} Sorted By Thickness")
        ax.set_xlabel(labels.x_label)
        ax.set_ylabel(y_label)
        legend_outside_top_right(ax, ncol=1)
        polish_axes(ax)
        sp_rows: list[dict] = [{"layer": "smoothed_profile", "x": float(xi), "y": float(yi)} for xi, yi in zip(xs, ys_s, strict=False)]
        save_plot_csv(y_dir, "Sorted Profile", sp_rows)
        savefig(fig, y_dir, "Sorted Profile", dpi=cfg.figure_dpi, fmt=cfg.figure_format)

        # Residual-like view vs thickness (linear only)
        fig, ax = with_axes(figsize=(7.5, 7.5))
        set_dark_background(fig, ax)
        try:
            coefs = np.polyfit(x, yv, deg=1)
            pred = np.polyval(coefs, x)
            resid = yv - pred
            ax.scatter(x_j, resid, alpha=0.75, s=46, label="Linear Residuals", color=PERO.teal, edgecolor=PERO.ink, linewidth=0.6)
        except Exception:
            pass
        ax.axhline(0, color=PERO.text, linewidth=1.2, alpha=0.85)
        ax.set_title(f"{y_title} Residual Pattern By Thickness")
        ax.set_xlabel(labels.x_label)
        ax.set_ylabel("Residual")
        legend_outside_top_right(ax, ncol=1)
        polish_axes(ax)
        rp_rows: list[dict] = []
        try:
            for xi, ri in zip(x, resid, strict=False):
                rp_rows.append({"layer": "residuals", "x": float(xi), "y": float(ri)})
        except Exception:
            pass
        save_plot_csv(y_dir, "Residual Pattern", rp_rows)
        savefig(fig, y_dir, "Residual Pattern", dpi=cfg.figure_dpi, fmt=cfg.figure_format)

        # Binned summary by thickness levels (since x is discrete, group-by exact x)
        grp = df.groupby(x_col)[y].agg(["count", "mean", "median", "std", "min", "max"]).reset_index()
        grp.to_csv(out_tables / f"group_by_thickness__{safe_filename(y)}.csv", index=False)

        # Correlation (Pearson/Spearman against x)
        pear = float(pd.Series(x).corr(pd.Series(yv), method="pearson"))
        spear = float(pd.Series(x).corr(pd.Series(yv), method="spearman"))
        corr_rows.append({"target": y, "pearson_r": pear, "spearman_r": spear})

    corr_tbl = pd.DataFrame(corr_rows).sort_values("target")
    corr_tbl.to_csv(out_tables / "04_thickness_target_correlations.csv", index=False)

    # 2.4 Group comparisons across thickness levels
    group_summary = df.groupby(x_col)[y_cols].agg(["count", "mean", "median", "std", "min", "max"])
    group_summary.to_csv(out_tables / "05_grouped_summary_all_targets_by_thickness.csv")

    # Plot group-wise means with error bars
    for y in y_cols:
        g = df.groupby(x_col)[y].agg(["count", "mean", "std"]).reset_index().sort_values(x_col)
        fig, ax = with_axes(figsize=(7.5, 7.5))
        set_dark_background(fig, ax)
        y_title = labels.target_title_map.get(y, to_title_case(strip_parentheses_text(y)))
        y_label = labels.y_label_map.get(y, to_title_case(strip_parentheses_text(y)))
        gx = g[x_col].to_numpy(dtype=float)
        mu = g["mean"].to_numpy(dtype=float)
        sg = g["std"].to_numpy(dtype=float)
        mu_s = smooth_curve_1d(mu)
        lo_s = smooth_curve_1d(mu - sg)
        hi_s = smooth_curve_1d(mu + sg)
        qpack = _group_quantiles_by_x(df, x_col=x_col, y_col=y, qs=(0.10, 0.50, 0.90))
        if qpack is not None:
            gx_q, qd = qpack
            q10 = smooth_curve_1d(qd[0.10])
            q50 = smooth_curve_1d(qd[0.50])
            q90 = smooth_curve_1d(qd[0.90])
            ax.fill_between(gx_q, q10, q90, color=PERO.text, alpha=0.10, label="_nolegend_")
            ax.plot(gx_q, q50, linestyle="-", linewidth=1.25, color=PERO.green, label="Median Curve")
        else:
            ax.fill_between(gx, lo_s, hi_s, color=PERO.text, alpha=0.10, label="_nolegend_")
            ax.plot(gx, mu_s, linestyle="-", linewidth=1.25, color=PERO.green, label="Mean Curve")
        ax.set_title(f"{y_title} Group Mean With Uncertainty")
        ax.set_xlabel(labels.x_label)
        ax.set_ylabel(y_label)
        legend_outside_top_right(ax, ncol=1)
        polish_axes(ax)
        y_dir = ensure_dir(out_grp / safe_filename(y_title))
        gm_rows: list[dict] = []
        if qpack is not None:
            for xi, lo, mid, hi in zip(gx_q, q10, q50, q90, strict=False):
                gm_rows.append({"layer": "quantile_band_10_90", "x": float(xi), "y_lo": float(lo), "y_hi": float(hi)})
                gm_rows.append({"layer": "median", "x": float(xi), "y": float(mid)})
        else:
            for xi, yi in zip(gx, mu_s, strict=False):
                gm_rows.append({"layer": "mean", "x": float(xi), "y": float(yi)})
        save_plot_csv(y_dir, "Group Mean With Uncertainty", gm_rows)
        savefig(fig, y_dir, "Group Mean With Uncertainty", dpi=cfg.figure_dpi, fmt=cfg.figure_format)

    # Compare 0.0 vs non-zero
    zero_mask = df[x_col] == 0.0
    compare_rows = []
    for y in y_cols:
        z = df.loc[zero_mask, y]
        nz = df.loc[~zero_mask, y]
        compare_rows.append(
            {
                "target": y,
                "n_zero": int(z.shape[0]),
                "n_nonzero": int(nz.shape[0]),
                "zero_mean": float(z.mean()),
                "nonzero_mean": float(nz.mean()),
                "zero_median": float(z.median()),
                "nonzero_median": float(nz.median()),
                "delta_mean_nonzero_minus_zero": float(nz.mean() - z.mean()),
                "delta_median_nonzero_minus_zero": float(nz.median() - z.median()),
            }
        )
    pd.DataFrame(compare_rows).to_csv(out_tables / "06_zero_vs_nonzero_comparison.csv", index=False)

    # 2.5 Relationship matrix
    num_df = df[[x_col, *y_cols]].copy()
    # Use short, display-safe names to avoid axis label overlap in dense grids
    # Pair plots are especially sensitive to long axis labels.
    display_name = {x_col: "Thickness"}
    display_name.update(
        {
            "Rct_initial_ohm": "Rct Initial",
            "ICE_percent": "Coulombic Efficiency",
            "Initial Reversible Capacity_mAh_g at 0.1C": "Reversible Capacity",
            "Highest Capacity Retention_percent": "Capacity Retention",
        }
    )
    for y in y_cols:
        display_name.setdefault(y, labels.target_title_map.get(y, to_title_case(strip_parentheses_text(y))))
    num_df_disp = num_df.rename(columns=display_name)

    pearson_corr = num_df.corr(method="pearson")
    spearman_corr = num_df.corr(method="spearman")
    pearson_corr.to_csv(out_tables / "07_corr_pearson.csv")
    spearman_corr.to_csv(out_tables / "08_corr_spearman.csv")

    fig, ax = with_axes(figsize=(7.5, 7.5))
    set_dark_background(fig, ax)
    sns.heatmap(
        pearson_corr.rename(index=display_name, columns=display_name),
        annot=True,
        fmt=".2f",
        cmap="vlag",
        ax=ax,
        linewidths=0.55,
        linecolor=PERO.panel,
        cbar_kws={"shrink": 0.85, "label": r"Pearson $\rho$"},
    )
    ax.set_title(r"Correlation heatmap: Pearson $\rho$")
    ax.tick_params(axis="x", labelrotation=28, labelsize=10)
    ax.tick_params(axis="y", labelrotation=0, labelsize=10)
    for lab in ax.get_xticklabels():
        lab.set_horizontalalignment("right")
    fig.tight_layout(pad=1.2)
    polish_axes(ax)
    savefig(fig, out_rel, "Correlation Heatmap Pearson", dpi=cfg.figure_dpi, fmt=cfg.figure_format)
    _p_disp = pearson_corr.rename(index=display_name, columns=display_name)
    _ph_rows = [
        {"series": "heatmap", "row": str(i), "col": str(j), "pearson_rho": float(_p_disp.loc[i, j])}
        for i in _p_disp.index
        for j in _p_disp.columns
    ]
    save_plot_csv(out_rel, "Correlation Heatmap Pearson", _ph_rows)

    fig, ax = with_axes(figsize=(7.5, 7.5))
    set_dark_background(fig, ax)
    sns.heatmap(
        spearman_corr.rename(index=display_name, columns=display_name),
        annot=True,
        fmt=".2f",
        cmap="vlag",
        ax=ax,
        linewidths=0.55,
        linecolor=PERO.panel,
        cbar_kws={"shrink": 0.85, "label": r"Spearman $\rho_{\mathrm{s}}$"},
    )
    ax.set_title(r"Correlation heatmap: Spearman $\rho_{\mathrm{s}}$")
    ax.tick_params(axis="x", labelrotation=28, labelsize=10)
    ax.tick_params(axis="y", labelrotation=0, labelsize=10)
    for lab in ax.get_xticklabels():
        lab.set_horizontalalignment("right")
    fig.tight_layout(pad=1.2)
    polish_axes(ax)
    savefig(fig, out_rel, "Correlation Heatmap Spearman", dpi=cfg.figure_dpi, fmt=cfg.figure_format)
    _s_disp = spearman_corr.rename(index=display_name, columns=display_name)
    _sh_rows = [
        {"series": "heatmap", "row": str(i), "col": str(j), "spearman_rho_s": float(_s_disp.loc[i, j])}
        for i in _s_disp.index
        for j in _s_disp.columns
    ]
    save_plot_csv(out_rel, "Correlation Heatmap Spearman", _sh_rows)

    # Pairplot (can be heavy but dataset is tiny)
    try:
        pp = sns.pairplot(num_df_disp, corner=True, diag_kind="hist")
        pp.fig.suptitle("Pair Plot Numeric Variables", y=1.02)
        # Make axes labels readable without overlap
        try:
            set_dark_background(pp.fig, [ax for ax in pp.axes.flatten() if ax is not None])
        except Exception:
            pass
        for axp in [ax for ax in pp.axes.flatten() if ax is not None]:
            try:
                axp.tick_params(axis="x", labelrotation=28, labelsize=9)
                axp.tick_params(axis="y", labelrotation=0, labelsize=9)
                for lab in axp.get_xticklabels():
                    lab.set_horizontalalignment("right")
            except Exception:
                pass
        pp.fig.subplots_adjust(left=0.10, bottom=0.10, right=0.98, top=0.94, wspace=0.08, hspace=0.08)
        pp.fig.tight_layout(pad=1.1, rect=[0, 0, 0.98, 0.94])
        out_path = out_rel / f"{safe_filename('Pair Plot Numeric Variables')}.{cfg.figure_format}"
        pp.fig.savefig(out_path, dpi=cfg.figure_dpi, bbox_inches="tight")
        plt.close(pp.fig)
        save_plot_csv(
            out_rel,
            "Pair Plot Numeric Variables",
            num_df_disp.reset_index(drop=True).to_dict(orient="records"),
        )
    except Exception:
        # Safe fallback (never crash)
        pass

    # Optional mutual information (single-feature setting)
    try:
        from sklearn.feature_selection import mutual_info_regression

        mi_rows = []
        X = df[[x_col]].to_numpy(dtype=float)
        for y in y_cols:
            yv = df[y].to_numpy(dtype=float)
            mi = float(mutual_info_regression(X, yv, random_state=cfg.random_seed)[0])
            mi_rows.append({"target": y, "mutual_info": mi})
        pd.DataFrame(mi_rows).to_csv(out_tables / "09_mutual_information_single_feature.csv", index=False)
    except Exception:
        pass

    # 3D plots removed by requirement. Advanced EDA remains fully 2D via trend overlays,
    # grouped uncertainty bands, and residual structure diagnostics.

    return EDAArtifacts(group_summary=group_summary.reset_index(), pearson_corr=pearson_corr, spearman_corr=spearman_corr)

