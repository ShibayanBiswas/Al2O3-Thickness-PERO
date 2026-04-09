from __future__ import annotations

from dataclasses import dataclass

import matplotlib as mpl

from .utils import strip_parentheses_text, to_title_case


@dataclass(frozen=True)
class PeroPalette:
    """
    Single source for figure colors (dark theme). Keeps EDA, diagnostics, and
    explainability visually consistent for thesis-style exports.
    """

    bg: str = "#0B0F1A"
    panel: str = "#121B2E"
    text: str = "#EAF0FF"
    axis: str = "#D9E1FF"
    grid: str = "#3A466B"
    grid_major: str = "#5A6AA0"
    grid_minor: str = "#2B3452"
    ink: str = "#0B0F1A"
    sky: str = "#5BC0EB"
    orange: str = "#FF9F1C"
    green: str = "#9FD356"
    gold: str = "#F7B801"
    red: str = "#D7263D"
    teal: str = "#1B998B"
    bar: str = "#2E86AB"
    violet: str = "#5E2BFF"
    lilac: str = "#C17CFF"
    legend_edge: str = "#5BC0EB"
    qq_ref: str = "#D7263D"

    def multiline_series(self) -> list[str]:
        """Distinct hues for several overlaid KDEs (e.g. scaling comparison)."""
        return [self.violet, self.gold, self.red, self.teal, self.lilac]


PERO = PeroPalette()


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
    # Chemical formula via mathtext (matches thesis-style notation); nm is explicit
    x_label = r"$\mathrm{Al}_{2}\mathrm{O}_{3}$ thickness / nm"

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
    dpi = getattr(cfg, "figure_dpi", 220)
    p = PERO
    base = {
            # Default geometry: enforce square figures unless a caller overrides.
            "figure.figsize": (8.0, 8.0),
            "figure.dpi": dpi,
            "savefig.dpi": dpi,
            "savefig.bbox": "tight",
            "savefig.facecolor": p.bg,
            "savefig.edgecolor": p.bg,
            "figure.facecolor": p.bg,
            "axes.facecolor": p.bg,
            "axes.edgecolor": p.axis,
            "axes.labelcolor": p.text,
            "axes.linewidth": 1.05,
            "text.color": p.text,
            "xtick.color": p.text,
            "ytick.color": p.text,
            "xtick.major.width": 1.0,
            "ytick.major.width": 1.0,
            "xtick.major.size": 5.0,
            "ytick.major.size": 5.0,
            "xtick.minor.size": 2.8,
            "ytick.minor.size": 2.8,
            "xtick.direction": "out",
            "ytick.direction": "out",
            # Grids: we prefer prominent majors + subtle minors on dark background.
            "axes.grid": True,
            "axes.axisbelow": True,
            "axes.grid.which": "both",
            "xtick.minor.visible": True,
            "ytick.minor.visible": True,
            "grid.color": p.grid_major,
            "grid.alpha": 0.78,
            "grid.linewidth": 1.25,
            "grid.linestyle": "-",
            "axes.titleweight": "semibold",
            "axes.titlesize": 16,
            "axes.labelsize": 13,
            "axes.titlepad": 10.0,
            "axes.labelpad": 6.0,
            "legend.frameon": True,
            "legend.facecolor": p.panel,
            "legend.edgecolor": p.grid,
            "legend.fontsize": 10.5,
            "legend.title_fontsize": 11.5,
            "legend.shadow": False,
            "legend.borderpad": 0.5,
            "legend.labelspacing": 0.55,
            # Slightly thinner strokes for a cleaner scientific feel.
            "lines.linewidth": 1.85,
            "lines.markersize": 6.6,
            "lines.antialiased": True,
            "patch.edgecolor": p.ink,
            "patch.linewidth": 0.75,
            "scatter.edgecolors": p.ink,
            "font.family": "DejaVu Sans",
            "font.size": 11,
            "mathtext.fontset": "stix",
        }

    # Matplotlib 3.11+ supports independent rcParams for major/minor grid.
    # If unavailable, we still get a "prominent major grid" via grid.* defaults above.
    if "grid.major.color" in mpl.rcParams:
        base.update(
            {
                "grid.major.color": p.grid_major,
                "grid.major.alpha": 0.78,
                "grid.major.linewidth": 1.25,
                "grid.major.linestyle": "-",
                "grid.minor.color": p.grid_minor,
                "grid.minor.alpha": 0.52,
                "grid.minor.linewidth": 0.85,
                "grid.minor.linestyle": "-",
            }
        )

    mpl.rcParams.update(base)


def polish_axes(ax) -> None:
    for spine in ax.spines.values():
        spine.set_linewidth(1.05)
        spine.set_color(PERO.axis)
        spine.set_alpha(0.92)
    ax.grid(True, which="major", alpha=0.78, linewidth=1.25, color=PERO.grid_major)
    try:
        ax.minorticks_on()
        ax.tick_params(which="major", length=5, width=1.0, colors=PERO.text, labelcolor=PERO.text)
        ax.tick_params(which="minor", length=2.5, width=0.7, colors=PERO.text, labelsize=9)
        ax.grid(True, which="minor", alpha=0.52, linewidth=0.85, color=PERO.grid_minor)
    except Exception:
        ax.tick_params(colors=PERO.text, labelcolor=PERO.text)


def set_dark_background(fig, axes) -> None:
    """
    Force PERO dark background even when callers create figures directly.
    """
    try:
        fig.patch.set_facecolor(PERO.bg)
    except Exception:
        pass
    if not isinstance(axes, (list, tuple)):
        axes = [axes]
    for ax in axes:
        try:
            ax.set_facecolor(PERO.bg)
        except Exception:
            pass


def legend_outside_top_right(
    ax,
    ncol: int = 1,
    *,
    title: str | None = None,
    handles: list | None = None,
    labels: list[str] | None = None,
) -> None:
    """
    Place a high-contrast legend to the right of the axes so it never occludes data.

    For heatmaps and other edge cases, pass explicit ``handles`` / ``labels``.
    """
    kw: dict = {
        "loc": "upper left",
        "bbox_to_anchor": (1.02, 1.0),
        "borderaxespad": 0.0,
        "ncol": ncol,
        "frameon": True,
        "framealpha": 0.95,
        "fancybox": True,
        "fontsize": 10,
    }
    if title:
        kw["title"] = title
    if handles is not None:
        kw["handles"] = handles
    if labels is not None:
        kw["labels"] = labels
    leg = ax.legend(**kw)
    if leg is not None:
        leg.get_frame().set_edgecolor(PERO.legend_edge)
        leg.get_frame().set_linewidth(0.95)
        leg.get_frame().set_alpha(0.96)
        for text in leg.get_texts():
            text.set_color(PERO.text)
        if leg.get_title() is not None:
            leg.get_title().set_color(PERO.text)


def apply_sexy_shadows(ax) -> None:
    """
    Add subtle shadows/strokes to improve legibility on dark backgrounds.
    Uses Matplotlib path effects (no extra dependencies).
    """
    try:
        import matplotlib.patheffects as pe
    except Exception:
        return

    # Text: outline + tiny offset shadow
    try:
        t = ax.title
        t.set_path_effects(
            [
                pe.SimpleLineShadow(offset=(1.2, -1.2), alpha=0.35, shadow_color=PERO.ink),
                pe.withStroke(linewidth=2.6, foreground=PERO.ink, alpha=0.75),
                pe.Normal(),
            ]
        )
    except Exception:
        pass

    # Lines: a faint stroke behind to "lift" the curve
    for ln in getattr(ax, "lines", []):
        try:
            ln.set_path_effects([pe.withStroke(linewidth=ln.get_linewidth() + 1.6, foreground=PERO.ink, alpha=0.55), pe.Normal()])
        except Exception:
            pass

    # Collections (scatter): subtle stroke (works on PathCollection)
    for coll in getattr(ax, "collections", []):
        try:
            coll.set_path_effects([pe.withStroke(linewidth=2.0, foreground=PERO.ink, alpha=0.35), pe.Normal()])
        except Exception:
            pass

    # Patches (bars, filled areas): soft outline
    for patch in getattr(ax, "patches", []):
        try:
            patch.set_path_effects([pe.withStroke(linewidth=2.0, foreground=PERO.ink, alpha=0.25), pe.Normal()])
        except Exception:
            pass
