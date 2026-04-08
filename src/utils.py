from __future__ import annotations

import importlib
import math
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

import numpy as np
import pandas as pd


def optional_import(module_name: str) -> Any | None:
    try:
        return importlib.import_module(module_name)
    except Exception:
        return None


def safe_filename(s: str, max_len: int = 140) -> str:
    s = s.strip()
    # Keep filenames readable and stable, but avoid punctuation that users asked to avoid in visible strings.
    # (Filenames are not plot text, but we still normalize aggressively.)
    s = s.replace("(", " ").replace(")", " ")
    s = re.sub(r"[^\w\-. \[\]]+", "_", s)
    s = re.sub(r"\s+", " ", s)
    s = s.strip(" .")
    if len(s) > max_len:
        s = s[:max_len].rstrip()
    return s


def to_title_case(s: str) -> str:
    """
    Convert to Title Case in a conservative way while preserving acronyms like ICE.
    """
    words = re.split(r"(\s+)", str(s).strip())
    out = []
    for w in words:
        if w.isspace():
            out.append(w)
            continue
        if w.isupper() and len(w) <= 6:
            out.append(w)
        else:
            out.append(w[:1].upper() + w[1:].lower())
    return "".join(out)


def strip_parentheses_text(s: str) -> str:
    # Remove any parenthesized content from display strings
    return re.sub(r"\s*\([^)]*\)\s*", " ", str(s)).strip()


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def set_global_plot_style(seaborn: Any, cfg: Any) -> None:
    seaborn.set_theme(style=cfg.seaborn_theme, context=cfg.seaborn_context, palette=cfg.seaborn_palette)


def iqr(x: np.ndarray) -> float:
    x = np.asarray(x, dtype=float)
    q75, q25 = np.nanpercentile(x, [75, 25])
    return float(q75 - q25)


def robust_summary_stats(x: pd.Series) -> dict[str, float]:
    x_num = pd.to_numeric(x, errors="coerce")
    vals = x_num.to_numpy(dtype=float)
    med = float(np.nanmedian(vals))
    q75, q25 = np.nanpercentile(vals, [75, 25])
    return {
        "median": med,
        "q25": float(q25),
        "q75": float(q75),
        "iqr": float(q75 - q25),
    }


def zscore_outliers(x: np.ndarray, threshold: float = 3.0) -> np.ndarray:
    x = np.asarray(x, dtype=float)
    mu = np.nanmean(x)
    sd = np.nanstd(x, ddof=1)
    if not np.isfinite(sd) or sd == 0:
        return np.zeros_like(x, dtype=bool)
    z = (x - mu) / sd
    return np.abs(z) > threshold


def iqr_outliers(x: np.ndarray, k: float = 1.5) -> np.ndarray:
    x = np.asarray(x, dtype=float)
    q1, q3 = np.nanpercentile(x, [25, 75])
    i = q3 - q1
    if not np.isfinite(i) or i == 0:
        return np.zeros_like(x, dtype=bool)
    lo = q1 - k * i
    hi = q3 + k * i
    return (x < lo) | (x > hi)


def adjusted_r2(r2: float, n: int, p: int) -> float | float("nan"):
    # p excludes intercept; for single-feature, p=1 (or polynomial feature count)
    if n <= p + 1:
        return float("nan")
    return 1.0 - (1.0 - r2) * (n - 1) / (n - p - 1)


def safe_mape(y_true: np.ndarray, y_pred: np.ndarray, eps: float = 1e-9) -> float:
    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)
    denom = np.maximum(np.abs(y_true), eps)
    return float(np.mean(np.abs((y_true - y_pred) / denom)) * 100.0)


@dataclass(frozen=True)
class TargetMetrics:
    mae: float
    mse: float
    rmse: float
    r2: float
    adj_r2: float
    mape_percent: float
    medae: float
    explained_var: float


def make_readme(path: Path, title: str, bullets: Iterable[str]) -> None:
    ensure_dir(path.parent)
    lines = [f"# {title}", ""]
    for b in bullets:
        lines.append(f"- {b}")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def write_tables_excel(path: Path, sheets: dict[str, pd.DataFrame]) -> None:
    ensure_dir(path.parent)
    with pd.ExcelWriter(path, engine="xlsxwriter") as writer:
        for name, df in sheets.items():
            df.to_excel(writer, sheet_name=safe_sheet_name(name), index=False)


def safe_sheet_name(name: str) -> str:
    # Excel: <=31 chars, cannot contain: : \ / ? * [ ]
    name = re.sub(r"[:\\/?*\[\]]+", "_", name)
    name = name.replace("(", " ").replace(")", " ")
    name = name.strip()
    if not name:
        name = "Sheet"
    return name[:31]

