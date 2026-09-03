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

    Args:
        ax (plt.Axes): Matplotlib axes object.
        x (float): Center X coordinate.
        y (float): Center Y coordinate.
        size (float): Scale size of the stickman figure and box.
        color (str): Color of the figure and box border.
        label (Optional[str]): Legend label.
    """
    # 1. Bounding Translucent Square Box
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

    # 2. Stickman Figure
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

    # Torso, Arms, and Legs
    verts = [
        (x, y + size * 0.43),
        (x, y + size * 0.1),  # Torso
        (x - size * 0.28, y + size * 0.30),
        (x + size * 0.28, y + size * 0.30),  # Arms
        (x, y + size * 0.1),
        (x - size * 0.22, y - size * 0.25),  # Left Leg
        (x, y + size * 0.1),
        (x + size * 0.22, y - size * 0.25),  # Right Leg
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
