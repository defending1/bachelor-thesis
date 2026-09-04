"""
Visualization module for DS-CDMA spatial positions and antenna-centered radius circles.
"""

import itertools
from pathlib import Path
from typing import Optional, Tuple
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import numpy as np
from scipy.optimize import least_squares

from experiments.dscdma.plot.stickman import draw_stickman


def extract_user_positions(
    S_est: np.ndarray,
    A_est: np.ndarray,
    area_side: float = 100.0,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    K, R = S_est.shape
    S_corr = S_est.copy()
    A_corr = A_est.copy()

    user_pos_est = np.zeros((R, 2), dtype=np.float64)

    for r in range(R):
        x_raw = S_corr[0, r]
        y_raw = S_corr[1, r]

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
    user_pos_est, S_corr, A_corr = extract_user_positions(S_est, A_est, area_side)
    I, R = A_corr.shape

    radii = 1.0 / np.abs(A_corr)

    best_total_cost = float("inf")
    best_antenna_pos_est = np.zeros((I, 2), dtype=np.float64)

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
    I, R = A_est.shape

    if S_est is None:
        S_est = np.zeros((2, R), dtype=np.float64)
        S_est[0, :] = user_pos[:, 0] / area_side
        S_est[1, :] = user_pos[:, 1] / area_side

    user_pos_est, _, A_corr = extract_user_positions(S_est, A_est, area_side)

    if antenna_pos_est is None:
        antenna_pos_est, _ = estimate_antenna_positions(S_est, A_est, area_side)

    radii_est = 1.0 / np.abs(A_corr)

    fig, ax = plt.subplots(figsize=(10, 8))
    colors = plt.cm.tab10(np.linspace(0, 1, max(I, 10)))

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
