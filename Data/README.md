# Data Directory

Authoritative data live here so provenance never forks silently. The pipeline reads **exactly one** workbook path and refuses to improvise alternates—reproducibility beats convenience.

---

## Design & measurement model (conceptual)

Rows index experimental cells; columns hold **one** controlled continuous nominal input—alumina thickness $x\ge 0$ (nm)—plus four **downstream electrochemical readouts** modeled as

$$
y_j = f_j(x) + \varepsilon_j,\quad j=1,\dots,4,
$$

with unknown smooth or threshold-like $f_j$ and cell-level noise $\varepsilon_j$. The tabulation is sparse in $x$: many replicate specimens share identical thickness, so **cohort structure** dominates naive “continuous regression” intuition.

---

## Structural facts every analyst should internalize

- **Sheet rule:** only `Dataset` is ingested; other sheets are ignored by construction.
- **Identifier column `Sample`:** deliberately dropped so inference cannot smuggle hidden covariates through label leakage.
- **Discrete support:** mass concentrates at $x=0$ nm with a long tail of sparse nonzero levels—EDA therefore emphasizes grouped means, ribbons, and overlap-aware scatter rather than a single Pearson coefficient.

Strict numeric coercion and schema checks fail fast if headers drift. That harshness is deliberate: **PERO** outputs should remain litigation-grade for thesis committees.

---

## Files

| File | Role |
| --- | --- |
| **`Data.xlsx`** | Canonical multi-sheet workbook; analysis consumes `Dataset` only |
