from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from .plots import savefig, with_axes
from .utils import ensure_dir, optional_import, safe_filename, strip_parentheses_text, to_title_case
from .viz_style import get_display_labels, legend_outside_top_right, polish_axes, set_dark_background


@dataclass(frozen=True)
class ExplainArtifacts:
    permutation_importance: pd.DataFrame | None


def permutation_importance_single_feature(
    model: Any,
    X: pd.DataFrame,
    Y: pd.DataFrame,
    y_cols: list[str],
    random_seed: int,
    n_repeats: int = 200,
) -> pd.DataFrame:
    from sklearn.inspection import permutation_importance
    from sklearn.metrics import r2_score, make_scorer

    # For multi-output, permutation_importance uses estimator.score by default.
    # We implement per-target via wrappers: compute importance for each target with a single-output model if needed.
    # Here: simplest robust method: use estimator as-is but compute r2 for each output on permutations manually.
    rng = np.random.default_rng(random_seed)
    Xv = X.to_numpy(dtype=float)
    Yv = Y.to_numpy(dtype=float)
    base_pred = model.predict(X)
    base_pred = np.asarray(base_pred, dtype=float)
    base_r2 = [float(r2_score(Yv[:, j], base_pred[:, j])) for j in range(Yv.shape[1])]

    importances = []
    for rep in range(n_repeats):
        X_perm = Xv.copy()
        rng.shuffle(X_perm[:, 0])
        pred_perm = model.predict(X_perm)
        pred_perm = np.asarray(pred_perm, dtype=float)
        r2_perm = [float(r2_score(Yv[:, j], pred_perm[:, j])) for j in range(Yv.shape[1])]
        drops = [base_r2[j] - r2_perm[j] for j in range(len(y_cols))]
        importances.append(drops)

    imp = np.asarray(importances, dtype=float)
    rows = []
    for j, name in enumerate(y_cols):
        rows.append(
            {
                "target": name,
                "feature": X.columns[0],
                "r2_drop_mean": float(np.mean(imp[:, j])),
                "r2_drop_std": float(np.std(imp[:, j], ddof=1)),
                "n_repeats": n_repeats,
            }
        )
    return pd.DataFrame(rows)


def shap_explain_1d_single_output(
    estimator: Any,
    X: pd.DataFrame,
    target: str,
    out_plots: Path,
    cfg: object,
    max_samples: int = 51,
) -> list[Path]:
    """
    SHAP for single-feature, single-output estimator.
    Multi-output models are handled by fitting per-target clones in run_explainability.
    """
    shap = optional_import("shap")
    if shap is None:
        return []

    ensure_dir(out_plots)
    saved: list[Path] = []

    X_use = X.copy()
    if X_use.shape[0] > max_samples:
        X_use = X_use.sample(max_samples, random_state=getattr(cfg, "random_seed", 42))

    # Use shap.Explainer where possible so beeswarm and waterfall work consistently
    try:
        explainer = shap.Explainer(estimator, X_use)
        shap_values = explainer(X_use)
    except Exception:
        return []

    labels = get_display_labels(x_col=X.columns[0], y_cols=[target])
    t_title = labels.target_title_map.get(target, to_title_case(strip_parentheses_text(target)))

    # Custom Beeswarm Style Plot for Single Feature
    try:
        import matplotlib.pyplot as plt
        import seaborn as sns

        xvals = X_use.iloc[:, 0].to_numpy(dtype=float)
        svals = np.asarray(shap_values.values, dtype=float).reshape(-1)
        # jitter for visibility with discrete x
        rng = np.random.default_rng(getattr(cfg, "random_seed", 42))
        xj = xvals + rng.normal(0, 0.02 * (np.nanmax(xvals) - np.nanmin(xvals) + 1e-9), size=xvals.shape)

        fig, ax = plt.subplots(figsize=(12, 7))
        ax.fill_between(
            np.sort(xvals),
            np.quantile(svals, 0.10) * np.ones_like(np.sort(xvals)),
            np.quantile(svals, 0.90) * np.ones_like(np.sort(xvals)),
            color="#EAF0FF",
            alpha=0.06,
            label="Shap Band",
        )
        ax.scatter(xj, svals, s=62, alpha=0.78, color="#5BC0EB", edgecolor="#0B0F1A", linewidth=0.8, label="Shap Values")
        # Smooth trend of SHAP value vs thickness
        try:
            order = np.argsort(xvals)
            ax.plot(xvals[order], _smooth_curve(svals[order]), color="#FF9F1C", linewidth=3.0, label="Smoothed Trend")
            ax.fill_between(xvals[order], _smooth_curve(svals[order]) - np.nanstd(svals), _smooth_curve(svals[order]) + np.nanstd(svals), color="#FF9F1C", alpha=0.08, label="Trend Band")
        except Exception:
            pass

        ax.set_title(f"{t_title} Shap Summary Beeswarm")
        ax.set_xlabel(labels.x_label)
        ax.set_ylabel("Shap Value")
        legend_outside_top_right(ax, ncol=1)
        polish_axes(ax)
        saved.append(savefig(fig, out_plots, f"shap_beeswarm__{target}", dpi=cfg.figure_dpi, fmt=cfg.figure_format))
    except Exception:
        pass

    # Custom Bar Plot for Single Feature Importance
    try:
        import matplotlib.pyplot as plt

        mean_abs = float(np.nanmean(np.abs(np.asarray(shap_values.values, dtype=float).reshape(-1))))
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.barh(["Thickness"], [mean_abs], color="#9FD356")
        ax.set_title(f"{t_title} Shap Summary Bar")
        ax.set_xlabel("Mean Absolute Shap Value")
        ax.text(
            0.98,
            0.98,
            "Shap Bar",
            transform=ax.transAxes,
            ha="right",
            va="top",
            fontsize=11,
            bbox={"facecolor": "#121B2E", "edgecolor": "#3A466B", "alpha": 0.9, "pad": 0.4},
        )
        polish_axes(ax)
        saved.append(savefig(fig, out_plots, f"shap_bar__{target}", dpi=cfg.figure_dpi, fmt=cfg.figure_format))
    except Exception:
        pass

    # Custom Dependence Plot for Single Feature
    try:
        import matplotlib.pyplot as plt

        xvals = X_use.iloc[:, 0].to_numpy(dtype=float)
        svals = np.asarray(shap_values.values, dtype=float).reshape(-1)

        # jitter in x for discrete thickness
        rng = np.random.default_rng(getattr(cfg, "random_seed", 42))
        xj = xvals + rng.normal(0, 0.02 * (np.nanmax(xvals) - np.nanmin(xvals) + 1e-9), size=xvals.shape)

        fig, ax = plt.subplots(figsize=(12, 7))
        set_dark_background(fig, ax)

        # global SHAP band
        order = np.argsort(xvals)
        ax.fill_between(
            xvals[order],
            np.quantile(svals, 0.10) * np.ones_like(xvals[order]),
            np.quantile(svals, 0.90) * np.ones_like(xvals[order]),
            color="#EAF0FF",
            alpha=0.06,
            label="Shap Band",
        )
        ax.scatter(xj, svals, s=62, alpha=0.78, color="#5BC0EB", edgecolor="#0B0F1A", linewidth=0.8, label="Shap Values")

        # smoothed central trend with band
        ax.plot(xvals[order], _smooth_curve(svals[order]), color="#FF9F1C", linewidth=3.0, label="Smoothed Trend")
        ax.fill_between(
            xvals[order],
            _smooth_curve(svals[order]) - np.nanstd(svals),
            _smooth_curve(svals[order]) + np.nanstd(svals),
            color="#FF9F1C",
            alpha=0.08,
            label="Trend Band",
        )

        ax.set_title(f"{t_title} Shap Dependence")
        ax.set_xlabel(labels.x_label)
        ax.set_ylabel("Shap Value")
        legend_outside_top_right(ax, ncol=1)
        polish_axes(ax)
        saved.append(savefig(fig, out_plots, f"shap_dependence__{target}", dpi=cfg.figure_dpi, fmt=cfg.figure_format))
    except Exception:
        pass

    # Custom Waterfall Style Plot for Representative Samples
    try:
        import matplotlib.pyplot as plt

        xvals = X_use.iloc[:, 0].to_numpy(dtype=float)
        svals = np.asarray(shap_values.values, dtype=float).reshape(-1)
        base = float(np.asarray(shap_values.base_values, dtype=float).reshape(-1)[0]) if hasattr(shap_values, "base_values") else 0.0
        idxs = [
            int(np.argmin(xvals)),
            int(np.argsort(np.abs(xvals - np.median(xvals)))[0]),
            int(np.argmax(xvals)),
        ]
        for k, idx in enumerate(idxs, start=1):
            contrib = float(svals[idx])
            pred = base + contrib
            fig, ax = plt.subplots(figsize=(11, 6))
            ax.barh(["Base Value"], [base], color="#5BC0EB", alpha=0.9, label="Base Value")
            ax.barh(["Feature Contribution"], [contrib], color="#FF9F1C", alpha=0.9, label="Feature Contribution")
            ax.axvline(pred, color="#EAF0FF", linewidth=2.2, linestyle="--", label="Predicted Value")
            ax.set_title(f"{t_title} Shap Waterfall")
            ax.set_xlabel("Model Output")
            legend_outside_top_right(ax, ncol=1)
            polish_axes(ax)
            saved.append(savefig(fig, out_plots, f"shap_waterfall__{target}__sample{k}", dpi=cfg.figure_dpi, fmt=cfg.figure_format))
    except Exception:
        pass

    return saved


def pdp_ice_1d(model: Any, X: pd.DataFrame, y_cols: list[str], out_plots: Path, cfg: object) -> list[Path]:
    saved: list[Path] = []
    ensure_dir(out_plots)
    import matplotlib.pyplot as plt

    # Manual PDP and ICE style plot using bootstrap refit curves as ICE lines
    x = X.iloc[:, 0].to_numpy(dtype=float)
    x_grid = np.linspace(float(np.min(x)), float(np.max(x)), 250)
    Xg = pd.DataFrame({X.columns[0]: x_grid})

    # Bootstrap ensemble curves
    band = _bootstrap_prediction_band(
        base_estimator=model,
        X=X,
        Y=pd.DataFrame(model.predict(X), columns=y_cols),
        X_grid=Xg,
        random_seed=getattr(cfg, "random_seed", 42),
        n_boot=120,
    )

    Yg = np.asarray(model.predict(Xg), dtype=float)
    for j, target in enumerate(y_cols):
        labels = get_display_labels(x_col=X.columns[0], y_cols=[target])
        t_title = labels.target_title_map.get(target, to_title_case(strip_parentheses_text(target)))
        y_label = labels.y_label_map.get(target, t_title)

        fig, ax = plt.subplots(figsize=(12, 7))
        set_dark_background(fig, ax)

        # ICE lines as bootstrapped response curves
        if band is not None and band.shape[2] > j:
            # draw a small subset of lines
            for k in range(min(25, band.shape[0])):
                ax.plot(x_grid, _smooth_curve(band[k, :, j]), color="#EAF0FF", alpha=0.10, linewidth=1.0)
            q10 = np.nanpercentile(band[:, :, j], 10, axis=0)
            q90 = np.nanpercentile(band[:, :, j], 90, axis=0)
            ax.fill_between(x_grid, q10, q90, color="#EAF0FF", alpha=0.10, label="ICE Band")

        ax.plot(x_grid, _smooth_curve(Yg[:, j]), color="#5BC0EB", linewidth=3.2, label="Partial Dependence")
        ax.set_title(f"{t_title} Partial Dependence And ICE")
        ax.set_xlabel(labels.x_label)
        ax.set_ylabel(y_label)
        legend_outside_top_right(ax, ncol=1)
        polish_axes(ax)
        saved.append(savefig(fig, out_plots, f"Partial Dependence And ICE__{target}", dpi=cfg.figure_dpi, fmt=cfg.figure_format))

    return saved


def _smooth_curve(y: np.ndarray) -> np.ndarray:
    y = np.asarray(y, dtype=float)
    sp = optional_import("scipy.signal")
    if sp is not None and y.size >= 9:
        try:
            # Savitzky Golay gives smooth curves without phase lag
            w = 11 if y.size >= 11 else (y.size // 2) * 2 + 1
            return sp.savgol_filter(y, window_length=w, polyorder=3)
        except Exception:
            pass
    # fallback moving average
    if y.size < 5:
        return y
    k = 5
    kernel = np.ones(k) / k
    return np.convolve(y, kernel, mode="same")


def _bootstrap_prediction_band(
    base_estimator: Any,
    X: pd.DataFrame,
    Y: pd.DataFrame,
    X_grid: pd.DataFrame,
    random_seed: int,
    n_boot: int = 160,
) -> np.ndarray | None:
    """
    Bootstrap refit band for 1D response curves.
    Returns array of shape (n_boot, n_grid, n_targets) or None on failure.
    """
    try:
        from sklearn.base import clone
    except Exception:
        return None

    rng = np.random.default_rng(random_seed)
    n = X.shape[0]
    preds = []
    for b in range(n_boot):
        idx = rng.integers(0, n, size=n)
        Xb = X.iloc[idx]
        Yb = Y.iloc[idx]
        try:
            est = clone(base_estimator)
            est.fit(Xb, Yb)
            pb = np.asarray(est.predict(X_grid), dtype=float)
            preds.append(pb)
        except Exception:
            continue

    if not preds:
        return None
    return np.stack(preds, axis=0)


def local_sensitivity_curve(
    model: Any,
    X: pd.DataFrame,
    Y: pd.DataFrame,
    y_cols: list[str],
    out_plots: Path,
    cfg: object,
    grid_size: int = 250,
) -> list[Path]:
    """
    Single-feature sensitivity-style interpretation:
    predict over a thickness grid; optionally include finite-difference slope curve.
    """
    import matplotlib.pyplot as plt

    ensure_dir(out_plots)
    x = X.iloc[:, 0].to_numpy(dtype=float)
    x_grid = np.linspace(float(np.min(x)), float(np.max(x)), grid_size)
    Xg = pd.DataFrame({X.columns[0]: x_grid})
    Yg = np.asarray(model.predict(Xg), dtype=float)

    # Uncertainty band via bootstrap refits
    band = _bootstrap_prediction_band(
        base_estimator=model,
        X=X,
        Y=Y,
        X_grid=Xg,
        random_seed=getattr(cfg, "random_seed", 42),
        n_boot=140,
    )

    saved: list[Path] = []
    for j, target in enumerate(y_cols):
        yg = Yg[:, j]
        yg_s = _smooth_curve(yg)
        dydx = np.gradient(yg_s, x_grid)
        dydx_s = _smooth_curve(dydx)

        labels = get_display_labels(x_col=X.columns[0], y_cols=[target])
        t_title = labels.target_title_map.get(target, to_title_case(strip_parentheses_text(target)))
        y_label = labels.y_label_map.get(target, t_title)

        fig, axes = plt.subplots(2, 1, figsize=(12, 9), sharex=True, gridspec_kw={"height_ratios": [2.3, 1.0]})
        ax = axes[0]
        axs = axes[1]
        set_dark_background(fig, [ax, axs])

        # Mandatory shaded uncertainty band
        if band is not None and band.shape[2] > j:
            q10 = np.nanpercentile(band[:, :, j], 10, axis=0)
            q90 = np.nanpercentile(band[:, :, j], 90, axis=0)
            ax.fill_between(x_grid, q10, q90, color="#EAF0FF", alpha=0.10, label="Uncertainty Band")

        ax.plot(x_grid, yg_s, linewidth=3.2, color="#5BC0EB", label="Predicted Response")
        ax.set_title(f"{t_title} Sensitivity Curve")
        ax.set_ylabel(y_label)
        legend_outside_top_right(ax, ncol=1)
        polish_axes(ax)

        # Slope panel with shaded magnitude band
        axs.fill_between(x_grid, 0, dydx_s, color="#D7263D", alpha=0.12, label="Slope Area")
        axs.plot(x_grid, dydx_s, linewidth=2.6, color="#D7263D", label="Local Slope")
        axs.set_xlabel(labels.x_label)
        axs.set_ylabel("Local Slope")
        legend_outside_top_right(axs, ncol=1)
        polish_axes(axs)

        saved.append(savefig(fig, out_plots, f"Sensitivity Curve__{target}", dpi=cfg.figure_dpi, fmt=cfg.figure_format))
    return saved


def run_explainability(
    model: Any,
    X: pd.DataFrame,
    Y: pd.DataFrame,
    y_cols: list[str],
    out_plots: Path,
    out_tables: Path,
    cfg: object,
) -> ExplainArtifacts:
    # Organize explainability plots into deeper hierarchy
    out_pdp = ensure_dir(out_plots / "PartialDependence")
    out_sens = ensure_dir(out_plots / "Sensitivity")
    out_shap = ensure_dir(out_plots / "Shap")
    ensure_dir(out_tables)

    # Permutation importance (single-feature, per-target)
    perm = None
    try:
        perm = permutation_importance_single_feature(model, X, Y, y_cols=y_cols, random_seed=getattr(cfg, "random_seed", 42), n_repeats=120)
        perm.to_csv(out_tables / "permutation_importance_single_feature.csv", index=False)
    except Exception:
        perm = None

    # PDP + ICE
    pdp_ice_1d(model, X, y_cols=y_cols, out_plots=out_pdp, cfg=cfg)

    # Sensitivity curve
    local_sensitivity_curve(model, X, Y, y_cols=y_cols, out_plots=out_sens, cfg=cfg)

    # SHAP outputs must be generated per target from single-output fits
    try:
        from sklearn.base import clone

        for t in y_cols:
            try:
                est_t = clone(model)
                est_t.fit(X, Y[t])
                shap_explain_1d_single_output(est_t, X, t, out_shap, cfg)
            except Exception:
                continue
    except Exception:
        pass

    return ExplainArtifacts(permutation_importance=perm)

