"""
Visualization module for DS-CDMA spatial positions and antenna-centered radius circles.
"""

from typing import Optional, Tuple
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, PathPatch, Rectangle
from matplotlib.path import Path as MPath
from scipy.optimize import least_squares


import itertools


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


def estimate_antenna_positions(
    user_pos: np.ndarray,
    A_est: np.ndarray,
) -> np.ndarray:
    """
    Estimates 2D antenna positions from user coordinates and estimated channel matrix A_est
    using non-linear least squares trilateration based on radii R_ir = 1 / |a_ir|.
    Evaluates column permutations of A_est to automatically identify the optimal user assignment.

    Args:
        user_pos (np.ndarray): Transmitting user 2D coordinates of shape (R, 2).
        A_est (np.ndarray): Estimated channel gain matrix of shape (I, R).

    Returns:
        np.ndarray: Estimated 2D antenna positions of shape (I, 2).
    """
    I, R = A_est.shape
    radii = 1.0 / np.abs(A_est)

    best_total_cost = float("inf")
    best_antenna_pos_est = np.zeros((I, 2), dtype=np.float64)

    # Evaluate column permutations if R is small (<= 8) to map columns to users
    permutations = (
        list(itertools.permutations(range(R))) if R <= 8 else [tuple(range(R))]
    )

    for perm in permutations:
        u_perm = user_pos[list(perm), :]
        init_pos = np.mean(u_perm, axis=0)
        pos_est = np.zeros((I, 2), dtype=np.float64)
        total_cost = 0.0

        for i in range(I):
            r_target = radii[i, :]

            def residuals(p: np.ndarray) -> np.ndarray:
                dists = np.linalg.norm(u_perm - p, axis=1)
                return dists - r_target

            res = least_squares(residuals, init_pos)
            pos_est[i] = res.x
            total_cost += float(res.cost)

        if total_cost < best_total_cost:
            best_total_cost = total_cost
            best_antenna_pos_est = pos_est

    return best_antenna_pos_est


def plot_antenna_and_radii(
    user_pos: np.ndarray,
    antenna_pos_true: np.ndarray,
    A_est: np.ndarray,
    antenna_pos_est: Optional[np.ndarray] = None,
    title: str = "User & Antenna Positions Recover using CP ALS",
    save_path: Optional[str] = None,
    show: bool = False,
) -> Tuple[plt.Figure, plt.Axes]:
    """
    Plots users as stickmen, ground truth antennae, recovered antennae, and circles of radius
    centered around recovered antenna positions.

    Args:
        user_pos (np.ndarray): User 2D coordinates of shape (R, 2).
        antenna_pos_true (np.ndarray): True antenna 2D coordinates of shape (I, 2).
        A_est (np.ndarray): Estimated channel matrix hat(A) of shape (I, R).
        antenna_pos_est (Optional[np.ndarray]): Estimated antenna 2D coordinates of shape (I, 2).
            If None, antenna positions are computed via trilateration.
        title (str): Title for the plot.
        save_path (Optional[str]): File path to save figure (e.g. 'plot.pdf').
        show (bool): If True, calls plt.show().

    Returns:
        Tuple[plt.Figure, plt.Axes]: Matplotlib figure and axes objects.
    """
    I, R = A_est.shape

    if antenna_pos_est is None:
        antenna_pos_est = estimate_antenna_positions(user_pos, A_est)

    # Radii for recovered antennae R_ir = 1 / |hat(a_ir)|
    radii_est = 1.0 / np.abs(A_est)

    fig, ax = plt.subplots(figsize=(10, 8))

    # Color map for antennae to distinguish their circles
    colors = plt.cm.tab10(np.linspace(0, 1, max(I, 10)))

    # 1. Plot estimated radii circles centered around recovered antennae
    for i in range(I):
        c_est = antenna_pos_est[i]
        ant_color = colors[i % len(colors)]
        for r in range(R):
            radius = radii_est[i, r]
            circle = Circle(
                xy=(c_est[0], c_est[1]),
                radius=radius,
                fill=False,
                edgecolor=ant_color,
                linestyle="--",
                linewidth=1.2,
                alpha=0.6,
                label=f"Rec Ant {i + 1} Circles" if r == 0 else None,
            )
            ax.add_patch(circle)

    # 2. Draw stickmen inside transparent bounding square boxes for user positions
    for r in range(R):
        draw_stickman(
            ax,
            user_pos[r, 0],
            user_pos[r, 1],
            size=4.0,
            color="royalblue",
            label="Users" if r == 0 else None,
        )
        ax.annotate(
            f"  U{r + 1}",
            (user_pos[r, 0], user_pos[r, 1] + 3.4),
            fontsize=10,
            fontweight="bold",
            color="navy",
            zorder=7,
        )

    # 3. Scatter plot true antenna positions
    ax.scatter(
        antenna_pos_true[:, 0],
        antenna_pos_true[:, 1],
        c="crimson",
        marker="^",
        s=120,
        edgecolors="black",
        linewidths=1.0,
        zorder=5,
        label="True Antennae",
    )
    for i in range(I):
        ax.annotate(
            f"  A{i + 1} (True)",
            (antenna_pos_true[i, 0], antenna_pos_true[i, 1]),
            fontsize=9,
            color="crimson",
            zorder=6,
        )

    # 4. Scatter plot recovered antenna positions with matching circle colors
    for i in range(I):
        ant_color = colors[i % len(colors)]
        ax.scatter(
            antenna_pos_est[i, 0],
            antenna_pos_est[i, 1],
            color=ant_color,
            marker="x",
            s=140,
            linewidths=2.5,
            zorder=7,
            label="Recovered Antennae" if i == 0 else None,
        )
        ax.annotate(
            f"  A{i + 1} (Rec)",
            (antenna_pos_est[i, 0], antenna_pos_est[i, 1]),
            fontsize=9,
            fontweight="bold",
            color=ant_color,
            zorder=8,
        )

    ax.set_aspect("equal", adjustable="datalim")
    ax.grid(True, linestyle=":", alpha=0.6)
    ax.set_xlabel("X Coordinate", fontsize=11)
    ax.set_ylabel("Y Coordinate", fontsize=11)
    ax.set_title(title, fontsize=13, fontweight="bold", pad=12)

    ax.legend(loc="upper right", framealpha=0.9)

    plt.tight_layout()

    if save_path:
        out_file = Path(save_path)
        if out_file.suffix.lower() != ".pdf":
            out_file = out_file.with_suffix(".pdf")
        out_file.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(out_file, format="pdf", bbox_inches="tight")
        print(f"Saved figure in PDF mode to: {out_file.resolve()}")

    if show:
        plt.show()

    return fig, ax
