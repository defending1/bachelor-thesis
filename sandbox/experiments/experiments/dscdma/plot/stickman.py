"""
Vector stickman figure drawing module for Matplotlib.
"""

from typing import Optional
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, PathPatch, Rectangle
from matplotlib.path import Path as MPath


def draw_stickman(
    ax: plt.Axes,
    x: float,
    y: float,
    size: float = 4.0,
    color: str = "#0072B2",
    label: Optional[str] = None,
    style: str = "solid",
    alpha: float = 1.0,
    linestyle: str = "-",
    fill_head: Optional[bool] = None,
    show_box: bool = False,
) -> None:
    """
    Draws a vector stickman figure at coordinate (x, y).

    Parameters
    ----------
    style : str
        'solid' for true users (filled head, solid lines), 'ghost' / 'dashed' / 'hollow' for recovered users.
    alpha : float
        Opacity level (0.0 to 1.0).
    linestyle : str
        Line style for drawing ('-' for continuous solid lines, '--' for dashed).
    fill_head : bool, optional
        Whether to fill the head circle. Defaults to True for 'solid' and False for 'ghost'/'hollow'.
    show_box : bool
        Whether to render a background bounding box (default False for publication clarity).
    """
    is_ghost = style.lower() in ("ghost", "dashed")
    ls = linestyle if linestyle != "-" else ("--" if is_ghost else "-")
    should_fill = (not is_ghost) if fill_head is None else fill_head
    eff_alpha = alpha

    if show_box:
        box_half = size * 0.7
        box = Rectangle(
            (x - box_half, y - box_half * 0.4),
            2 * box_half,
            2 * box_half,
            facecolor="aliceblue" if should_fill else "none",
            alpha=0.3 * eff_alpha,
            edgecolor=color,
            linestyle=ls,
            linewidth=1.2,
            zorder=5,
            label=label if label else None,
        )
        ax.add_patch(box)

    head_radius = size * 0.20
    head_center = (x, y + size * 0.65)
    head = Circle(
        head_center,
        head_radius,
        facecolor=color if should_fill else "none",
        edgecolor=color if not should_fill else "black",
        linestyle=ls,
        linewidth=1.2 if not should_fill else 0.8,
        alpha=eff_alpha,
        zorder=6,
        label=label if (label and not show_box) else None,
    )
    ax.add_patch(head)

    verts = [
        (x, y + size * 0.43),
        (x, y + size * 0.1),
        (x - size * 0.28, y + size * 0.30),
        (x + size * 0.28, y + size * 0.30),
        (x, y + size * 0.1),
        (x - size * 0.22, y - size * 0.25),
        (x, y + size * 0.1),
        (x + size * 0.22, y - size * 0.25),
    ]
    codes = [
        MPath.MOVETO,
        MPath.LINETO,
        MPath.MOVETO,
        MPath.LINETO,
        MPath.MOVETO,
        MPath.LINETO,
        MPath.MOVETO,
        MPath.LINETO,
    ]
    path = MPath(verts, codes)
    patch = PathPatch(
        path,
        edgecolor=color,
        linestyle=ls,
        linewidth=2.0 if should_fill else 1.6,
        alpha=eff_alpha,
        zorder=6,
    )
    ax.add_patch(patch)
