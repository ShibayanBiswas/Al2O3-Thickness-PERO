from __future__ import annotations

from pathlib import Path
from typing import Callable

import matplotlib.pyplot as plt

from .utils import ensure_dir, safe_filename


def savefig(fig: plt.Figure, out_dir: Path, name: str, dpi: int = 220, fmt: str = "png") -> Path:
    ensure_dir(out_dir)
    fname = f"{safe_filename(name)}.{fmt}"
    out_path = out_dir / fname
    fig.tight_layout()
    fig.savefig(out_path, dpi=dpi, bbox_inches="tight")
    plt.close(fig)
    return out_path


def new_figure(figsize=(10, 6)) -> plt.Figure:
    return plt.figure(figsize=figsize)


def with_axes(figsize=(10, 6)):
    fig, ax = plt.subplots(figsize=figsize)
    return fig, ax


def annotate_extremes(ax, x, y, n: int = 2, label_fmt: Callable[[int, float, float], str] | None = None):
    import numpy as np

    x = np.asarray(x)
    y = np.asarray(y)
    if y.size == 0:
        return
    idx_sorted = np.argsort(y)
    idxs = list(idx_sorted[:n]) + list(idx_sorted[-n:])
    seen = set()
    for i in idxs:
        if int(i) in seen:
            continue
        seen.add(int(i))
        txt = label_fmt(i, x[i], y[i]) if label_fmt else f"idx={i}"
        ax.annotate(txt, (x[i], y[i]), textcoords="offset points", xytext=(6, 6), fontsize=9)

