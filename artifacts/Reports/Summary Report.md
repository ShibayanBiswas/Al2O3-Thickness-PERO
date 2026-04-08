# PERO Summary Report: Al2O3 thickness → multi-output response

## Data integrity snapshot
- **Feature (only input)**: `Al2O3 Thickness_nm`
- **Targets**:
  - `Rct_initial_ohm`
  - `ICE_percent`
  - `Initial Reversible Capacity_mAh_g at 0.1C`
  - `Highest Capacity Retention_percent`

### Thickness discreteness & concentration
| Al2O3 Thickness_nm | count | fraction |
| --- | --- | --- |
| 0.0 | 36 | 0.7058823529411765 |
| 0.2 | 1 | 0.0196078431372549 |
| 0.5 | 1 | 0.0196078431372549 |
| 1.0 | 1 | 0.0196078431372549 |
| 1.1 | 1 | 0.0196078431372549 |
| 2.0 | 1 | 0.0196078431372549 |
| 2.1 | 1 | 0.0196078431372549 |
| 3.1 | 1 | 0.0196078431372549 |
| 5.0 | 1 | 0.0196078431372549 |
| 10.0 | 1 | 0.0196078431372549 |

- **Zero-thickness group**: 36 rows (70.6% of dataset)

## EDA: thickness ↔ target association (1D setting)
Correlation is only a **first-pass** indicator in a highly discrete single-feature dataset; nonlinearity/thresholds can matter more than a single coefficient.

### Pearson & Spearman (thickness vs each target)
| target | pearson_r | spearman_r |
| --- | --- | --- |
| Highest Capacity Retention_percent | -0.0145445186489114 | 0.0724287983840943 |
| ICE_percent | -0.2042295402886098 | 0.153416466508575 |
| Initial Reversible Capacity_mAh_g at 0.1C | -0.3972572115877752 | -0.0784803650014886 |
| Rct_initial_ohm | -0.2315026861470775 | -0.6142125579852413 |

### 0.0 nm vs non-zero thickness comparison
This contrasts the large `0.0 nm` cluster against the pooled non-zero thicknesses (diagnostic; not causal).

| target | n_zero | n_nonzero | zero_mean | nonzero_mean | zero_median | nonzero_median | delta_mean_nonzero_minus_zero | delta_median_nonzero_minus_zero |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Rct_initial_ohm | 36 | 15 | 177.66944444444445 | 38.81466666666667 | 125.5 | 25.0 | -138.85477777777777 | -100.5 |
| ICE_percent | 36 | 15 | 58.67222222222222 | 63.24666666666667 | 62.1 | 71.2 | 4.5744444444444525 | 9.1 |
| Initial Reversible Capacity_mAh_g at 0.1C | 36 | 15 | 257.09444444444443 | 232.79333333333332 | 278.5 | 269.0 | -24.301111111111084 | -9.5 |
| Highest Capacity Retention_percent | 36 | 15 | 77.08888888888889 | 78.45333333333335 | 80.0 | 82.0 | 1.3644444444444588 | 2.0 |

## Modeling (in-sample / full-data fit by requirement)
- No normal train/test split was used; final models are fitted on **all 51 rows**.
- Metrics and residual diagnostics are **in-sample** and should be read as *fit/diagnostic* rather than generalization guarantees.

### Overall model leaderboard (mean across targets)
| model | OVERALL_MAE | OVERALL_RMSE | OVERALL_R2 | OVERALL_Adj_R2 | OVERALL_MAPE_percent | rank_by_overall_rmse |
| --- | --- | --- | --- | --- | --- | --- |
| Extra Trees | 36.502096949891055 | 56.463637279027225 | 0.3115079787479606 | 0.2974571211713884 | 43.96871790144956 | 1 |
| Decision Tree | 36.50209694989107 | 56.463637279027225 | 0.3115079787479606 | 0.2974571211713884 | 43.96871790144958 | 2 |
| Gradient Boosting | 36.62474727363456 | 56.46469020353801 | 0.3114797871300989 | 0.2974283542143867 | 44.17276238103285 | 3 |
| Random Forest | 40.12439201168747 | 57.22694292073815 | 0.2767615784138001 | 0.2620016106263266 | 52.487483531127566 | 4 |
| Bagging Regressor | 40.26839203969183 | 57.30588946629285 | 0.2697306555574985 | 0.2548271995484679 | 52.08331988037873 | 5 |
| Adaptive Boosting | 41.376324788358616 | 58.61552086383991 | 0.2413618016134405 | 0.2258793894014699 | 53.47012151600998 | 6 |
| Polynomial Regression Degree 3 | 45.93310218664039 | 61.46651043144696 | 0.1253442357404909 | 0.0695151444047776 | 75.84562028343396 | 7 |
| Polynomial Ridge Degree 3 | 45.83368966291799 | 61.73859126927061 | 0.1170064334914919 | 0.0606451420122254 | 77.71204418012663 | 8 |
| Polynomial Regression Degree 2 | 47.58581699448067 | 62.82814994632612 | 0.0816772964980667 | 0.0434138505188195 | 82.03919656927027 | 9 |
| Polynomial Ridge Degree 2 | 47.36162114757483 | 62.84394243278399 | 0.0814027092593474 | 0.0431278221451535 | 81.38673994146862 | 10 |
| Linear Regression | 47.88620327402283 | 63.48626724091056 | 0.063332008500258 | 0.0442163352043449 | 84.11703649434362 | 11 |
| Lasso Regression | 47.8862242804854 | 63.48626725895862 | 0.0633320065241967 | 0.0442163331879558 | 84.11720260021775 | 12 |
| Elastic Net Regression | 47.88695737276996 | 63.4862680821951 | 0.0633319896952182 | 0.0442163160155288 | 84.12050988761703 | 13 |
| Ridge Regression | 47.91481760345432 | 63.48742364228925 | 0.0633085868994814 | 0.0441924356117157 | 84.2475009956124 | 14 |
| K Nearest Neighbors Five | 45.39443137254902 | 66.13774847857172 | 0.0435126642333794 | 0.0239925145238565 | 50.12863096442569 | 15 |

- **Best overall model (by overall mean RMSE)**: `Extra Trees`

### Best model per target (by RMSE)
| target | best_model_by_rmse | RMSE | R2 |
| --- | --- | --- | --- |
| Rct_initial_ohm | Decision Tree | 117.90478920480368 | 0.2429688145716846 |
| ICE_percent | Decision Tree | 12.617473273531386 | 0.3179943591466978 |
| Initial Reversible Capacity_mAh_g at 0.1C | Decision Tree | 81.96072216747183 | 0.3041163615888186 |
| Highest Capacity Retention_percent | Decision Tree | 13.37156447030198 | 0.3809523796846417 |

## Scientific interpretation (1D thickness-response)
Because the feature space is one-dimensional, model flexibility mainly controls whether the relationship is treated as **linear**, **smoothly nonlinear**, or **piecewise/threshold-like**.
Use the exported plots in `outputs/eda/plots/` and `outputs/models/diagnostics_plots/` to judge whether residual structure remains versus thickness (a sign the chosen model family is too rigid).
