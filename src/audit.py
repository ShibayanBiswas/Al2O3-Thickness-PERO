from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from .utils import robust_summary_stats


@dataclass(frozen=True)
class AuditResult:
    audit_table: pd.DataFrame
    duplicates_count: int
    thickness_value_counts: pd.DataFrame


def build_data_audit_table(df: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for c in df.columns:
        s = df[c]
        is_num = np.issubdtype(s.dtype, np.number)
        row: dict[str, object] = {
            "column": c,
            "dtype": str(s.dtype),
            "missing": int(s.isna().sum()),
            "unique": int(s.nunique(dropna=False)),
        }
        if is_num:
            vals = pd.to_numeric(s, errors="coerce")
            row.update(
                {
                    "min": float(vals.min()),
                    "max": float(vals.max()),
                    "mean": float(vals.mean()),
                    "std": float(vals.std(ddof=1)),
                }
            )
            row.update(robust_summary_stats(vals))
        else:
            row.update({"min": np.nan, "max": np.nan, "mean": np.nan, "std": np.nan, "median": np.nan, "q25": np.nan, "q75": np.nan, "iqr": np.nan})
        rows.append(row)

    out = pd.DataFrame(rows)
    ordered = [
        "column",
        "dtype",
        "missing",
        "unique",
        "min",
        "max",
        "mean",
        "std",
        "median",
        "q25",
        "q75",
        "iqr",
    ]
    return out[ordered]


def audit_dataset(df: pd.DataFrame, x_col: str) -> AuditResult:
    audit_table = build_data_audit_table(df)
    duplicates_count = int(df.duplicated().sum())
    vc = df[x_col].value_counts(dropna=False).sort_index()
    thickness_value_counts = vc.reset_index()
    thickness_value_counts.columns = [x_col, "count"]
    thickness_value_counts["fraction"] = thickness_value_counts["count"] / thickness_value_counts["count"].sum()
    return AuditResult(audit_table=audit_table, duplicates_count=duplicates_count, thickness_value_counts=thickness_value_counts)

