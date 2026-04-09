from __future__ import annotations

from pathlib import Path
from typing import Callable

import matplotlib.pyplot as plt

from .utils import ensure_dir, safe_filename


def scatter_with_marginals(
    x,
    y,
    *,
    figsize=(7.5, 7.5),
    top_frac: float = 0.18,
    right_frac: float = 0.18,
):
    """
    Create a square scatter layout with inset distributions *inside* the main axes.

    The inset panels are intended as a "raincloud-like" context: KDE + histogram
    (or histogram fallback), plus a light rug where possible. They live inside the
    main plot area (not on separate exterior axes).
    """
    import numpy as np

    x = np.asarray(x, dtype=float).ravel()
    y = np.asarray(y, dtype=float).ravel()

    fig, ax_main = plt.subplots(figsize=figsize)

    # Inset distributions (inside-plot) placed in reserved corner rectangles
    # using axes coordinates so they don't drift with data limits.
    pad = 0.045
    top_h = float(np.clip(top_frac, 0.10, 0.28))
    right_w = float(np.clip(right_frac, 0.10, 0.28))

    # Top inset spans most width but leaves room for the right inset.
    top_x0 = pad
    top_y0 = 1.0 - pad - top_h
    top_w = max(0.20, 1.0 - 2 * pad - right_w)
    ax_top = ax_main.inset_axes([top_x0, top_y0, top_w, top_h], transform=ax_main.transAxes)

    # Right inset spans most height but leaves room for the top inset.
    right_x0 = 1.0 - pad - right_w
    right_y0 = pad
    right_h = max(0.20, 1.0 - 2 * pad - top_h)
    ax_right = ax_main.inset_axes([right_x0, right_y0, right_w, right_h], transform=ax_main.transAxes)

    # "Glass" panels: visible but not intrusive.
    for a in (ax_top, ax_right):
        a.set_facecolor((0.08, 0.10, 0.12, 0.55))
        for sp in a.spines.values():
            sp.set_alpha(0.45)
            sp.set_linewidth(0.9)
        a.grid(False)
        a.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)

    # Marginals: prefer seaborn if available
    try:
        import seaborn as sns  # type: ignore

        # Top: x distribution
        sns.histplot(x, ax=ax_top, stat="density", kde=False, bins="auto", alpha=0.25)
        sns.kdeplot(x, ax=ax_top, linewidth=1.4, warn_singular=False)
        try:
            sns.rugplot(x, ax=ax_top, height=0.08, alpha=0.25)
        except Exception:
            pass

        # Right: y distribution (horizontal)
        sns.histplot(y=y, ax=ax_right, stat="density", kde=False, bins="auto", orientation="horizontal", alpha=0.25)
        sns.kdeplot(y=y, ax=ax_right, linewidth=1.4, warn_singular=False)
        try:
            sns.rugplot(y, ax=ax_right, height=0.08, alpha=0.25)
        except Exception:
            pass
    except Exception:
        # Fallback: simple histograms
        try:
            ax_top.hist(x[np.isfinite(x)], bins="auto", density=True, alpha=0.22)
        except Exception:
            pass
        try:
            ax_right.hist(y[np.isfinite(y)], bins="auto", density=True, alpha=0.22, orientation="horizontal")
        except Exception:
            pass

    return fig, ax_main, ax_top, ax_right


def savefig(fig: plt.Figure, out_dir: Path, name: str, dpi: int = 220, fmt: str = "png") -> Path:
    ensure_dir(out_dir)
    fname = f"{safe_filename(name)}.{fmt}"
    out_path = out_dir / fname
    # Apply global finishing touches (shadows/strokes) right before export.
    try:
        from .viz_style import apply_sexy_shadows

        for ax in fig.axes:
            apply_sexy_shadows(ax)
    except Exception:
        pass
    fig.tight_layout()
    fig.savefig(out_path, dpi=dpi, bbox_inches="tight")
    plt.close(fig)
    return out_path


def new_figure(figsize=(8, 8)) -> plt.Figure:
    return plt.figure(figsize=figsize)


def with_axes(figsize=(8, 8)):
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

