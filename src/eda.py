from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

from .plots import annotate_extremes, savefig, with_axes
from .utils import ensure_dir, iqr_outliers, optional_import, safe_filename, strip_parentheses_text, to_title_case, zscore_outliers
from .viz_style import get_display_labels, legend_outside_top_right, polish_axes, set_dark_background


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

        # Histogram + KDE
        fig, ax = with_axes(figsize=(10, 6))
        sns.histplot(vals, kde=True, ax=ax, color="#5BC0EB", edgecolor="#0B0F1A", alpha=0.92)
        ax.set_title(f"{title} Distribution")
        ax.set_xlabel(display)
        ax.set_ylabel("Density")
        polish_axes(ax)
        savefig(fig, var_dir, f"Histogram And Kernel Density", dpi=cfg.figure_dpi, fmt=cfg.figure_format)

        # Box + Violin
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))
        sns.boxplot(x=vals, ax=axes[0], color="#9FD356")
        axes[0].set_title(f"{title} Box Plot")
        axes[0].set_xlabel(display)
        polish_axes(axes[0])
        sns.violinplot(x=vals, ax=axes[1], color="#FF9F1C", inner="quartile")
        axes[1].set_title(f"{title} Violin Plot")
        axes[1].set_xlabel(display)
        polish_axes(axes[1])
        savefig(fig, var_dir, f"Box And Violin", dpi=cfg.figure_dpi, fmt=cfg.figure_format)

        # Raincloud Style Plot
        try:
            fig, ax = with_axes(figsize=(11, 4))
            sns.violinplot(x=vals, ax=ax, color="#5BC0EB", inner=None, cut=0, linewidth=0)
            sns.boxplot(x=vals, ax=ax, width=0.22, color="#9FD356", fliersize=0)
            sns.stripplot(x=vals, ax=ax, color="#EAF0FF", alpha=0.65, jitter=0.18, size=5)
            ax.set_title(f"{title} Raincloud Plot")
            ax.set_xlabel(display)
            ax.set_ylabel("")
            polish_axes(ax)
            savefig(fig, var_dir, "Raincloud Plot", dpi=cfg.figure_dpi, fmt=cfg.figure_format)
        except Exception:
            pass

        # ECDF
        x_ecdf, y_ecdf = _ecdf(vals)
        fig, ax = with_axes(figsize=(10, 6))
        set_dark_background(fig, ax)
        # Line only, no markers
        ax.plot(x_ecdf, y_ecdf, linestyle="-", alpha=0.92, color="#F7B801")
        ax.fill_between(x_ecdf, 0, y_ecdf, alpha=0.12, color="#F7B801")
        ax.set_title(f"{title} Empirical Cumulative Distribution")
        ax.set_xlabel(display)
        ax.set_ylabel("Cumulative Probability")
        polish_axes(ax)
        savefig(fig, var_dir, f"Empirical Cumulative Distribution", dpi=cfg.figure_dpi, fmt=cfg.figure_format)

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

                    scalers["Robust Scale"] = RobustScaler().fit_transform(Xv).ravel()
                    scalers["Max Abs Scale"] = MaxAbsScaler().fit_transform(Xv).ravel()
                    scalers["Quantile Normal Scale"] = QuantileTransformer(output_distribution="normal", random_state=cfg.random_seed).fit_transform(Xv).ravel()
                    scalers["Quantile Uniform Scale"] = QuantileTransformer(output_distribution="uniform", random_state=cfg.random_seed).fit_transform(Xv).ravel()
                    scalers["Power Yeo Johnson Scale"] = PowerTransformer(method="yeo-johnson", standardize=True).fit_transform(Xv).ravel()
                except Exception:
                    scalers = {}
                fig, ax = with_axes(figsize=(10, 5))
                set_dark_background(fig, ax)
                sns.kdeplot(v, ax=ax, linewidth=2.8, label="Original Scale", color="#5BC0EB")
                sns.kdeplot(z, ax=ax, linewidth=2.8, label="Standard Scale", color="#9FD356")
                sns.kdeplot(mm, ax=ax, linewidth=2.8, label="Min Max Scale", color="#FF9F1C")
                palette = ["#5E2BFF", "#F7B801", "#D7263D", "#1B998B", "#C17CFF"]
                for (lab, arr), col in zip(scalers.items(), palette, strict=False):
                    try:
                        sns.kdeplot(arr, ax=ax, linewidth=2.4, label=lab, color=col)
                    except Exception:
                        continue
                ax.set_title(f"{title} Scaling Comparison Density")
                ax.set_xlabel(display)
                ax.set_ylabel("Density")
                legend_outside_top_right(ax, ncol=1)
                polish_axes(ax)
                savefig(fig, var_dir, "Scaling Comparison Density", dpi=cfg.figure_dpi, fmt=cfg.figure_format)
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

        # Scatter + jitter + linear trend only
        fig, ax = with_axes(figsize=(11, 7))
        set_dark_background(fig, ax)
        ax.scatter(x_j, yv, alpha=0.82, s=64, edgecolor="#0B0F1A", linewidth=0.8, label="Observed Points", color="#5BC0EB")

        # Mandatory area shade based on thickness level quartiles
        try:
            gq = df.groupby(x_col)[y].quantile([0.25, 0.5, 0.75]).unstack()
            gx = gq.index.to_numpy(dtype=float)
            q25 = gq[0.25].to_numpy(dtype=float)
            q50 = gq[0.5].to_numpy(dtype=float)
            q75 = gq[0.75].to_numpy(dtype=float)
            order = np.argsort(gx)
            ax.fill_between(gx[order], q25[order], q75[order], color="#EAF0FF", alpha=0.08, label="Interquartile Band")
            ax.plot(gx[order], q50[order], color="#9FD356", linewidth=2.8, label="Median By Thickness")
        except Exception:
            pass

        # Linear trend
        try:
            gx, gp = _polynomial_fit(x, yv, degree=1)
            ax.plot(gx, gp, color="#FF9F1C", linewidth=3.2, label="Linear Trend")
            # Shade a narrow band around the linear trend based on residual spread
            pred_x = np.polyval(np.polyfit(x, yv, deg=1), x)
            resid = yv - pred_x
            band = float(np.nanstd(resid, ddof=1)) if np.isfinite(np.nanstd(resid, ddof=1)) else 0.0
            if band > 0:
                ax.fill_between(gx, gp - band, gp + band, color="#FF9F1C", alpha=0.08, label="Trend Band")
        except Exception:
            pass

        annotate_extremes(ax, x, yv, n=2, label_fmt=lambda i, xi, yi: "Notable Point")
        ax.set_title(f"{y_title} Versus Thickness")
        ax.set_xlabel(labels.x_label)
        ax.set_ylabel(y_label)
        legend_outside_top_right(ax, ncol=1)
        polish_axes(ax)
        savefig(fig, y_dir, "Scatter With Trends", dpi=cfg.figure_dpi, fmt=cfg.figure_format)

        # Sorted-by-thickness line plot
        order = np.argsort(x)
        fig, ax = with_axes(figsize=(11, 6))
        set_dark_background(fig, ax)
        xs = x[order]
        ys = yv[order]
        # Smooth line
        try:
            from scipy.signal import savgol_filter

            w = 11 if ys.size >= 11 else (ys.size // 2) * 2 + 1
            ys_s = savgol_filter(ys, window_length=max(5, w), polyorder=3)
        except Exception:
            ys_s = ys
        ax.plot(xs, ys_s, linewidth=3.0, color="#5BC0EB", label="Smoothed Profile")
        # Mandatory shaded band: rolling interquartile around the sorted curve
        try:
            s = pd.Series(ys)
            q25 = s.rolling(window=min(9, max(3, ys.size // 5)), center=True, min_periods=1).quantile(0.25).to_numpy()
            q75 = s.rolling(window=min(9, max(3, ys.size // 5)), center=True, min_periods=1).quantile(0.75).to_numpy()
            ax.fill_between(xs, q25, q75, color="#EAF0FF", alpha=0.10, label="Interquartile Band")
            ax.plot(xs, pd.Series(ys).rolling(window=min(9, max(3, ys.size // 5)), center=True, min_periods=1).median(), color="#9FD356", linewidth=2.4, label="Rolling Median")
        except Exception:
            pass
        ax.set_title(f"{y_title} Sorted By Thickness")
        ax.set_xlabel(labels.x_label)
        ax.set_ylabel(y_label)
        legend_outside_top_right(ax, ncol=1)
        polish_axes(ax)
        savefig(fig, y_dir, "Sorted Profile", dpi=cfg.figure_dpi, fmt=cfg.figure_format)

        # Residual-like view vs thickness (linear and cubic)
        fig, ax = with_axes(figsize=(11, 6))
        set_dark_background(fig, ax)
        for deg, col, name in [(1, "#1B998B", "Linear Residuals"), (3, "#FF9F1C", "Cubic Residuals")]:
            try:
                coefs = np.polyfit(x, yv, deg=deg)
                pred = np.polyval(coefs, x)
                resid = yv - pred
                ax.scatter(x_j, resid, alpha=0.75, s=50, label=name, color=col, edgecolor="#0B0F1A", linewidth=0.7)
            except Exception:
                pass
        ax.axhline(0, color="#EAF0FF", linewidth=1.2, alpha=0.85)
        ax.set_title(f"{y_title} Residual Pattern By Thickness")
        ax.set_xlabel(labels.x_label)
        ax.set_ylabel("Residual")
        legend_outside_top_right(ax, ncol=1)
        polish_axes(ax)
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
        g = df.groupby(x_col)[y].agg(["count", "mean", "std"]).reset_index()
        fig, ax = with_axes(figsize=(11, 6))
        set_dark_background(fig, ax)
        y_title = labels.target_title_map.get(y, to_title_case(strip_parentheses_text(y)))
        y_label = labels.y_label_map.get(y, to_title_case(strip_parentheses_text(y)))
        # Line only, no markers
        ax.errorbar(g[x_col], g["mean"], yerr=g["std"], fmt="-", capsize=5, linewidth=3.0, color="#9FD356", label="Mean With Spread")
        ax.fill_between(g[x_col], g["mean"] - g["std"], g["mean"] + g["std"], color="#9FD356", alpha=0.12)
        ax.set_title(f"{y_title} Group Mean With Uncertainty")
        ax.set_xlabel(labels.x_label)
        ax.set_ylabel(y_label)
        legend_outside_top_right(ax, ncol=1)
        polish_axes(ax)
        y_dir = ensure_dir(out_grp / safe_filename(y_title))
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

    fig, ax = with_axes(figsize=(10, 8))
    set_dark_background(fig, ax)
    sns.heatmap(
        pearson_corr.rename(index=display_name, columns=display_name),
        annot=True,
        fmt=".2f",
        cmap="vlag",
        ax=ax,
        cbar_kws={"shrink": 0.85},
    )
    ax.set_title("Correlation Heatmap Pearson")
    ax.tick_params(axis="x", labelrotation=28, labelsize=10)
    ax.tick_params(axis="y", labelrotation=0, labelsize=10)
    for lab in ax.get_xticklabels():
        lab.set_horizontalalignment("right")
    fig.tight_layout(pad=1.2)
    polish_axes(ax)
    savefig(fig, out_rel, "Correlation Heatmap Pearson", dpi=cfg.figure_dpi, fmt=cfg.figure_format)

    fig, ax = with_axes(figsize=(10, 8))
    set_dark_background(fig, ax)
    sns.heatmap(
        spearman_corr.rename(index=display_name, columns=display_name),
        annot=True,
        fmt=".2f",
        cmap="vlag",
        ax=ax,
        cbar_kws={"shrink": 0.85},
    )
    ax.set_title("Correlation Heatmap Spearman")
    ax.tick_params(axis="x", labelrotation=28, labelsize=10)
    ax.tick_params(axis="y", labelrotation=0, labelsize=10)
    for lab in ax.get_xticklabels():
        lab.set_horizontalalignment("right")
    fig.tight_layout(pad=1.2)
    polish_axes(ax)
    savefig(fig, out_rel, "Correlation Heatmap Spearman", dpi=cfg.figure_dpi, fmt=cfg.figure_format)

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

