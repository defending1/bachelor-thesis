"""
Visualization module for DS-CDMA spatial positions and antenna-centered radius circles.
"""

from pathlib import Path
from typing import Optional, Tuple
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
import numpy as np
from experiments.dscdma.plot.stickman import (
    draw_stickman,
    StickmanLegendObject,
    HandlerStickman,
)
from experiments.dscdma.solver.localization import extract_user_positions_from_A


def plot_antenna_and_radii(
    user_pos: np.ndarray,
    antenna_pos_true: np.ndarray,
    A_est: np.ndarray,
    S_est: Optional[np.ndarray] = None,
    A_true: Optional[np.ndarray] = None,
    title: str = "Stima della Posizione degli Utenti e delle Antenne",
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




    # Colorblind-safe palette (Okabe-Ito standard for academic publications)
    user_colors = [
        "#0072B2",  # Deep Blue
        "#E69F00",  # Amber / Orange
        "#009E73",  # Bluish Green
        "#CC79A7",  # Reddish Purple
        "#D55E00",  # Vermillion
        "#56B4E9",  # Sky Blue
    ]
    ant_color = "#2C3E50"  # Neutral dark slate for fixed antennas

    # Draw distance circles centered at fixed known antenna positions, color-coded by User (no legend entry)
    for r in range(R):
        u_color = user_colors[r % len(user_colors)]
        for i in range(I):
            c_ant = antenna_pos_true[i]
            radius = radii_est[i, r]
            circle = Circle(
                xy=(c_ant[0], c_ant[1]),
                radius=radius,
                fill=False,
                edgecolor=u_color,
                linestyle=":",
                linewidth=1.0,
                alpha=0.35,
                label=None,
            )
            ax.add_patch(circle)

    # Draw True Users (Empty solid square) and Recovered Users (Stickman)
    sq_side = 4.8
    for r in range(R):
        u_color = user_colors[r % len(user_colors)]

        # Displacement vector line linking True and Recovered position (no legend entry)
        ax.plot(
            [user_pos[r, 0], user_pos_est[r, 0]],
            [user_pos[r, 1], user_pos_est[r, 1]],
            linestyle=":",
            linewidth=1.3,
            color=u_color,
            alpha=0.7,
            zorder=5,
            label=None,
        )

        # True User (Empty solid square)
        sq = Rectangle(
            (user_pos[r, 0] - sq_side * 0.5, user_pos[r, 1] - sq_side * 0.3),
            sq_side,
            sq_side,
            facecolor="none",
            edgecolor=u_color,
            linewidth=2.0,
            linestyle="-",
            zorder=6,
            label="Posizione Utente Reale" if r == 0 else None,
        )
        ax.add_patch(sq)
        ax.annotate(
            rf"  $U_{{{r + 1}}}$",
            (user_pos[r, 0], user_pos[r, 1] + sq_side * 0.55),
            fontsize=10,
            fontweight="bold",
            color=u_color,
            zorder=7,
        )

        # Recovered User (Continuous Stickman)
        draw_stickman(
            ax,
            user_pos_est[r, 0],
            user_pos_est[r, 1],
            size=4.0,
            color=u_color,
            style="continuous",
            linestyle="-",
            fill_head=False,
            alpha=0.95,
            label="Utenti Stimati" if r == 0 else None,
        )
        ax.annotate(
            rf"  $\hat{{U}}_{{{r + 1}}}$",
            (user_pos_est[r, 0], user_pos_est[r, 1] - 2.5),
            fontsize=9,
            fontweight="bold",
            color=u_color,
            alpha=0.95,
            zorder=7,
        )

    # Plot fixed known antenna locations matrix P using neutral dark slate
    for i in range(I):
        ax.scatter(
            antenna_pos_true[i, 0],
            antenna_pos_true[i, 1],
            color=ant_color,
            marker="^",
            s=140,
            edgecolors="black",
            linewidths=1.0,
            zorder=8,
            label="Antenne" if i == 0 else None,
        )
        ax.annotate(
            rf"  $a_{{{i + 1}}}$",
            (antenna_pos_true[i, 0], antenna_pos_true[i, 1] + 1.2),
            fontsize=9,
            fontweight="bold",
            color=ant_color,
            zorder=9,
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
    handles, labels = ax.get_legend_handles_labels()
    new_handles = []
    for h, l in zip(handles, labels):
        if "Recovered" in l or "Extracted" in l or "Utenti" in l:
            new_handles.append(
                StickmanLegendObject(
                    color="#2C3E50", linestyle="-", fill_head=False, label_text=r"$l$"
                )
            )
        else:
            new_handles.append(h)

    ax.legend(
        handles=new_handles,
        labels=labels,
        handler_map={StickmanLegendObject: HandlerStickman()},
        loc="upper center",
        bbox_to_anchor=(0.5, -0.04),
        ncol=3,
        handleheight=1.5,
        handlelength=1.8,
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


def generate_multi_plot_pdf(
    config,
    num_plots: int = 6,
    output_path: str = "dscdma_6_experiments.pdf",
    seeds: Optional[list] = None,
) -> Path:
    """
    Generates a multi-page PDF document containing multiple independent DS-CDMA simulation runs.
    """
    from matplotlib.backends.backend_pdf import PdfPages
    from experiments.dscdma.utils.generator import DSCDMADatasetGenerator
    from experiments.utils.cp import CP
    from experiments.dscdma.solver import align_factors
    from dataclasses import replace

    out_file = Path(output_path)
    if out_file.suffix.lower() != ".pdf":
        out_file = out_file.with_suffix(".pdf")
    out_file.parent.mkdir(parents=True, exist_ok=True)

    with PdfPages(out_file) as pdf:
        for run_idx in range(num_plots):
            seed = seeds[run_idx] if seeds and run_idx < len(seeds) else None
            run_cfg = replace(config, seed=seed)

            generator = DSCDMADatasetGenerator(run_cfg)
            data = generator.generate()

            T_true = data["tensor"]
            user_pos = data["user_pos"]
            antenna_pos_true = data["antenna_pos"]

            cp = CP(T_true, run_cfg.num_sources).compute(
                n_iter_max=2000,
                tol=1e-9,
                random_state=run_cfg.seed,
            )
            align_factors(cp, data["A_true"])

            title = (
                f"Run {run_idx + 1}/{num_plots}: Antenna & User Recovery "
                f"(R={run_cfg.num_sources}, I={run_cfg.num_antennas}, Seed={seed if seed is not None else 'random'})"
            )

            fig, _ = plot_antenna_and_radii(
                user_pos=user_pos,
                antenna_pos_true=antenna_pos_true,
                A_est=cp.A,
                S_est=cp.S,
                title=title,
                save_path=None,
                show=False,
                area_side=run_cfg.area_side,
            )
            pdf.savefig(fig, bbox_inches="tight")
            plt.close(fig)

    print(f"Successfully generated {num_plots} plots in single PDF: {out_file.resolve()}")
    return out_file


def plot_antenna_localization_multi(
    config,
    num_runs: int = 6,
    seeds: Optional[list] = None,
    title: str = "Stima della Posizione degli Utenti e delle Antenne",
    save_path: Optional[str] = "dscdma_6_experiments.pdf",
    show: bool = False,
) -> Tuple[plt.Figure, np.ndarray]:
    """
    Generates a multi-subfigure grid layout (default 6 subfigures in 2 rows of 3) containing independent runs of the antenna localization experiment.
    Optimized for inclusion in an A4 document. All subfigures share identical coordinate limits
    so that the physical 2D spatial area box is rendered at the exact same size across all subfigures.
    """
    from dataclasses import replace
    from experiments.dscdma.utils.generator import DSCDMADatasetGenerator
    from experiments.utils.cp import CP
    from experiments.dscdma.solver import align_factors

    if seeds is None:
        base_seed = config.seed if config.seed is not None else 42
        seeds = [base_seed + 10 * i for i in range(num_runs)]
    num_runs = len(seeds)
    runs_data = []

    for run_idx, seed in enumerate(seeds):
        run_cfg = replace(config, seed=seed)
        generator = DSCDMADatasetGenerator(run_cfg)
        data = generator.generate()

        cp = CP(data["tensor"], run_cfg.num_sources).compute(
            n_iter_max=2000,
            tol=1e-9,
            random_state=seed,
        )
        align_factors(cp, data["A_true"])

        user_pos_est, scale_factors = extract_user_positions_from_A(
            cp.A, data["antenna_pos"], area_side=run_cfg.area_side
        )

        I, R = cp.A.shape
        radii_est = np.zeros((I, R), dtype=np.float64)
        for r in range(R):
            radii_est[:, r] = scale_factors[r] / np.maximum(np.abs(cp.A[:, r]), 1e-6)

        runs_data.append(
            {
                "user_pos": data["user_pos"],
                "antenna_pos": data["antenna_pos"],
                "user_pos_est": user_pos_est,
                "radii_est": radii_est,
                "seed": seed,
            }
        )

    all_x = []
    all_y = []
    for rdata in runs_data:
        all_x.extend([rdata["antenna_pos"][:, 0], rdata["user_pos"][:, 0], rdata["user_pos_est"][:, 0]])
        all_y.extend([rdata["antenna_pos"][:, 1], rdata["user_pos"][:, 1], rdata["user_pos_est"][:, 1]])
    all_x = np.concatenate(all_x)
    all_y = np.concatenate(all_y)

    min_x, max_x = all_x.min(), all_x.max()
    min_y, max_y = all_y.min(), all_y.max()

    center_x = (min_x + max_x) / 2.0
    center_y = (min_y + max_y) / 2.0
    span = max(max_x - min_x, max_y - min_y)
    margin = max(6.0, span * 0.08)
    half_span = span / 2.0 + margin

    shared_xlim = (center_x - half_span, center_x + half_span)
    shared_ylim = (center_y - half_span, center_y + half_span)

    n_cols = 3
    n_rows = (num_runs + n_cols - 1) // n_cols
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(13.5, 4.2 * n_rows))
    axes_flat = axes.flatten() if isinstance(axes, np.ndarray) else np.array([axes])

    user_colors = ["#0072B2", "#E69F00", "#009E73", "#CC79A7", "#D55E00", "#56B4E9"]
    ant_color = "#2C3E50"
    sq_side = 4.8

    sub_titles = [f"({chr(97 + i)}) Esperimento {i + 1}" for i in range(num_runs)]

    for idx in range(n_rows * n_cols):
        ax = axes_flat[idx]
        if idx >= num_runs:
            ax.axis("off")
            continue

        rdata = runs_data[idx]
        user_pos = rdata["user_pos"]
        antenna_pos_true = rdata["antenna_pos"]
        user_pos_est = rdata["user_pos_est"]
        radii_est = rdata["radii_est"]
        I, R = radii_est.shape

        for r in range(R):
            u_color = user_colors[r % len(user_colors)]
            for i in range(I):
                circle = Circle(
                    xy=(antenna_pos_true[i, 0], antenna_pos_true[i, 1]),
                    radius=radii_est[i, r],
                    fill=False,
                    edgecolor=u_color,
                    linestyle=":",
                    linewidth=1.0,
                    alpha=0.35,
                )
                ax.add_patch(circle)

        for r in range(R):
            u_color = user_colors[r % len(user_colors)]
            ax.plot(
                [user_pos[r, 0], user_pos_est[r, 0]],
                [user_pos[r, 1], user_pos_est[r, 1]],
                linestyle=":",
                linewidth=1.3,
                color=u_color,
                alpha=0.7,
                zorder=5,
            )

            sq = Rectangle(
                (user_pos[r, 0] - sq_side * 0.5, user_pos[r, 1] - sq_side * 0.3),
                sq_side,
                sq_side,
                facecolor="none",
                edgecolor=u_color,
                linewidth=2.0,
                linestyle="-",
                zorder=6,
            )
            ax.add_patch(sq)
            ax.annotate(
                rf"  $U_{{{r + 1}}}$",
                (user_pos[r, 0], user_pos[r, 1] + sq_side * 0.55),
                fontsize=9,
                fontweight="bold",
                color=u_color,
                zorder=7,
            )

            draw_stickman(
                ax,
                user_pos_est[r, 0],
                user_pos_est[r, 1],
                size=3.8,
                color=u_color,
                style="continuous",
                linestyle="-",
                fill_head=False,
                alpha=0.95,
            )
            ax.annotate(
                rf"  $\hat{{U}}_{{{r + 1}}}$",
                (user_pos_est[r, 0], user_pos_est[r, 1] - 2.5),
                fontsize=8.5,
                fontweight="bold",
                color=u_color,
                alpha=0.95,
                zorder=7,
            )

        for i in range(I):
            ax.scatter(
                antenna_pos_true[i, 0],
                antenna_pos_true[i, 1],
                color=ant_color,
                marker="^",
                s=120,
                edgecolors="black",
                linewidths=1.0,
                zorder=8,
            )
            ax.annotate(
                rf"  $a_{{{i + 1}}}$",
                (antenna_pos_true[i, 0], antenna_pos_true[i, 1] + 1.2),
                fontsize=8.5,
                fontweight="bold",
                color=ant_color,
                zorder=9,
            )

        ax.set_xlim(shared_xlim)
        ax.set_ylim(shared_ylim)
        ax.set_aspect("equal", adjustable="box")
        ax.grid(True, linestyle=":", alpha=0.4)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_xlabel("")
        ax.set_ylabel("")
        ax.set_title(sub_titles[idx], fontsize=11, fontweight="bold", pad=8)

    legend_handles = [
        Rectangle((0, 0), 1, 1, facecolor="none", edgecolor="#0072B2", linewidth=2.0),
        StickmanLegendObject(color="#2C3E50", linestyle="-", fill_head=False, label_text=r"$l$"),
        plt.Line2D([0], [0], marker="^", color="w", markerfacecolor=ant_color, markeredgecolor="black", markersize=10),
    ]
    legend_labels = ["Posizione Utente Reale", "Utenti Stimati", "Antenne"]

    fig.legend(
        handles=legend_handles,
        labels=legend_labels,
        handler_map={StickmanLegendObject: HandlerStickman()},
        loc="upper center",
        bbox_to_anchor=(0.5, -0.01),
        ncol=3,
        handleheight=1.5,
        handlelength=1.8,
        frameon=True,
        framealpha=0.95,
        fontsize=10,
    )

    if title:
        fig.suptitle(title, fontsize=13, fontweight="bold", y=1.02)

    plt.tight_layout()

    if save_path:
        out_file = Path(save_path)
        if out_file.suffix.lower() != ".pdf":
            out_file = out_file.with_suffix(".pdf")
        out_file.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(out_file, format="pdf", bbox_inches="tight")
        print(f"Saved {num_runs}-subfigure multi plot to PDF: {out_file.resolve()}")

    if show:
        plt.show()

    return fig, axes


def plot_noise_degradation_trajectory(
    user_pos: np.ndarray,
    antenna_pos_true: np.ndarray,
    extracted_users_per_noise: list[np.ndarray],
    noise_stds: list[float],
    title: str = "Deriva della Localizzazione degli Utenti sotto Rumore Gaussiano",
    save_path: Optional[str] = None,
    show: bool = False,
    area_side: float = 100.0,
    tensor_rms: Optional[float] = None,
    **kwargs,
) -> Tuple[plt.Figure, plt.Axes]:
    """
    Plots ground-truth user locations with distinct user colors, fixed red antennas,
    and translucent user position markers tracking position drift as noise increases.
    Annotations explicitly state the step index, relative noise level (%), and Signal-to-Noise Ratio (SNR in dB).
    """
    R = user_pos.shape[0]
    I = antenna_pos_true.shape[0]
    K_noise = len(extracted_users_per_noise)

    fig, ax = plt.subplots(figsize=(9.0, 7.0))

    # Colorblind-safe palette (Okabe-Ito standard for academic publications)
    user_colors = [
        "#0072B2",  # Deep Blue
        "#E69F00",  # Amber / Orange
        "#009E73",  # Bluish Green
        "#CC79A7",  # Reddish Purple
        "#D55E00",  # Vermillion
        "#56B4E9",  # Sky Blue
    ]
    ant_color = "#2C3E50"  # Neutral dark slate for fixed antennas

    # Plot fixed antenna positions in neutral dark slate
    for i in range(I):
        ax.scatter(
            antenna_pos_true[i, 0],
            antenna_pos_true[i, 1],
            color=ant_color,
            marker="^",
            s=140,
            edgecolors="black",
            linewidths=1.0,
            zorder=8,
            label="Antenne" if i == 0 else None,
        )
        ax.annotate(
            rf"  $a_{{{i + 1}}}$",
            (antenna_pos_true[i, 0], antenna_pos_true[i, 1] + 1.2),
            fontsize=9,
            fontweight="bold",
            color=ant_color,
            zorder=9,
        )

    # Plot ground truth users as empty solid squares (unlabeled)
    sq_side = 4.8
    for r in range(R):
        u_color = user_colors[r % len(user_colors)]
        sq = Rectangle(
            (user_pos[r, 0] - sq_side * 0.5, user_pos[r, 1] - sq_side * 0.3),
            sq_side,
            sq_side,
            facecolor="none",
            edgecolor=u_color,
            linewidth=2.0,
            linestyle="-",
            zorder=6,
            label="Posizione Utente Reale" if r == 0 else None,
        )
        ax.add_patch(sq)

    # Plot recovered users as continuous stickmen for noise steps k >= 1 (k=0 noiseless is omitted)
    for r in range(R):
        u_color = user_colors[r % len(user_colors)]
        traj_x = [extracted_users_per_noise[k][r, 0] for k in range(K_noise)]
        traj_y = [extracted_users_per_noise[k][r, 1] for k in range(K_noise)]

        # Draw Continuous Stickmen for noise steps k >= 1 with high visibility
        for k in range(1, K_noise):
            step_alpha = max(0.70, 1.0 - 0.05 * k)

            draw_stickman(
                ax,
                traj_x[k],
                traj_y[k],
                size=3.6,
                color=u_color,
                style="continuous",
                linestyle="-",
                fill_head=False,
                alpha=step_alpha,
                label=r"Utenti Stimati per $\sigma_l$" if (r == 0 and k == 1) else None,
            )

            # Annotate simple step number (1, 2, 3, ...)
            annotation_str = f"{k}"

            ax.annotate(
                annotation_str,
                (traj_x[k], traj_y[k] - 2.2),
                fontsize=9,
                fontweight="bold",
                color=u_color,
                alpha=step_alpha,
                zorder=9,
            )

    all_x_pts = [antenna_pos_true[:, 0], user_pos[:, 0]]
    all_y_pts = [antenna_pos_true[:, 1], user_pos[:, 1]]
    for k in range(K_noise):
        all_x_pts.append(extracted_users_per_noise[k][:, 0])
        all_y_pts.append(extracted_users_per_noise[k][:, 1])

    all_x = np.concatenate(all_x_pts)
    all_y = np.concatenate(all_y_pts)

    margin_x = max(3.0, (all_x.max() - all_x.min()) * 0.05)
    margin_y = max(3.0, (all_y.max() - all_y.min()) * 0.05)

    ax.set_xlim(all_x.min() - margin_x, all_x.max() + margin_x)
    ax.set_ylim(all_y.min() - margin_y, all_y.max() + margin_y)
    ax.set_aspect("equal", adjustable="box")
    ax.grid(True, linestyle=":", alpha=0.4)

    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel("")
    ax.set_ylabel("")

    ax.set_title(title, fontsize=13, fontweight="bold", pad=12)

    handles, labels = ax.get_legend_handles_labels()
    new_handles = []
    for h, l in zip(handles, labels):
        if "Recovered" in l or "Extracted" in l or "Utenti" in l:
            new_handles.append(
                StickmanLegendObject(
                    color="#2C3E50", linestyle="-", fill_head=False, label_text=r"$l$"
                )
            )
        else:
            new_handles.append(h)

    ax.legend(
        handles=new_handles,
        labels=labels,
        handler_map={StickmanLegendObject: HandlerStickman()},
        loc="upper center",
        bbox_to_anchor=(0.5, -0.04),
        ncol=3,
        handleheight=1.5,
        handlelength=1.8,
        frameon=True,
        framealpha=0.95,
        fontsize=9,
    )
    plt.tight_layout()

    if save_path:
        out_file = Path(save_path)
        if out_file.suffix.lower() != ".pdf":
            out_file = out_file.with_suffix(".pdf")
        out_file.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(out_file, format="pdf", bbox_inches="tight")
        print(f"Saved trajectory figure to: {out_file.resolve()}")

    if show:
        plt.show()

    return fig, ax


def plot_noise_degradation_multi(
    config,
    num_runs: int = 6,
    noise_stds: Optional[list[float]] = None,
    seeds: Optional[list] = None,
    title: str = "Deriva della Localizzazione degli Utenti sotto Rumore Gaussiano",
    save_path: Optional[str] = "dscdma_noise_experiment.pdf",
    show: bool = False,
) -> Tuple[plt.Figure, np.ndarray]:
    """
    Generates a multi-subfigure grid layout (default 6 subfigures in 2 rows of 3) containing independent runs of the Gaussian noise degradation experiment.
    Optimized for inclusion in an A4 document. All subfigures share identical coordinate limits
    so that the physical 2D spatial area box is rendered at the exact same size across all subfigures.
    """
    from dataclasses import replace
    from experiments.dscdma.utils.generator import DSCDMADatasetGenerator, add_gaussian_noise
    from experiments.utils.cp import CP
    from experiments.dscdma.solver import align_factors

    if seeds is None:
        base_seed = config.seed if config.seed is not None else 42
        seeds = [base_seed + 10 * i for i in range(num_runs)]
    num_runs = len(seeds)
    runs_data = []

    for run_idx, seed in enumerate(seeds):
        run_cfg = replace(config, seed=seed)
        generator = DSCDMADatasetGenerator(run_cfg)
        data = generator.generate()

        T_true = data["tensor"]
        user_pos_true = data["user_pos"]
        antenna_pos_true = data["antenna_pos"]
        A_true = data["A_true"]

        tensor_rms = float(np.sqrt(np.mean(T_true ** 2)))

        if noise_stds is None:
            relative_levels = [0.0, 0.15, 0.35, 0.60, 0.90, 1.20]
            run_noise_stds = [rel * tensor_rms for rel in relative_levels]
        else:
            run_noise_stds = noise_stds

        K_noise = len(run_noise_stds)
        extracted_users_per_noise = []
        rng = np.random.default_rng(seed)

        for k, noise_std in enumerate(run_noise_stds):
            T_noisy = add_gaussian_noise(T_true, noise_std=noise_std, rng=rng)
            cp = CP(T_noisy, config.num_sources).compute(
                n_iter_max=2000,
                tol=1e-9,
                random_state=seed,
            )
            align_factors(cp, A_true)

            user_pos_est, _ = extract_user_positions_from_A(
                cp.A, antenna_pos_true, area_side=config.area_side
            )
            extracted_users_per_noise.append(user_pos_est)

        runs_data.append(
            {
                "user_pos": user_pos_true,
                "antenna_pos": antenna_pos_true,
                "extracted_users_per_noise": extracted_users_per_noise,
                "noise_stds": run_noise_stds,
                "seed": seed,
            }
        )

    all_x = []
    all_y = []
    for rdata in runs_data:
        all_x.extend([rdata["antenna_pos"][:, 0], rdata["user_pos"][:, 0]])
        all_y.extend([rdata["antenna_pos"][:, 1], rdata["user_pos"][:, 1]])
        for est in rdata["extracted_users_per_noise"]:
            all_x.append(est[:, 0])
            all_y.append(est[:, 1])

    all_x = np.concatenate(all_x)
    all_y = np.concatenate(all_y)

    min_x, max_x = all_x.min(), all_x.max()
    min_y, max_y = all_y.min(), all_y.max()

    center_x = (min_x + max_x) / 2.0
    center_y = (min_y + max_y) / 2.0
    span = max(max_x - min_x, max_y - min_y)
    margin = max(5.0, span * 0.06)
    half_span = span / 2.0 + margin

    shared_xlim = (center_x - half_span, center_x + half_span)
    shared_ylim = (center_y - half_span, center_y + half_span)

    n_cols = 3
    n_rows = (num_runs + n_cols - 1) // n_cols
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(13.5, 4.2 * n_rows))
    axes_flat = axes.flatten() if isinstance(axes, np.ndarray) else np.array([axes])

    user_colors = ["#0072B2", "#E69F00", "#009E73", "#CC79A7", "#D55E00", "#56B4E9"]
    ant_color = "#2C3E50"
    sq_side = 4.8

    sub_titles = [f"({chr(97 + i)}) Esperimento {i + 1}" for i in range(num_runs)]

    for idx in range(n_rows * n_cols):
        ax = axes_flat[idx]
        if idx >= num_runs:
            ax.axis("off")
            continue

        rdata = runs_data[idx]
        user_pos = rdata["user_pos"]
        antenna_pos_true = rdata["antenna_pos"]
        extracted_users = rdata["extracted_users_per_noise"]
        R = user_pos.shape[0]
        I = antenna_pos_true.shape[0]
        K_noise = len(extracted_users)

        for i in range(I):
            ax.scatter(
                antenna_pos_true[i, 0],
                antenna_pos_true[i, 1],
                color=ant_color,
                marker="^",
                s=120,
                edgecolors="black",
                linewidths=1.0,
                zorder=8,
            )
            ax.annotate(
                rf"  $a_{{{i + 1}}}$",
                (antenna_pos_true[i, 0], antenna_pos_true[i, 1] + 1.2),
                fontsize=8.5,
                fontweight="bold",
                color=ant_color,
                zorder=9,
            )

        for r in range(R):
            u_color = user_colors[r % len(user_colors)]
            sq = Rectangle(
                (user_pos[r, 0] - sq_side * 0.5, user_pos[r, 1] - sq_side * 0.3),
                sq_side,
                sq_side,
                facecolor="none",
                edgecolor=u_color,
                linewidth=2.0,
                linestyle="-",
                zorder=6,
            )
            ax.add_patch(sq)

        for r in range(R):
            u_color = user_colors[r % len(user_colors)]
            traj_x = [extracted_users[k][r, 0] for k in range(K_noise)]
            traj_y = [extracted_users[k][r, 1] for k in range(K_noise)]

            for k in range(1, K_noise):
                step_alpha = max(0.70, 1.0 - 0.05 * k)
                draw_stickman(
                    ax,
                    traj_x[k],
                    traj_y[k],
                    size=3.4,
                    color=u_color,
                    style="continuous",
                    linestyle="-",
                    fill_head=False,
                    alpha=step_alpha,
                )
                ax.annotate(
                    f"{k}",
                    (traj_x[k], traj_y[k] - 2.0),
                    fontsize=8.5,
                    fontweight="bold",
                    color=u_color,
                    alpha=step_alpha,
                    zorder=9,
                )

        ax.set_xlim(shared_xlim)
        ax.set_ylim(shared_ylim)
        ax.set_aspect("equal", adjustable="box")
        ax.grid(True, linestyle=":", alpha=0.4)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_xlabel("")
        ax.set_ylabel("")
        ax.set_title(sub_titles[idx], fontsize=11, fontweight="bold", pad=8)

    legend_handles = [
        Rectangle((0, 0), 1, 1, facecolor="none", edgecolor="#0072B2", linewidth=2.0),
        StickmanLegendObject(color="#2C3E50", linestyle="-", fill_head=False, label_text=r"$l$"),
        plt.Line2D([0], [0], marker="^", color="w", markerfacecolor=ant_color, markeredgecolor="black", markersize=10),
    ]
    legend_labels = ["Posizione Utente Reale", r"Utenti Stimati per $\sigma_l$", "Antenne"]

    fig.legend(
        handles=legend_handles,
        labels=legend_labels,
        handler_map={StickmanLegendObject: HandlerStickman()},
        loc="upper center",
        bbox_to_anchor=(0.5, -0.01),
        ncol=3,
        handleheight=1.5,
        handlelength=1.8,
        frameon=True,
        framealpha=0.95,
        fontsize=10,
    )

    if title:
        fig.suptitle(title, fontsize=13, fontweight="bold", y=1.02)

    plt.tight_layout()

    if save_path:
        out_file = Path(save_path)
        if out_file.suffix.lower() != ".pdf":
            out_file = out_file.with_suffix(".pdf")
        out_file.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(out_file, format="pdf", bbox_inches="tight")
        print(f"Saved {num_runs}-subfigure noise plot to PDF: {out_file.resolve()}")

    if show:
        plt.show()

    return fig, axes


def generate_dscdma_noise_experiment_pdf(
    config,
    noise_stds: Optional[list[float]] = None,
    output_path: str = "dscdma_noise_experiment.pdf",
) -> Path:
    """
    Runs the DS-CDMA Gaussian noise experiment for a single experiment run
    and generates the overlaid trajectory plot.
    """
    from experiments.dscdma.utils.generator import DSCDMADatasetGenerator, add_gaussian_noise
    from experiments.utils.cp import CP
    from experiments.dscdma.solver import align_factors

    generator = DSCDMADatasetGenerator(config)
    data = generator.generate()

    T_true = data["tensor"]
    user_pos_true = data["user_pos"]
    antenna_pos_true = data["antenna_pos"]
    A_true = data["A_true"]

    tensor_rms = float(np.sqrt(np.mean(T_true ** 2)))

    if noise_stds is None:
        relative_levels = [0.0, 0.15, 0.35, 0.60, 0.90, 1.20]
        noise_stds = [rel * tensor_rms for rel in relative_levels]

    K_noise = len(noise_stds)
    extracted_users_per_noise = []
    rng = np.random.default_rng(config.seed if config.seed is not None else 42)

    for k, noise_std in enumerate(noise_stds):
        T_noisy = add_gaussian_noise(T_true, noise_std=noise_std, rng=rng)
        cp = CP(T_noisy, config.num_sources).compute(
            n_iter_max=2000,
            tol=1e-9,
            random_state=config.seed,
        )
        align_factors(cp, A_true)

        user_pos_est, _ = extract_user_positions_from_A(
            cp.A, antenna_pos_true, area_side=config.area_side
        )
        extracted_users_per_noise.append(user_pos_est)

    traj_title = f"Deriva della Localizzazione degli Utenti sotto Rumore Gaussiano (R={config.num_sources}, I={config.num_antennas})"

    fig_traj, _ = plot_noise_degradation_trajectory(
        user_pos=user_pos_true,
        antenna_pos_true=antenna_pos_true,
        extracted_users_per_noise=extracted_users_per_noise,
        noise_stds=noise_stds,
        title=traj_title,
        save_path=output_path,
        show=False,
        area_side=config.area_side,
        tensor_rms=tensor_rms,
    )
    plt.close(fig_traj)
    out_file = Path(output_path)
    print(f"\nSUCCESS: Single noise experiment PDF saved to: {out_file.resolve()}")
    return out_file


def generate_dscdma_noise_multi_experiment_pdf(
    config,
    num_runs: int = 6,
    noise_stds: Optional[list[float]] = None,
    output_path: str = "dscdma_noise_experiment_multi.pdf",
) -> Path:
    """
    Runs the DS-CDMA Gaussian noise experiment across 6 independent experiment runs
    and generates a single A4-friendly PDF figure with 6 subfigures (2x3 grid).
    """
    fig, _ = plot_noise_degradation_multi(
        config=config,
        num_runs=num_runs,
        noise_stds=noise_stds,
        save_path=output_path,
        show=False,
    )
    plt.close(fig)
    out_file = Path(output_path)
    print(f"\nSUCCESS: Multi noise experiment PDF saved to: {out_file.resolve()}")
    return out_file









