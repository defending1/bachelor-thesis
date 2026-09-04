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
    color: str = "royalblue",
    label: Optional[str] = None,
) -> None:
    """
    Draws a vector stickman figure inside a transparent bounding square box at coordinate (x, y).
    """
    box_half = size * 0.7
    box = Rectangle(
        (x - box_half, y - box_half * 0.4),
        2 * box_half,
        2 * box_half,
        facecolor="aliceblue",
        alpha=0.6,
        edgecolor=color,
        linewidth=1.5,
        zorder=5,
        label=label,
    )
    ax.add_patch(box)

    head_radius = size * 0.20
    head_center = (x, y + size * 0.65)
    head = Circle(
        head_center,
        head_radius,
        facecolor=color,
        edgecolor="black",
        linewidth=0.8,
        zorder=6,
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
    patch = PathPatch(path, edgecolor=color, linewidth=2.0, zorder=6)
    ax.add_patch(patch)
