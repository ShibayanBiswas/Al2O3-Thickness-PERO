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
| 0.0 | 3 | 0.2727272727272727 |
| 0.2 | 1 | 0.09090909090909091 |
| 1.0 | 1 | 0.09090909090909091 |
| 1.1 | 1 | 0.09090909090909091 |
| 2.1 | 1 | 0.09090909090909091 |
| 3.1 | 1 | 0.09090909090909091 |
| 5.0 | 1 | 0.09090909090909091 |
| 12.0 | 1 | 0.09090909090909091 |
| 18.0 | 1 | 0.09090909090909091 |

- **Zero-thickness group**: 3 rows (27.3% of dataset)

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
| Gradient Boosting | 3.1687329063870795 | 6.525074842751619 | 0.9455637350402234 | 0.9395152611558036 | 9.736368691795033 | 1 |
| Gaussian Process Regression | 3.929159497152678 | 6.822468374053738 | 0.9420084422883457 | 0.9355649358759397 | 15.476123070722688 | 2 |
| Adaptive Boosting | 3.8037878787878814 | 7.100246612458202 | 0.9339239374684735 | 0.9265821527427482 | 10.001709506065362 | 3 |
| Extra Trees | 5.775431818181824 | 7.822140196304651 | 0.9190809984302347 | 0.9100899982558164 | 15.623018357777784 | 4 |
| K Nearest Neighbors Five | 3.220000000000001 | 8.079737322128098 | 0.901002211606513 | 0.89000245734057 | 6.552485325108222 | 5 |
| K Nearest Neighbors Three | 3.220000000000001 | 8.079737322128098 | 0.901002211606513 | 0.89000245734057 | 6.552485325108222 | 6 |
| Bagging Regressor | 6.724683766233768 | 9.014969095534857 | 0.8883535513059304 | 0.8759483903399227 | 14.802704460405685 | 7 |
| Polynomial Regression Degree 3 | 9.687263572354752 | 13.870493456673305 | 0.602676471343589 | 0.4323949590622701 | 19.710583943040504 | 8 |
| Decision Tree | 10.83068181818182 | 13.991555948773652 | 0.6394045833539457 | 0.5993384259488284 | 22.800886069516725 | 9 |
| Polynomial Ridge Degree 3 | 10.18948263078555 | 14.08231914778145 | 0.596743573226068 | 0.4239193903229541 | 21.763256762801625 | 10 |
| Support Vector Regression | 8.160169082257129 | 14.799535325273247 | 0.5514224295634942 | 0.5015804772927714 | 15.128891198559003 | 11 |
| Random Forest | 11.056820383824304 | 14.939809844052284 | 0.6035202991550379 | 0.5594669990611532 | 25.364279416895236 | 12 |
| Polynomial Regression Degree 2 | 13.704882266034115 | 16.96819961741376 | 0.5068381739464329 | 0.38354771743304106 | 31.19930956978714 | 13 |
| Polynomial Ridge Degree 2 | 13.299339259050857 | 17.119353612750018 | 0.49915612214230565 | 0.3739451526778821 | 31.17984184084805 | 14 |
| Linear Regression | 14.261887336262951 | 18.50032274622348 | 0.4291297958482495 | 0.36569977316472163 | 35.28442817873522 | 15 |

- **Best overall model (by overall mean RMSE)**: `Decision Tree`

### Best model per target (by RMSE)
| target | best_model_by_rmse | RMSE | R2 |
| --- | --- | --- | --- |
| Rct_initial_ohm | Adaptive Boosting | 12.545979757707569 | 0.9261236904318099 |
| ICE_percent | Gaussian Process Regression | 2.231636211036968 | 0.9407888002999073 |
| Initial Reversible Capacity_mAh_g at 0.1C | Gaussian Process Regression | 6.846584112358198 | 0.9544680577851876 |
| Highest Capacity Retention_percent | Gaussian Process Regression | 4.389801766206672 | 0.9624430495297631 |

## Scientific interpretation (1D thickness-response)

With $p=1$, estimator flexibility governs how $\mathbb{E}[Y_j \mid x]$ is approximated: **affine**, **smooth nonlinear** ($\hat{y}_j \in C^k$ for low $k$), or **threshold / cohort-segmented** behavior at the discrete support of $x$. In-sample $R^2$ can rise via interpolation of thickness cohorts; the decisive diagnostic is residual structure **vs.** $x$ and the plausibility of $\mathrm{d}\hat{y}_j/\mathrm{d}x$ on the nm axis.

Consult `outputs/eda/plots/` and `outputs/models/diagnostics_plots/` for overlap-aware scatter, parity lines, and residual sweeps keyed to thickness.

## Metric definitions (in-sample)

Residuals $\hat{\varepsilon}_{ij} = y_{ij} - \hat{y}_{ij}$. For each target $j$:

$$
\mathrm{MAE}_j = \frac{1}{n}\sum_{i=1}^{n}\bigl|\hat{\varepsilon}_{ij}\bigr|,\qquad \mathrm{RMSE}_j = \sqrt{\frac{1}{n}\sum_{i=1}^{n}\hat{\varepsilon}_{ij}^{2}},\qquad R^{2}_j = 1 - \frac{\sum_i \hat{\varepsilon}_{ij}^{2}}{\sum_i (y_{ij}-\bar{y}_j)^{2}}.
$$
