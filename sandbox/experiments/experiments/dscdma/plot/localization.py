"""
Visualization module for DS-CDMA spatial positions and antenna-centered radius circles.
"""

from pathlib import Path
from typing import Optional, Tuple
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import numpy as np
from scipy.optimize import least_squares

from experiments.dscdma.plot.stickman import draw_stickman


def extract_user_positions_from_A(
    A_est: np.ndarray,
    antenna_pos: np.ndarray,
    area_side: float = 100.0,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Extracts 2D user positions by solving non-linear least squares trilateration
    for each column of channel factor A_est against known fixed antenna positions matrix P (antenna_pos).

    Formulation:
        For column r of A_est (shape I, R):
            |a_{i, r}| ~ c_r / ||antenna_pos[i] - u_r||_2

        We solve for u_r = (x_r, y_r) in R^2 and scalar gain c_r > 0:
            min_{u_r, c_r} sum_{i=1}^I (|a_{i, r}| - c_r / ||p_i - u_r||_2)^2

    Args:
        A_est (np.ndarray): Channel gain factor matrix of shape (I, R).
        antenna_pos (np.ndarray): Fixed antenna coordinates matrix P of shape (I, 2).
        area_side (float): Bounding side length of 2D region. Default 100.0.

    Returns:
        Tuple[np.ndarray, np.ndarray]:
            - user_pos_est: Estimated user positions matrix of shape (R, 2).
            - scale_factors: Estimated scalar gain factors c of shape (R,).
    """
    I, R = A_est.shape
    user_pos_est = np.zeros((R, 2), dtype=np.float64)
    scale_factors = np.zeros(R, dtype=np.float64)

    # Multi-start initial candidates to avoid local minima in non-linear least squares
    grid = np.linspace(0.2 * area_side, 0.8 * area_side, 3)
    grid_pts = np.array(np.meshgrid(grid, grid)).T.reshape(-1, 2)
    candidate_inits = np.vstack([np.mean(antenna_pos, axis=0)[np.newaxis, :], antenna_pos, grid_pts])

    for r in range(R):
        a_col = np.abs(A_est[:, r])

        best_cost = float("inf")
        best_pos = np.mean(antenna_pos, axis=0)
        best_c = 1.0

        for init_pos in candidate_inits:
            init_dists = np.linalg.norm(antenna_pos - init_pos, axis=1)
            init_c = float(np.median(a_col * np.maximum(init_dists, 0.1)))
            theta_0 = np.array([init_pos[0], init_pos[1], max(init_c, 1e-3)], dtype=np.float64)

            def residuals(theta: np.ndarray) -> np.ndarray:
                pos = theta[:2]
                c = max(theta[2], 1e-6)
                dists = np.linalg.norm(antenna_pos - pos, axis=1)
                dists = np.maximum(dists, 1e-4)
                expected_a = c / dists
                return a_col - expected_a

            res = least_squares(
                residuals,
                theta_0,
                bounds=([0.0, 0.0, 1e-6], [area_side * 2.0, area_side * 2.0, np.inf]),
            )

            if res.cost < best_cost:
                best_cost = float(res.cost)
                best_pos = res.x[:2]
                best_c = float(res.x[2])

        user_pos_est[r] = best_pos
        scale_factors[r] = best_c

    return user_pos_est, scale_factors


def plot_antenna_and_radii(
    user_pos: np.ndarray,
    antenna_pos_true: np.ndarray,
    A_est: np.ndarray,
    S_est: Optional[np.ndarray] = None,
    A_true: Optional[np.ndarray] = None,
    title: str = "User Position Recovery via Fixed Antenna Trilateration",
    save_path: Optional[str] = None,
    show: bool = False,
    area_side: float = 100.0,
    **kwargs,
) -> Tuple[plt.Figure, plt.Axes]:
    """
    Plots true/extracted user positions and antenna distance circles around fixed known antennas matrix P.
    """
    I, R = A_est.shape

    if A_true is not None:
        from experiments.dscdma.cp_solver import align_factors_by_channel_matching
        C_dummy = np.zeros((1, R))
        S_dummy = np.zeros((1, R)) if S_est is None else S_est
        A_est, _, S_est_aligned, perm, _ = align_factors_by_channel_matching(
            A_est, C_dummy, S_dummy, A_true
        )
        if S_est is not None:
            S_est = S_est_aligned

    user_pos_est, scale_factors = extract_user_positions_from_A(
        A_est, antenna_pos_true, area_side=area_side
    )


    radii_est = np.zeros((I, R), dtype=np.float64)
    for r in range(R):
        c_r = scale_factors[r]
        radii_est[:, r] = c_r / np.maximum(np.abs(A_est[:, r]), 1e-6)

    fig, ax = plt.subplots(figsize=(10, 8))




    # Distinct palette for antennas and their circles (distinct from lightblue user and orange recovered user)
    antenna_palette = [
        "crimson",
        "purple",
        "forestgreen",
        "saddlebrown",
        "mediumvioletred",
        "teal",
        "darkolivegreen",
        "deeppink",
    ]

    # Draw distance circles centered at fixed known antenna positions
    for i in range(I):
        c_ant = antenna_pos_true[i]
        ant_color = antenna_palette[i % len(antenna_palette)]
        for r in range(R):
            radius = radii_est[i, r]
            circle = Circle(
                xy=(c_ant[0], c_ant[1]),
                radius=radius,
                fill=False,
                edgecolor=ant_color,
                linestyle="--",
                linewidth=1.2,
                alpha=0.6,
                label=f"Ant {i + 1} Circles" if r == 0 else None,
            )
            ax.add_patch(circle)

    # Draw true users in lightblue / royalblue
    for r in range(R):
        draw_stickman(
            ax,
            user_pos[r, 0],
            user_pos[r, 1],
            size=4.0,
            color="deepskyblue",
            label="True Users" if r == 0 else None,
        )
        ax.annotate(
            f"  U{r + 1} (True)",
            (user_pos[r, 0], user_pos[r, 1] + 3.4),
            fontsize=10,
            fontweight="bold",
            color="dodgerblue",
            zorder=7,
        )

        # Draw recovered users in orange
        ax.scatter(
            user_pos_est[r, 0],
            user_pos_est[r, 1],
            color="darkorange",
            marker="o",
            s=100,
            edgecolors="black",
            zorder=7,
            label="Extracted Users (from A)" if r == 0 else None,
        )
        ax.annotate(
            f"  U{r + 1} (Rec)",
            (user_pos_est[r, 0], user_pos_est[r, 1] - 2.5),
            fontsize=9,
            color="darkorange",
            fontweight="bold",
            zorder=8,
        )

    # Plot fixed known antenna locations matrix P using distinct colors matching their respective circles
    for i in range(I):
        ant_color = antenna_palette[i % len(antenna_palette)]
        ax.scatter(
            antenna_pos_true[i, 0],
            antenna_pos_true[i, 1],
            color=ant_color,
            marker="^",
            s=130,
            edgecolors="black",
            linewidths=1.0,
            zorder=6,
            label="Fixed Antennas (P)" if i == 0 else None,
        )
        ax.annotate(
            f"  A{i + 1}",
            (antenna_pos_true[i, 0], antenna_pos_true[i, 1]),
            fontsize=9,
            fontweight="bold",
            color=ant_color,
            zorder=7,
        )

    # Calculate tight bounding box around fixed antennas and true/extracted users
    all_x = np.concatenate([antenna_pos_true[:, 0], user_pos[:, 0], user_pos_est[:, 0]])
    all_y = np.concatenate([antenna_pos_true[:, 1], user_pos[:, 1], user_pos_est[:, 1]])

    margin_x = max(6.0, (all_x.max() - all_x.min()) * 0.15)
    margin_y = max(6.0, (all_y.max() - all_y.min()) * 0.15)

    ax.set_xlim(all_x.min() - margin_x, all_x.max() + margin_x)
    ax.set_ylim(all_y.min() - margin_y, all_y.max() + margin_y)
    ax.set_aspect("equal", adjustable="box")
    ax.grid(True, linestyle=":", alpha=0.4)

    # Remove tick marks and numerical axis coordinates
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel("")
    ax.set_ylabel("")

    ax.set_title(title, fontsize=13, fontweight="bold", pad=12)

    # Place legend outside the plot area at the bottom center
    ax.legend(
        loc="upper center",
        bbox_to_anchor=(0.5, -0.04),
        ncol=3,
        frameon=True,
        framealpha=0.95,
        fontsize=10,
    )
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





