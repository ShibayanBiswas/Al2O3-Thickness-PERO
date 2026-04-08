from __future__ import annotations

from dataclasses import dataclass

import matplotlib as mpl

from .utils import strip_parentheses_text, to_title_case


@dataclass(frozen=True)
class DisplayLabels:
    x_label: str
    y_label_map: dict[str, str]
    target_title_map: dict[str, str]


def get_display_labels(x_col: str, y_cols: list[str]) -> DisplayLabels:
    """
    Human-friendly, publication-style display names.

    Hard constraint from user:
    - No parentheses in displayed text
    - Title Case text in labels
    - Avoid bare digits and operator symbols in visible titles/labels/legends
    """
    # X label: avoid chemical digits in "Al2O3" on axes text; keep the scientific intent in words
    x_label = r"$\mathrm{Aluminum\ Oxide}$ Thickness"

    y_map: dict[str, str] = {
        "Rct_initial_ohm": r"$R_{\mathrm{ct}}$ Initial",
        "ICE_percent": r"$\mathrm{Initial\ Coulombic\ Efficiency}$",
        "Initial Reversible Capacity_mAh_g at 0.1C": r"$Q_{\mathrm{rev}}$ Initial",
        "Highest Capacity Retention_percent": r"$\mathrm{Capacity\ Retention}$ Highest",
    }

    # Titles can mirror labels but should be readable sentences without punctuation noise
    title_map: dict[str, str] = {
        "Rct_initial_ohm": "Charge Transfer Resistance Initial",
        "ICE_percent": "Initial Coulombic Efficiency",
        "Initial Reversible Capacity_mAh_g at 0.1C": "Initial Reversible Capacity",
        "Highest Capacity Retention_percent": "Highest Capacity Retention",
    }

    # Ensure every target has something sensible
    for y in y_cols:
        y_map.setdefault(y, to_title_case(strip_parentheses_text(y)))
        title_map.setdefault(y, to_title_case(strip_parentheses_text(y)))

    return DisplayLabels(x_label=x_label, y_label_map=y_map, target_title_map=title_map)


def apply_pero_theme(cfg: object) -> None:
    """
    A high-contrast, modern research style tuned for export figures.
    Uses mathtext (LaTeX-like) formatting without requiring a LaTeX install.
    """
    # Seaborn will be configured by caller; here we tighten mpl rcParams.
    mpl.rcParams.update(
        {
            "figure.dpi": getattr(cfg, "figure_dpi", 220),
            "savefig.dpi": getattr(cfg, "figure_dpi", 220),
            "savefig.bbox": "tight",
            "figure.facecolor": "#0B0F1A",  # deep navy
            "axes.facecolor": "#0B0F1A",
            "axes.edgecolor": "#D9E1FF",
            "axes.labelcolor": "#EAF0FF",
            "text.color": "#EAF0FF",
            "xtick.color": "#EAF0FF",
            "ytick.color": "#EAF0FF",
            "grid.color": "#3A466B",
            "grid.alpha": 0.55,
            "grid.linewidth": 0.9,
            "axes.grid": True,
            "axes.axisbelow": True,
            "axes.titleweight": "semibold",
            "axes.titlesize": 16,
            "axes.labelsize": 14,
            "legend.frameon": True,
            "legend.facecolor": "#121B2E",
            "legend.edgecolor": "#3A466B",
            "legend.fontsize": 12,
            "lines.linewidth": 2.6,
            "lines.markersize": 7.5,
            "patch.edgecolor": "#0B0F1A",
            "font.family": "DejaVu Sans",
            "mathtext.fontset": "stix",
        }
    )


def polish_axes(ax) -> None:
    # Subtle spines and minor grid for a "sexy" but readable look
    for spine in ax.spines.values():
        spine.set_linewidth(1.1)
        spine.set_alpha(0.9)
    ax.grid(True, which="major")
    try:
        ax.minorticks_on()
        ax.grid(True, which="minor", alpha=0.22, linewidth=0.6)
    except Exception:
        pass


def set_dark_background(fig, axes) -> None:
    """
    Force PERO dark background even when callers create figures directly.
    """
    try:
        fig.patch.set_facecolor("#0B0F1A")
    except Exception:
        pass
    if not isinstance(axes, (list, tuple)):
        axes = [axes]
    for ax in axes:
        try:
            ax.set_facecolor("#0B0F1A")
        except Exception:
            pass


def legend_outside_top_right(ax, ncol: int = 1) -> None:
    """
    Place legend outside so it never overlaps data.
    """
    leg = ax.legend(
        loc="upper left",
        bbox_to_anchor=(1.02, 1.0),
        borderaxespad=0.0,
        ncol=ncol,
        frameon=True,
    )
    if leg is not None:
        leg.get_frame().set_alpha(0.92)
