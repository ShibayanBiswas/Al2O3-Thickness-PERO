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

    When ``param_distributions`` is empty (nothing to tune), we still report
    ``best_cv_r2_mean`` as the mean out-of-fold R² on the primary CV splitter,
    so leaderboard CSVs stay comparable to tuned models.
    """
    from sklearn.metrics import make_scorer

    scorer = make_scorer(_multioutput_r2_uniform, greater_is_better=True)

    if not param_distributions:
        from sklearn.model_selection import cross_val_score

        try:
            scores = cross_val_score(
                estimator,
                X,
                Y,
                scoring=scorer,
                cv=cv_primary,
                n_jobs=None,
                error_score=np.nan,
            )
            scores = np.asarray(scores, dtype=float)
            mean_score = float(np.nanmean(scores)) if np.any(np.isfinite(scores)) else float("nan")
        except Exception:
            mean_score = float("nan")
        return estimator, {}, mean_score

    from sklearn.model_selection import RandomizedSearchCV

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

