from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class TunedModelResult:
    name: str
    estimator: Any
    best_params: dict[str, Any]
    cv_summary: pd.DataFrame


def _rmse(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)
    err = y_true - y_pred
    return float(np.sqrt(np.mean(err * err)))


def _multioutput_r2_uniform(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    from sklearn.metrics import r2_score

    return float(r2_score(y_true, y_pred, multioutput="uniform_average"))


def build_cv_strategies(n: int, random_seed: int) -> dict[str, Any]:
    """
    Multiple CV techniques (small-n friendly).
    """
    from sklearn.model_selection import KFold, RepeatedKFold, ShuffleSplit

    k = int(max(2, min(5, n)))
    return {
        f"KFold({k})": KFold(n_splits=k, shuffle=True, random_state=random_seed),
        f"RepeatedKFold({k}x5)": RepeatedKFold(n_splits=k, n_repeats=5, random_state=random_seed),
        "ShuffleSplit(15x20%)": ShuffleSplit(n_splits=15, test_size=0.2, random_state=random_seed),
    }


def cv_r2_table(estimator: Any, X, Y, *, strategies: dict[str, Any]) -> pd.DataFrame:
    """
    Return a compact table of R2 across multiple CV strategies.
    Uses fold-level per-target R2 (then averages across targets), skipping folds with <2 test samples.
    """
    from sklearn.base import clone
    from sklearn.metrics import r2_score

    rows: list[dict[str, Any]] = []
    for name, cv in strategies.items():
        fold_scores: list[float] = []
        for tr_idx, te_idx in cv.split(X, Y):
            te_idx = np.asarray(te_idx)
            if te_idx.size < 2:
                continue
            est = clone(estimator)
            est.fit(X.iloc[tr_idx], Y.iloc[tr_idx])
            pred = np.asarray(est.predict(X.iloc[te_idx]), dtype=float)
            yt = np.asarray(Y.iloc[te_idx].to_numpy(dtype=float), dtype=float)
            # Per-target R2; average across targets.
            per_t = []
            for j in range(yt.shape[1]):
                try:
                    per_t.append(float(r2_score(yt[:, j], pred[:, j])))
                except Exception:
                    continue
            if per_t:
                fold_scores.append(float(np.mean(per_t)))

        scores = np.asarray(fold_scores, dtype=float)
        rows.append(
            {
                "cv_scheme": name,
                "R2_mean": float(np.nanmean(scores)) if scores.size else float("nan"),
                "R2_std": float(np.nanstd(scores, ddof=1)) if scores.size >= 2 else 0.0,
                "folds": int(scores.size),
            }
        )
    return pd.DataFrame(rows)


def tune_estimator(
    name: str,
    estimator: Any,
    param_distributions: dict[str, Any] | None,
    X,
    Y,
    *,
    random_seed: int,
    cv_primary: Any,
    n_iter: int = 25,
) -> tuple[Any, dict[str, Any], float]:
    """
    Randomized hyperparameter tuning for a (potentially multioutput) regressor.
    Returns (best_estimator, best_params, best_cv_r2_mean).
    """
    if not param_distributions:
        # No tuning for this estimator.
        return estimator, {}, float("nan")

    from sklearn.model_selection import RandomizedSearchCV
    from sklearn.metrics import make_scorer

    scorer = make_scorer(_multioutput_r2_uniform, greater_is_better=True)

    search = RandomizedSearchCV(
        estimator=estimator,
        param_distributions=param_distributions,
        n_iter=int(max(5, n_iter)),
        scoring=scorer,
        cv=cv_primary,
        random_state=random_seed,
        n_jobs=None,
        refit=True,
    )
    search.fit(X, Y)
    best = search.best_estimator_
    best_params = dict(search.best_params_ or {})
    best_score = float(search.best_score_) if search.best_score_ is not None else float("nan")
    return best, best_params, best_score

