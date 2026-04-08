from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from .config import ColumnSpec


@dataclass(frozen=True)
class DataBundle:
    df_raw: pd.DataFrame
    df: pd.DataFrame
    X: pd.DataFrame
    Y: pd.DataFrame
    x_col: str
    y_cols: tuple[str, ...]


def load_dataset_excel(xlsx_path: str, colspec: ColumnSpec) -> pd.DataFrame:
    df = pd.read_excel(xlsx_path, sheet_name=colspec.sheet_name)
    return df


def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    # We keep original names if they match; otherwise do light cleanup (whitespace normalization)
    df2 = df.copy()
    df2.columns = [str(c).strip() for c in df2.columns]
    return df2


def coerce_numeric(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    df2 = df.copy()
    for c in cols:
        df2[c] = pd.to_numeric(df2[c], errors="raise")
    return df2


def validate_dataset(df: pd.DataFrame, colspec: ColumnSpec) -> None:
    missing = [c for c in [colspec.x_col, *colspec.y_cols] if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns in Dataset sheet: {missing}. Found: {list(df.columns)}")

    # No missing values in main sheet (per requirement) – enforce strongly
    required = [colspec.x_col, *colspec.y_cols]
    if df[required].isna().any().any():
        na_cols = df[required].isna().sum().sort_values(ascending=False)
        raise ValueError(f"Unexpected missing values found:\n{na_cols[na_cols>0]}")

    # Ensure numeric types for X and y
    for c in required:
        if not np.issubdtype(df[c].dtype, np.number):
            raise TypeError(f"Column {c!r} is not numeric after coercion. dtype={df[c].dtype}")

    # Sanity: thickness should be >= 0 (physical thickness)
    if (df[colspec.x_col] < 0).any():
        bad = df.loc[df[colspec.x_col] < 0, colspec.x_col].head(10).to_list()
        raise ValueError(f"Found negative thickness values (showing up to 10): {bad}")


def prepare_data(xlsx_path: str, colspec: ColumnSpec) -> DataBundle:
    df_raw = load_dataset_excel(xlsx_path, colspec=colspec)
    df = standardize_columns(df_raw)

    # Drop ignore columns (Sample), but only if present
    drop_cols = [c for c in colspec.ignore_columns if c in df.columns]
    if drop_cols:
        df = df.drop(columns=drop_cols)

    # Coerce required numeric columns strictly
    df = coerce_numeric(df, cols=[colspec.x_col, *list(colspec.y_cols)])

    validate_dataset(df, colspec=colspec)

    X = df[[colspec.x_col]].copy()
    Y = df[list(colspec.y_cols)].copy()
    return DataBundle(df_raw=df_raw, df=df, X=X, Y=Y, x_col=colspec.x_col, y_cols=colspec.y_cols)

