# PERO Summary Report: Al₂O₃ thickness → multi-output response

## Notation

Let $x \in \mathbb{R}_{\ge 0}$ denote the single engineered input (Al₂O₃ thickness, nm), stored in the dataset as the column `Al2O3 Thickness_nm`. Targets form $\mathbf{y} = (y_1,\dots,y_4)^\top$ over the four electrochemical metrics named below. Each fitted model implements a map $\hat{\mathbf{f}} : x \mapsto \widehat{\mathbf{y}}$ trained on the full tabulated sample; every scalar error metric is therefore **in-sample** unless stated otherwise.

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
| Extra Trees | 36.502096949891055 | 56.463637279027225 | 0.31150797874796066 | 0.29745712117138845 | 43.96871790144956 | 1 |
| Decision Tree | 36.50209694989107 | 56.463637279027225 | 0.31150797874796066 | 0.29745712117138845 | 43.96871790144958 | 2 |
| Gaussian Process Regression | 36.50211144577678 | 56.46363727973788 | 0.31150797873020625 | 0.29745712115327166 | 43.96879424143795 | 3 |
| Gradient Boosting | 36.62474727363456 | 56.46469020353801 | 0.31147978713009894 | 0.29742835421438674 | 44.172762381032854 | 4 |
| Extreme Gradient Boosting | 36.68221718881645 | 56.47065577776298 | 0.311307091678354 | 0.2972521343656674 | 44.06025933190316 | 5 |
| Categorical Boosting | 37.077481746004295 | 56.4823468839188 | 0.31092460676791145 | 0.296861843640726 | 45.0521131016635 | 6 |
| Random Forest | 40.12439201168747 | 57.226942920738146 | 0.2767615784138001 | 0.26200161062632665 | 52.487483531127566 | 7 |
| Bagging Regressor | 40.26839203969183 | 57.305889466292854 | 0.2697306555574985 | 0.2548271995484679 | 52.08331988037873 | 8 |
| Adaptive Boosting | 41.376324788358616 | 58.615520863839905 | 0.24136180161344056 | 0.22587938940146995 | 53.47012151600998 | 9 |
| Polynomial Regression Degree 3 | 45.93310218664039 | 61.46651043144696 | 0.12534423574049097 | 0.06951514440477766 | 75.84562028343396 | 10 |
| Polynomial Ridge Degree 3 | 45.83368966291799 | 61.738591269270614 | 0.11700643349149198 | 0.060645142012225484 | 77.71204418012663 | 11 |
| Polynomial Regression Degree 2 | 47.58581699448067 | 62.82814994632612 | 0.08167729649806676 | 0.04341385051881955 | 82.03919656927027 | 12 |
| Polynomial Ridge Degree 2 | 47.36162114757483 | 62.84394243278399 | 0.08140270925934742 | 0.043127822145153594 | 81.38673994146862 | 13 |
| Linear Regression | 47.88620327402283 | 63.48626724091056 | 0.06333200850025808 | 0.04421633520434498 | 84.11703649434362 | 14 |
| Lasso Regression | 47.8862242804854 | 63.48626725895862 | 0.06333200652419671 | 0.044216333187955814 | 84.11720260021775 | 15 |

- **Best overall model (by overall mean RMSE)**: `Extra Trees`

### Best model per target (by RMSE)
| target | best_model_by_rmse | RMSE | R2 |
| --- | --- | --- | --- |
| Rct_initial_ohm | Decision Tree | 117.90478920480369 | 0.24296881457168462 |
| ICE_percent | Gaussian Process Regression | 12.617473273515825 | 0.31799435914838015 |
| Initial Reversible Capacity_mAh_g at 0.1C | Decision Tree | 81.96072216747183 | 0.3041163615888186 |
| Highest Capacity Retention_percent | Decision Tree | 13.37156447030198 | 0.3809523796846417 |

## Scientific interpretation (1D thickness-response)

With $p=1$, estimator flexibility governs how $\mathbb{E}[Y_j \mid x]$ is approximated: **affine**, **smooth nonlinear** ($\hat{y}_j \in C^k$ for low $k$), or **threshold / cohort-segmented** behavior at the discrete support of $x$. In-sample $R^2$ can rise via interpolation of thickness cohorts; the decisive diagnostic is residual structure **vs.** $x$ and the plausibility of $\mathrm{d}\hat{y}_j/\mathrm{d}x$ on the nm axis.

Consult `outputs/eda/plots/` and `outputs/models/diagnostics_plots/` for overlap-aware scatter, parity lines, and residual sweeps keyed to thickness.

## Metric definitions (in-sample)

Residuals $\hat{\varepsilon}_{ij} = y_{ij} - \hat{y}_{ij}$. For each target $j$:

$$
\mathrm{MAE}_j = \frac{1}{n}\sum_{i=1}^{n}\bigl|\hat{\varepsilon}_{ij}\bigr|,
\qquad
\mathrm{RMSE}_j = \sqrt{\frac{1}{n}\sum_{i=1}^{n}\hat{\varepsilon}_{ij}^{2}},
\qquad
R^{2}_j = 1 - \frac{\sum_i \hat{\varepsilon}_{ij}^{2}}{\sum_i (y_{ij}-\bar{y}_j)^{2}}.
$$
