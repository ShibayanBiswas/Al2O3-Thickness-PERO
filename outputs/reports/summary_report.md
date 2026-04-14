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
| 0.0 | 4 | 0.2857142857142857 |
| 0.2 | 1 | 0.07142857142857142 |
| 0.5 | 1 | 0.07142857142857142 |
| 1.0 | 1 | 0.07142857142857142 |
| 1.1 | 1 | 0.07142857142857142 |
| 2.0 | 1 | 0.07142857142857142 |
| 2.1 | 1 | 0.07142857142857142 |
| 3.1 | 1 | 0.07142857142857142 |
| 5.0 | 1 | 0.07142857142857142 |
| 12.0 | 1 | 0.07142857142857142 |

- **Zero-thickness group**: 4 rows (28.6% of dataset)

## EDA: thickness ↔ target association (1D setting)
Correlation is only a **first-pass** indicator in a highly discrete single-feature dataset; nonlinearity/thresholds can matter more than a single coefficient.

### Pearson & Spearman (thickness vs each target)
| target | pearson_r | spearman_r |
| --- | --- | --- |
| Highest Capacity Retention_percent | -0.758929879659332 | -0.1133403298659407 |
| ICE_percent | -0.1440046389217678 | -0.0555589852284023 |
| Initial Reversible Capacity_mAh_g at 0.1C | 0.1036236589396839 | 0.0444471881827218 |
| Rct_initial_ohm | 0.8491310216716105 | 0.0688931416832188 |

### 0.0 nm vs non-zero thickness comparison
This contrasts the large `0.0 nm` cluster against the pooled non-zero thicknesses (diagnostic; not causal).

| target | n_zero | n_nonzero | zero_mean | nonzero_mean | zero_median | nonzero_median | delta_mean_nonzero_minus_zero | delta_median_nonzero_minus_zero |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Rct_initial_ohm | 4 | 10 | 35.525 | 46.690000000000005 | 32.91 | 35.75 | 11.165000000000006 | 2.8400000000000034 |
| ICE_percent | 4 | 10 | 71.25 | 65.91 | 70.5 | 71.9 | -5.340000000000003 | 1.4000000000000057 |
| Initial Reversible Capacity_mAh_g at 0.1C | 4 | 10 | 278.975 | 256.56 | 281.0 | 269.5 | -22.41500000000002 | -11.5 |
| Highest Capacity Retention_percent | 4 | 10 | 76.7 | 75.31 | 79.9 | 81.0 | -1.3900000000000006 | 1.0999999999999943 |

## Modeling (in-sample / full-data fit by requirement)
- No normal train/test split was used; final models are fitted on **all 51 rows**.
- Metrics and residual diagnostics are **in-sample** and should be read as *fit/diagnostic* rather than generalization guarantees.

### Overall model leaderboard (mean across targets)
| model | OVERALL_MAE | OVERALL_RMSE | OVERALL_R2 | OVERALL_Adj_R2 | OVERALL_MAPE_percent | rank_by_overall_rmse |
| --- | --- | --- | --- | --- | --- | --- |
| Gradient Boosting | 3.352380071380857 | 7.490347085127204 | 0.9186481118372842 | 0.9118687878237246 | 10.332481357959841 | 1 |
| Gaussian Process Regression | 4.52130048637139 | 7.8487400041662125 | 0.9143535482814524 | 0.9072163439715735 | 17.814132034858847 | 2 |
| Adaptive Boosting | 4.994553571428572 | 8.350237732030237 | 0.9086560452830199 | 0.901044049056605 | 10.731743407306803 | 3 |
| Extra Trees | 7.27885211640207 | 9.598162906480946 | 0.8870326089380014 | 0.8776186596828348 | 18.616055786154618 | 4 |
| Decision Tree | 9.405833333333334 | 11.90708057405086 | 0.8395422978097675 | 0.8261708226272482 | 20.840902613671428 | 5 |
| Bagging Regressor | 9.945483482142858 | 12.894284565366252 | 0.81358447085416 | 0.79804984342534 | 20.890008682070153 | 6 |
| Random Forest | 10.649431095650364 | 14.201912552475958 | 0.7741271154704554 | 0.7553043750929934 | 22.245285017612442 | 7 |
| Polynomial Regression Degree 3 | 14.48011672793636 | 20.33457760275129 | 0.4762210209648448 | 0.3190873272542982 | 25.583960660561225 | 8 |
| Support Vector Regression | 12.311867421062232 | 21.76376782966211 | 0.4112792158705586 | 0.3622191505264385 | 25.708182593978005 | 9 |
| Polynomial Regression Degree 2 | 17.075345427530564 | 22.500550285619056 | 0.40194725185028046 | 0.29321038855033144 | 33.898668417147974 | 10 |
| Polynomial Ridge Degree 2 | 17.07526361925966 | 22.500550287433395 | 0.40194725175714385 | 0.2932103884402609 | 33.89861337410156 | 11 |
| Linear Regression | 17.586375268465023 | 24.02370698363448 | 0.3321183132319596 | 0.2764615060012896 | 37.86706591949187 | 12 |
| Lasso Regression | 17.58637565411988 | 24.02370698363722 | 0.33211831323172203 | 0.27646150600103225 | 37.86706986545299 | 13 |
| Elastic Net Regression | 17.586383426293246 | 24.023706983966655 | 0.33211831321994134 | 0.27646150598826985 | 37.86711074396536 | 14 |
| Ridge Regression | 17.58638523634016 | 24.023706984116924 | 0.33211831321501495 | 0.2764615059829329 | 37.86711925484783 | 15 |

- **Best overall model (by overall mean RMSE)**: `K Nearest Neighbors Three`

### Best model per target (by RMSE)
| target | best_model_by_rmse | RMSE | R2 |
| --- | --- | --- | --- |
| Rct_initial_ohm | Adaptive Boosting | 11.83201365042356 | 0.9168218829125843 |
| ICE_percent | Gaussian Process Regression | 2.2179688234524155 | 0.9691202865725025 |
| Initial Reversible Capacity_mAh_g at 0.1C | Gaussian Process Regression | 6.34826935136047 | 0.9827338574026928 |
| Highest Capacity Retention_percent | Gaussian Process Regression | 9.112072159657277 | 0.8173461621033391 |

## Scientific interpretation (1D thickness-response)

With $p=1$, estimator flexibility governs how $\mathbb{E}[Y_j \mid x]$ is approximated: **affine**, **smooth nonlinear** ($\hat{y}_j \in C^k$ for low $k$), or **threshold / cohort-segmented** behavior at the discrete support of $x$. In-sample $R^2$ can rise via interpolation of thickness cohorts; the decisive diagnostic is residual structure **vs.** $x$ and the plausibility of $\mathrm{d}\hat{y}_j/\mathrm{d}x$ on the nm axis.

Consult `outputs/eda/plots/` and `outputs/models/diagnostics_plots/` for overlap-aware scatter, parity lines, and residual sweeps keyed to thickness.

## Metric definitions (in-sample)

Residuals $\hat{\varepsilon}_{ij} = y_{ij} - \hat{y}_{ij}$. For each target $j$:

$$
\mathrm{MAE}_j = \frac{1}{n}\sum_{i=1}^{n}\bigl|\hat{\varepsilon}_{ij}\bigr|,\qquad \mathrm{RMSE}_j = \sqrt{\frac{1}{n}\sum_{i=1}^{n}\hat{\varepsilon}_{ij}^{2}},\qquad R^{2}_j = 1 - \frac{\sum_i \hat{\varepsilon}_{ij}^{2}}{\sum_i (y_{ij}-\bar{y}_j)^{2}}.
$$
