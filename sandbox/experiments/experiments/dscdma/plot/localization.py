"""
Visualization module for DS-CDMA spatial positions and antenna-centered radius circles.
"""

from pathlib import Path
from typing import Optional, Tuple
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import numpy as np
from experiments.dscdma.plot.stickman import draw_stickman
from experiments.dscdma.solver.localization import extract_user_positions_from_A


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





