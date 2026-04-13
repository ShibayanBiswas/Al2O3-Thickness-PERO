# Data Directory

Authoritative data live here so provenance never forks silently. The pipeline reads **exactly one** workbook path and refuses to improvise alternates—reproducibility beats convenience.

---

## Design & measurement model (conceptual)

Rows index experimental cells. The sole **controlled** continuous coordinate is **$\mathrm{Al}_{2}\mathrm{O}_{3}$** thickness $x\ge 0$ (nanometres), paired with four electrochemical responses:

$$
y_j \;=\; f_j(x) + \varepsilon_j,
\qquad j=1,\ldots,4,
\qquad \mathbb{E}[\varepsilon_j \mid x]=0 \;\text{(working identity).}
$$

The maps $f_j$ may be smooth, piecewise, or cohort-dominated; with replicated $x$ atoms, **within-level** and **between-level** variance must be read together—marginal correlations are not sufficient statistics.

---

## Structural facts every analyst should internalize

- **Sheet rule:** the pipeline prefers `Dataset` if present; if the workbook uses a different name (e.g. `Sheet1`), it falls back to the **first** worksheet deterministically.
- **Identifier column `Sample`:** deliberately dropped so inference cannot smuggle hidden covariates through label leakage.
- **Discrete support:** mass concentrates at $x=0$ nm with a long tail of sparse nonzero levels—EDA therefore emphasizes grouped means, ribbons, and overlap-aware scatter rather than a single Pearson coefficient.

Strict numeric coercion and schema checks fail fast if headers drift. That harshness is deliberate: **PERO** outputs should remain litigation-grade for thesis committees.

---

## Files

| File | Role |
| --- | --- |
| **`Data.xlsx`** | Canonical workbook; analysis consumes the configured worksheet name (fallback: first sheet) |
