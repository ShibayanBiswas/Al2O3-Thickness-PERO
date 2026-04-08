from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

from .utils import TargetMetrics, adjusted_r2, safe_mape


@dataclass(frozen=True)
class ModelEvalResult:
    model_name: str
    y_cols: list[str]
    y_true: np.ndarray
    y_pred: np.ndarray
    per_target_metrics: dict[str, TargetMetrics]
    metrics_table: pd.DataFrame


def compute_metrics_per_target(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    y_cols: list[str],
    n_features_effective: int,
) -> tuple[dict[str, TargetMetrics], pd.DataFrame]:
    from sklearn.metrics import (
        explained_variance_score,
        mean_absolute_error,
        mean_squared_error,
        median_absolute_error,
        r2_score,
    )

    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)
    n = y_true.shape[0]

    per: dict[str, TargetMetrics] = {}
    rows: list[dict[str, object]] = []
    for j, name in enumerate(y_cols):
        yt = y_true[:, j]
        yp = y_pred[:, j]
        mae = float(mean_absolute_error(yt, yp))
        mse = float(mean_squared_error(yt, yp))
        rmse = float(np.sqrt(mse))
        r2 = float(r2_score(yt, yp))
        adj = float(adjusted_r2(r2, n=n, p=n_features_effective))
        mape = float(safe_mape(yt, yp))
        medae = float(median_absolute_error(yt, yp))
        ev = float(explained_variance_score(yt, yp))
        per[name] = TargetMetrics(mae=mae, mse=mse, rmse=rmse, r2=r2, adj_r2=adj, mape_percent=mape, medae=medae, explained_var=ev)
        rows.append(
            {
                "target": name,
                "MAE": mae,
                "MSE": mse,
                "RMSE": rmse,
                "R2": r2,
                "Adj_R2": adj,
                "MAPE_percent": mape,
                "MedianAE": medae,
                "ExplainedVariance": ev,
            }
        )

    df = pd.DataFrame(rows)
    return per, df


def summarize_overall(metrics_table: pd.DataFrame) -> pd.DataFrame:
    # Simple overall row: mean across targets of each metric (for comparability)
    out = metrics_table.copy()
    overall = {"target": "OVERALL_MEAN"}
    for c in out.columns:
        if c == "target":
            continue
        overall[c] = float(out[c].mean())
    return pd.concat([out, pd.DataFrame([overall])], ignore_index=True)


def rank_models(model_tables: list[pd.DataFrame], model_names: list[str]) -> pd.DataFrame:
    """
    Combine model metric tables (with OVERALL_MEAN row) into a wide comparison table.
    Ranks primarily by OVERALL_MEAN RMSE (lower is better) and OVERALL_MEAN R2 (higher is better).
    """
    rows = []
    for name, tbl in zip(model_names, model_tables, strict=True):
        overall = tbl.loc[tbl["target"] == "OVERALL_MEAN"].iloc[0].to_dict()
        rows.append(
            {
                "model": name,
                "OVERALL_MAE": overall["MAE"],
                "OVERALL_RMSE": overall["RMSE"],
                "OVERALL_R2": overall["R2"],
                "OVERALL_Adj_R2": overall["Adj_R2"],
                "OVERALL_MAPE_percent": overall["MAPE_percent"],
            }
        )
    comp = pd.DataFrame(rows)
    comp = comp.sort_values(["OVERALL_RMSE", "OVERALL_MAE", "OVERALL_R2"], ascending=[True, True, False]).reset_index(drop=True)
    comp["rank_by_overall_rmse"] = np.arange(1, comp.shape[0] + 1)
    return comp

