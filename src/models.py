from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd

from .utils import optional_import


@dataclass(frozen=True)
class ModelSpec:
    name: str
    estimator: Any
    n_features_effective: int  # used only for adjusted R^2 reporting


def build_model_suite(random_seed: int) -> list[ModelSpec]:
    """
    Build a broad suite of single-feature regressors for multi-output regression.
    Models that don't support multi-output natively should already be wrapped.
    """
    from sklearn.compose import TransformedTargetRegressor
    from sklearn.ensemble import (
        AdaBoostRegressor,
        BaggingRegressor,
        ExtraTreesRegressor,
        GradientBoostingRegressor,
        RandomForestRegressor,
    )
    from sklearn.gaussian_process import GaussianProcessRegressor
    from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C
    from sklearn.linear_model import (
        ElasticNet,
        Lasso,
        LinearRegression,
        Ridge,
        SGDRegressor,
    )
    from sklearn.multioutput import MultiOutputRegressor
    from sklearn.neighbors import KNeighborsRegressor
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import PolynomialFeatures, StandardScaler
    from sklearn.svm import SVR
    from sklearn.tree import DecisionTreeRegressor

    # HistGradientBoostingRegressor can be faster/more stable for certain patterns
    try:
        from sklearn.ensemble import HistGradientBoostingRegressor
    except Exception:
        HistGradientBoostingRegressor = None  # type: ignore

    suite: list[ModelSpec] = []

    def with_scaler(est):
        # User requirement: apply Standard Scaler before modeling
        return Pipeline(steps=[("scaler", StandardScaler()), ("model", est)])

    # LINEAR / REGULARIZED
    suite.append(ModelSpec("Linear Regression", with_scaler(LinearRegression()), n_features_effective=1))
    suite.append(ModelSpec("Ridge Regression", with_scaler(Ridge(alpha=1.0, random_state=random_seed)), n_features_effective=1))
    suite.append(ModelSpec("Lasso Regression", with_scaler(Lasso(alpha=0.001, random_state=random_seed, max_iter=50000)), n_features_effective=1))
    suite.append(
        ModelSpec(
            "Elastic Net Regression",
            with_scaler(ElasticNet(alpha=0.001, l1_ratio=0.5, random_state=random_seed, max_iter=50000)),
            n_features_effective=1,
        )
    )

    # Polynomial regression (engineered features derived only from thickness)
    for deg in (2, 3):
        suite.append(
            ModelSpec(
                f"Polynomial Regression Degree {deg}",
                Pipeline(
                    steps=[
                        ("scaler", StandardScaler()),
                        ("poly", PolynomialFeatures(degree=deg, include_bias=False)),
                        ("lin", LinearRegression()),
                    ]
                ),
                n_features_effective=deg,  # approx p for adj R^2 reporting (x, x^2, x^3)
            )
        )
        suite.append(
            ModelSpec(
                f"Polynomial Ridge Degree {deg}",
                Pipeline(
                    steps=[
                        ("scaler", StandardScaler()),
                        ("poly", PolynomialFeatures(degree=deg, include_bias=False)),
                        ("ridge", Ridge(alpha=1.0, random_state=random_seed)),
                    ]
                ),
                n_features_effective=deg,
            )
        )

    # SGDRegressor needs scaling; also not natively multi-output
    suite.append(
        ModelSpec(
            "Stochastic Gradient Regression",
            MultiOutputRegressor(
                Pipeline(
                    steps=[
                        ("scaler", StandardScaler()),
                        ("sgd", SGDRegressor(loss="huber", random_state=random_seed, max_iter=5000, tol=1e-4)),
                    ]
                )
            ),
            n_features_effective=1,
        )
    )

    # TREE-BASED
    suite.append(ModelSpec("Decision Tree", DecisionTreeRegressor(random_state=random_seed), n_features_effective=1))
    suite.append(
        ModelSpec(
            "Random Forest",
            RandomForestRegressor(
                n_estimators=240,
                random_state=random_seed,
                min_samples_leaf=1,
            ),
            n_features_effective=1,
        )
    )
    suite.append(
        ModelSpec(
            "Extra Trees",
            ExtraTreesRegressor(
                n_estimators=240,
                random_state=random_seed,
                min_samples_leaf=1,
            ),
            n_features_effective=1,
        )
    )

    # Gradient Boosting (single-feature is fine)
    suite.append(ModelSpec("Gradient Boosting", MultiOutputRegressor(GradientBoostingRegressor(random_state=random_seed)), n_features_effective=1))
    suite.append(ModelSpec("Adaptive Boosting", MultiOutputRegressor(AdaBoostRegressor(random_state=random_seed)), n_features_effective=1))

    if HistGradientBoostingRegressor is not None:
        suite.append(
            ModelSpec(
                "Histogram Gradient Boosting",
                MultiOutputRegressor(HistGradientBoostingRegressor(random_state=random_seed)),
                n_features_effective=1,
            )
        )

    # Bagging
    suite.append(ModelSpec("Bagging Regressor", MultiOutputRegressor(BaggingRegressor(random_state=random_seed)), n_features_effective=1))

    # KNN (can behave like local averaging on discrete x)
    suite.append(ModelSpec("K Nearest Neighbors Five", with_scaler(KNeighborsRegressor(n_neighbors=5)), n_features_effective=1))
    suite.append(ModelSpec("K Nearest Neighbors Three", with_scaler(KNeighborsRegressor(n_neighbors=3)), n_features_effective=1))

    # SVR (needs scaling; wrap for multi-output)
    suite.append(
        ModelSpec(
            "Support Vector Regression",
            MultiOutputRegressor(Pipeline(steps=[("scaler", StandardScaler()), ("svr", SVR(C=10.0, gamma="scale"))])),
            n_features_effective=1,
        )
    )

    # Gaussian Process (can overfit; keep simple kernel)
    try:
        kernel = C(1.0, (1e-2, 1e2)) * RBF(length_scale=5.0, length_scale_bounds=(1e-2, 1e3))
        gpr = GaussianProcessRegressor(kernel=kernel, random_state=random_seed, alpha=1e-6, normalize_y=True)
        suite.append(ModelSpec("Gaussian Process Regression", MultiOutputRegressor(gpr), n_features_effective=1))
    except Exception:
        pass

    # Optional: XGBoost / LightGBM / CatBoost (wrapped)
    xgb = optional_import("xgboost")
    if xgb is not None:
        try:
            suite.append(
                ModelSpec(
                    "Extreme Gradient Boosting",
                    MultiOutputRegressor(
                        xgb.XGBRegressor(
                            n_estimators=300,
                            learning_rate=0.06,
                            max_depth=3,
                            subsample=0.9,
                            colsample_bytree=1.0,
                            reg_lambda=1.0,
                            random_state=random_seed,
                            objective="reg:squarederror",
                        )
                    ),
                    n_features_effective=1,
                )
            )
        except Exception:
            pass

    lgbm = optional_import("lightgbm")
    if lgbm is not None:
        try:
            suite.append(
                ModelSpec(
                    "Light Gradient Boosting",
                    MultiOutputRegressor(
                        lgbm.LGBMRegressor(
                            n_estimators=400,
                            learning_rate=0.06,
                            num_leaves=15,
                            random_state=random_seed,
                        )
                    ),
                    n_features_effective=1,
                )
            )
        except Exception:
            pass

    cat = optional_import("catboost")
    if cat is not None:
        try:
            suite.append(
                ModelSpec(
                    "Categorical Boosting",
                    MultiOutputRegressor(
                        cat.CatBoostRegressor(
                            depth=4,
                            learning_rate=0.06,
                            iterations=450,
                            random_seed=random_seed,
                            verbose=False,
                            loss_function="RMSE",
                        )
                    ),
                    n_features_effective=1,
                )
            )
        except Exception:
            pass

    return suite


def fit_predict(model, X: pd.DataFrame, Y: pd.DataFrame) -> tuple[Any, np.ndarray]:
    fitted = model.fit(X, Y)
    pred = fitted.predict(X)
    pred = np.asarray(pred, dtype=float)
    return fitted, pred

