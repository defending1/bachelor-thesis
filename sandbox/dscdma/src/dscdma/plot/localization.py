"""
Visualization module for DS-CDMA spatial positions and antenna-centered radius circles.
"""

import itertools
from pathlib import Path
from typing import Optional, Tuple, Union

import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import numpy as np
from scipy.optimize import least_squares

from dscdma.plot.stickman import draw_stickman


def extract_user_positions(
    S_est: np.ndarray,
    A_est: np.ndarray,
    area_side: float = 100.0,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Extracts 2D user positions from the first two rows of estimated signal matrix S_est.
    Resolves column sign flips from CP decomposition ambiguity: since spatial coordinates
    x_r, y_r >= 0, if S_est[0, r] < 0 or S_est[1, r] < 0, the sign of column r is flipped
    in both S_est and A_est.

    Args:
        S_est (np.ndarray): Estimated signal matrix of shape (K, R).
        A_est (np.ndarray): Estimated channel matrix of shape (I, R).
        area_side (float): 2D area side length scale factor (default 100.0).

    Returns:
        Tuple[np.ndarray, np.ndarray, np.ndarray]:
            - user_pos_est: Extracted user 2D coordinates of shape (R, 2)
            - S_corr: Sign-corrected signal matrix of shape (K, R)
            - A_corr: Sign-corrected channel matrix of shape (I, R)
    """
    K, R = S_est.shape
    S_corr = S_est.copy()
    A_corr = A_est.copy()

    user_pos_est = np.zeros((R, 2), dtype=np.float64)

    for r in range(R):
        x_raw = S_corr[0, r]
        y_raw = S_corr[1, r]

        # Resolve sign ambiguity: if either coordinate is negative, flip the column sign
        if x_raw < -1e-6 or y_raw < -1e-6:
            S_corr[:, r] = -S_corr[:, r]
            A_corr[:, r] = -A_corr[:, r]

        x_val = max(S_corr[0, r], 0.0) * area_side
        y_val = max(S_corr[1, r], 0.0) * area_side
        user_pos_est[r] = [x_val, y_val]

    return user_pos_est, S_corr, A_corr


def estimate_antenna_positions(
    S_est: np.ndarray,
    A_est: np.ndarray,
    area_side: float = 100.0,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Estimates 2D antenna positions and user positions from estimated factor matrices (S_est, A_est).
    User positions are automatically extracted from S_est rows 0 and 1.

    Args:
        S_est (np.ndarray): Estimated signal matrix of shape (K, R) where K >= 2.
        A_est (np.ndarray): Estimated channel gain matrix of shape (I, R).
        area_side (float): Area bounding box side length (default 100.0).

    Returns:
        Tuple[np.ndarray, np.ndarray]:
            - antenna_pos_est: Estimated antenna positions of shape (I, 2).
            - user_pos_est: Estimated user positions of shape (R, 2).
    """
    user_pos_est, S_corr, A_corr = extract_user_positions(S_est, A_est, area_side)
    I, R = A_corr.shape

    radii = 1.0 / np.abs(A_corr)

    best_total_cost = float("inf")
    best_antenna_pos_est = np.zeros((I, 2), dtype=np.float64)

    # Evaluate column permutations if R is small (<= 8) to map columns to users
    permutations = (
        list(itertools.permutations(range(R))) if R <= 8 else [tuple(range(R))]
    )

    for perm in permutations:
        u_perm = user_pos_est[list(perm), :]
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

    return best_antenna_pos_est, user_pos_est


def plot_antenna_and_radii(
    user_pos: np.ndarray,
    antenna_pos_true: np.ndarray,
    A_est: np.ndarray,
    S_est: Optional[np.ndarray] = None,
    antenna_pos_est: Optional[np.ndarray] = None,
    title: str = "User & Antenna Positions Recovery using CP-ALS",
    save_path: Optional[str] = None,
    show: bool = False,
    area_side: float = 100.0,
) -> Tuple[plt.Figure, plt.Axes]:
    """
    Plots users as stickmen, ground truth antennae, recovered antennae, and circles of radius
    centered around recovered antenna positions.

    Args:
        user_pos (np.ndarray): User 2D coordinates of shape (R, 2).
        antenna_pos_true (np.ndarray): True antenna 2D coordinates of shape (I, 2).
        A_est (np.ndarray): Estimated channel matrix hat(A) of shape (I, R).
        S_est (Optional[np.ndarray]): Estimated signal matrix hat(S) of shape (K, R).
        antenna_pos_est (Optional[np.ndarray]): Estimated antenna 2D coordinates of shape (I, 2).
        title (str): Title for the plot.
        save_path (Optional[str]): File path to save figure (e.g. 'plot.pdf').
        show (bool): If True, calls plt.show().
        area_side (float): Bounding box size.

    Returns:
        Tuple[plt.Figure, plt.Axes]: Matplotlib figure and axes objects.
    """
    I, R = A_est.shape

    if S_est is None:
        # Construct S_est from user_pos for decoding
        S_est = np.zeros((2, R), dtype=np.float64)
        S_est[0, :] = user_pos[:, 0] / area_side
        S_est[1, :] = user_pos[:, 1] / area_side

    user_pos_est, _, A_corr = extract_user_positions(S_est, A_est, area_side)

    if antenna_pos_est is None:
        antenna_pos_est, _ = estimate_antenna_positions(S_est, A_est, area_side)

    # Radii for recovered antennae R_ir = 1 / |hat(a_ir)|
    radii_est = 1.0 / np.abs(A_corr)

    fig, ax = plt.subplots(figsize=(10, 8))

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

    # 2. Draw stickmen for true user positions and markers for recovered user positions
    for r in range(R):
        draw_stickman(
            ax,
            user_pos[r, 0],
            user_pos[r, 1],
            size=4.0,
            color="royalblue",
            label="True Users" if r == 0 else None,
        )
        ax.annotate(
            f"  U{r + 1} (True)",
            (user_pos[r, 0], user_pos[r, 1] + 3.4),
            fontsize=10,
            fontweight="bold",
            color="navy",
            zorder=7,
        )

        if S_est is not None:
            ax.scatter(
                user_pos_est[r, 0],
                user_pos_est[r, 1],
                color="darkorange",
                marker="o",
                s=100,
                edgecolors="black",
                zorder=7,
                label="Recovered Users (from S)" if r == 0 else None,
            )
            ax.annotate(
                f"  U{r + 1} (Rec)",
                (user_pos_est[r, 0], user_pos_est[r, 1] - 2.5),
                fontsize=9,
                color="darkorange",
                fontweight="bold",
                zorder=8,
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

    # 4. Scatter plot recovered antenna positions
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
