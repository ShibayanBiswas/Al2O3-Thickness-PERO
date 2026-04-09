# Modeling Tables Index

Machine-readable **in-sample** scores for every fitted estimator. Produced in ``run_all.py``; ``postprocess.py`` can regenerate the aggregate files from ``metrics__*.csv``.

---

## File inventory

| File | Description |
| --- | --- |
| ``metrics__<ModelSafe>.csv`` | One row per target plus a synthetic row ``target == OVERALL_MEAN`` (mean of per-target metrics). ``<ModelSafe>`` matches ``safe_filename(model.name)``. |
| ``model_comparison_overall.csv`` | One row per successfully fit model; sorted by overall RMSE. |
| ``best_model_per_target.csv`` | Argmin of RMSE over models, separately for each target column. |
| ``all_model_metrics.xlsx`` | Workbook: sheets ``model_comparison_overall``, ``best_model_per_target``, and ``metrics__<ModelName>`` per model. Sheet names pass through ``safe_sheet_name()`` in ``src/utils.py`` (Excel max 31 characters; ``: \\ / ? * [ ]`` removed). |

---

## Columns: ``metrics__*.csv`` (from ``compute_metrics_per_target`` + ``summarize_overall``)

| Column | Meaning |
| --- | --- |
| ``target`` | Electrochemical column name, or ``OVERALL_MEAN`` for the pooled row |
| ``MAE``, ``MSE``, ``RMSE`` | Standard sklearn-style errors |
| ``R2``, ``Adj_R2`` | Coefficient of determination and adjusted form ($p$ from the model spec) |
| ``MAPE_percent`` | Percent MAPE where defined (safe for zeros via ``safe_mape``) |
| ``MedianAE`` | Median absolute error |
| ``ExplainedVariance`` | Explained variance score |

---

## Metric definitions (math; matches ``src/model_eval.py``)

For each target $j$ with observations $y_{ij}$ and predictions $\hat y_{ij}$, define residuals:

$$
\hat\varepsilon_{ij} = y_{ij}-\hat y_{ij}.
$$

Then

$$
\mathrm{MAE}_j = \frac{1}{n}\sum_i |\hat\varepsilon_{ij}|,\qquad
\mathrm{MSE}_j = \frac{1}{n}\sum_i \hat\varepsilon_{ij}^2,\qquad
\mathrm{RMSE}_j = \sqrt{\mathrm{MSE}_j}.
$$

Coefficient of determination (in-sample):

$$
R^2_j = 1 - \frac{\sum_i \hat\varepsilon_{ij}^2}{\sum_i (y_{ij}-\bar y_j)^2}.
$$

Adjusted $R^2$ (with effective feature count $p$ used by the model spec):

$$
R^2_{j,\mathrm{adj}} = 1 - (1-R^2_j)\frac{n-1}{n-p-1}.
$$

MAPE (as implemented via ``safe_mape`` with a stabilizer $\varepsilon$):

$$
\mathrm{MAPE}_j = 100\cdot \frac{1}{n}\sum_i \frac{|\hat\varepsilon_{ij}|}{\max(|y_{ij}|,\varepsilon)}.
$$

Explained variance score:

$$
\mathrm{EV}_j = 1 - \frac{\mathrm{Var}(y_j-\hat y_j)}{\mathrm{Var}(y_j)}.
$$

---

## Columns: ``model_comparison_overall.csv`` (from ``rank_models``)

| Column | Meaning |
| --- | --- |
| ``model`` | Estimator display name |
| ``OVERALL_MAE``, ``OVERALL_RMSE``, ``OVERALL_R2``, ``OVERALL_Adj_R2``, ``OVERALL_MAPE_percent`` | Taken from the ``OVERALL_MEAN`` row of each model's metrics table |
| ``rank_by_overall_rmse`` | 1 = best (lowest overall RMSE) |

---

## Columns: ``best_model_per_target.csv``

| Column | Meaning |
| --- | --- |
| ``target`` | Raw target column name |
| ``best_model_by_rmse`` | Model name achieving lowest RMSE on that target |
| ``RMSE``, ``R2`` | In-sample scores for that best model on that target |

---

## Equations (residual form)

$$
\hat\varepsilon_{ij} = y_{ij}-\hat{y}_{ij},\qquad
\mathrm{RMSE}_j=\sqrt{\frac{1}{n}\sum_{i=1}^{n}\hat\varepsilon_{ij}^2}.
$$

Pair tables with ``../diagnostics_plots/`` for thickness-structured residuals.

---

## Interpreting the numbers (quick reference)

| Metric | Plain-language meaning | Typical pitfall |
| --- | --- | --- |
| MAE | Average absolute error in the same units as $Y_j$ | Can hide occasional large errors |
| RMSE | Penalises **large** errors more than MAE | Dominated by outliers if present |
| $R^2$ | Fraction of variance of $Y_j$ explained **in sample** | Can be high with cohort interpolation |
| MAPE | Relative error notion (percent) | Unstable if $y$ crosses zero |
| MedianAE | Robust central error | Does not summarise tail risk |

The **``OVERALL_MEAN``** row inside each ``metrics__*.csv`` averages these quantities across the four targets so you can rank **multi-output** models with one line per model in ``model_comparison_overall.csv``.
