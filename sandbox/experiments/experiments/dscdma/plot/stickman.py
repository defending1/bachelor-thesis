"""
Vector stickman figure drawing module for Matplotlib.
"""

from typing import Optional
import matplotlib.pyplot as plt
from matplotlib.legend_handler import HandlerBase
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


class StickmanLegendObject:
    """Proxy object representing a stickman figure in Matplotlib legends."""
    def __init__(
        self,
        color: str = "black",
        linestyle: str = "-",
        fill_head: bool = False,
        label_text: Optional[str] = None,
    ):
        self.color = color
        self.linestyle = linestyle
        self.fill_head = fill_head
        self.label_text = label_text


class HandlerStickman(HandlerBase):
    """Custom Matplotlib Legend Handler that renders a stickman icon inside legends."""
    def create_artists(self, legend, orig_handle, xdescent, ydescent, width, height, fontsize, trans):
        from matplotlib.patches import Circle, PathPatch
        from matplotlib.path import Path as MPath
        from matplotlib.text import Text

        cx = xdescent + width * 0.38
        cy = ydescent + height * 0.15
        size = height * 1.2
        color = getattr(orig_handle, "color", "black")
        ls = getattr(orig_handle, "linestyle", "-")
        should_fill = getattr(orig_handle, "fill_head", False)
        text_str = getattr(orig_handle, "label_text", None)

        head = Circle(
            (cx, cy + size * 0.24),
            size * 0.21,
            facecolor=color if should_fill else "none",
            edgecolor=color,
            linestyle=ls,
            linewidth=1.3,
            transform=trans,
        )
        verts = [
            (cx, cy + size * 0.08), (cx, cy - size * 0.16),
            (cx - size * 0.23, cy + size * 0.02), (cx + size * 0.23, cy + size * 0.02),
            (cx, cy - size * 0.16), (cx - size * 0.20, cy - size * 0.43),
            (cx, cy - size * 0.16), (cx + size * 0.20, cy - size * 0.43),
        ]
        codes = [
            MPath.MOVETO, MPath.LINETO,
            MPath.MOVETO, MPath.LINETO,
            MPath.MOVETO, MPath.LINETO,
            MPath.MOVETO, MPath.LINETO,
        ]
        body = PathPatch(
            MPath(verts, codes),
            edgecolor=color,
            linestyle=ls,
            linewidth=1.5,
            transform=trans,
        )
        artists = [head, body]

        if text_str:
            txt = Text(
                cx + size * 0.22,
                cy - size * 0.35,
                text_str,
                fontsize=fontsize * 0.95,
                fontweight="bold",
                color=color,
                ha="left",
                va="center",
                transform=trans,
            )
            artists.append(txt)

        return artists
