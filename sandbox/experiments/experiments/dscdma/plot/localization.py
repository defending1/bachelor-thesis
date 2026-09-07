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
                restore_physical_scale=run_cfg.restore_physical_scale,
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


def plot_noise_degradation_trajectory(
    user_pos: np.ndarray,
    antenna_pos_true: np.ndarray,
    extracted_users_per_noise: list[np.ndarray],
    noise_stds: list[float],
    title: str = "User Position Recovery Trajectory under Increasing Gaussian Noise",
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

    fig, ax = plt.subplots(figsize=(11.5, 8.5))

    # Distinct color per user
    user_colors = [
        "dodgerblue",
        "darkorange",
        "forestgreen",
        "purple",
        "mediumvioletred",
        "teal",
    ]

    # Plot fixed antenna positions in red
    for i in range(I):
        ax.scatter(
            antenna_pos_true[i, 0],
            antenna_pos_true[i, 1],
            color="red",
            marker="^",
            s=140,
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
            color="red",
            zorder=7,
        )

    # Plot ground truth users with distinct user colors
    for r in range(R):
        u_color = user_colors[r % len(user_colors)]
        draw_stickman(
            ax,
            user_pos[r, 0],
            user_pos[r, 1],
            size=4.0,
            color=u_color,
            label=f"User {r + 1} True" if r < 4 else None,
        )
        ax.annotate(
            f"  U{r + 1} (True)",
            (user_pos[r, 0], user_pos[r, 1] + 3.4),
            fontsize=10,
            fontweight="bold",
            color=u_color,
            zorder=7,
        )

    # Plot user position trajectories across noise levels
    for r in range(R):
        u_color = user_colors[r % len(user_colors)]
        traj_x = [extracted_users_per_noise[k][r, 0] for k in range(K_noise)]
        traj_y = [extracted_users_per_noise[k][r, 1] for k in range(K_noise)]

        # Connect trajectory points with a translucent dashed line
        ax.plot(
            traj_x,
            traj_y,
            linestyle="--",
            linewidth=1.5,
            color=u_color,
            alpha=0.5,
            zorder=4,
            label=f"U{r + 1} Drift Trajectory",
        )

        # Plot translucent individual points for each noise level
        for k in range(K_noise):
            noise_val = noise_stds[k]
            marker = "o" if k == 0 else "s"
            size = 110 if k == 0 else 75

            # Translucent user points (alpha=0.55)
            ax.scatter(
                traj_x[k],
                traj_y[k],
                color=u_color,
                alpha=0.55,
                marker=marker,
                s=size,
                edgecolors="black",
                linewidths=0.8,
                zorder=8,
            )

            # Format descriptive noise scale text (Step, Relative %, SNR dB)
            if noise_val == 0.0:
                annotation_str = f" σ{k} (0%, ∞dB)"
            elif tensor_rms is not None and tensor_rms > 0:
                rel = noise_val / tensor_rms
                snr = -20.0 * np.log10(rel)
                annotation_str = f" σ{k} ({rel:.0%}, {snr:.1f}dB)"
            else:
                annotation_str = f" σ{k} ({noise_val:.3f})"

            ax.annotate(
                annotation_str,
                (traj_x[k], traj_y[k]),
                fontsize=8,
                color="black",
                alpha=0.85,
                fontweight="bold" if k == 0 else "normal",
                zorder=9,
            )

    all_x_pts = [antenna_pos_true[:, 0], user_pos[:, 0]]
    all_y_pts = [antenna_pos_true[:, 1], user_pos[:, 1]]
    for k in range(K_noise):
        all_x_pts.append(extracted_users_per_noise[k][:, 0])
        all_y_pts.append(extracted_users_per_noise[k][:, 1])

    all_x = np.concatenate(all_x_pts)
    all_y = np.concatenate(all_y_pts)

    margin_x = max(6.0, (all_x.max() - all_x.min()) * 0.15)
    margin_y = max(6.0, (all_y.max() - all_y.min()) * 0.15)

    ax.set_xlim(all_x.min() - margin_x, all_x.max() + margin_x)
    ax.set_ylim(all_y.min() - margin_y, all_y.max() + margin_y)
    ax.set_aspect("equal", adjustable="box")
    ax.grid(True, linestyle=":", alpha=0.4)

    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel("")
    ax.set_ylabel("")

    ax.set_title(title, fontsize=13, fontweight="bold", pad=12)

    ax.legend(
        loc="upper center",
        bbox_to_anchor=(0.5, -0.04),
        ncol=3,
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


def generate_dscdma_noise_experiment_pdf(
    config,
    noise_stds: Optional[list[float]] = None,
    output_path: str = "dscdma_noise_experiment.pdf",
) -> Path:
    """
    Runs the DS-CDMA Gaussian noise experiment across 6 noise levels (starting at 0 noise).
    Generates a multi-page PDF containing:
      - Page 1: Overlaid Trajectory Plot showing position drift as noise increases.
      - Pages 2-7: Individual localization & distance circle plots for each noise level.
    """
    from matplotlib.backends.backend_pdf import PdfPages
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
        # 6 noise levels: 0% (Noiseless, ∞ dB), 15% (16.5 dB), 35% (9.1 dB), 60% (4.4 dB), 90% (0.9 dB), 120% (-1.6 dB)
        relative_levels = [0.0, 0.15, 0.35, 0.60, 0.90, 1.20]
        noise_stds = [rel * tensor_rms for rel in relative_levels]

    K_noise = len(noise_stds)
    extracted_users_per_noise = []
    cp_results = []

    rng = np.random.default_rng(config.seed if config.seed is not None else 42)

    print(f"\n>>> Running Noise Experiment across {K_noise} noise levels...")
    for k, noise_std in enumerate(noise_stds):
        rel_noise = noise_std / max(1e-12, tensor_rms)
        snr_str = "∞" if rel_noise == 0 else f"{-20.0 * np.log10(rel_noise):.1f}"
        print(f"  [Level {k}/{K_noise - 1}] Noise std σ = {noise_std:.4f} (Rel = {rel_noise:.1%}, SNR = {snr_str} dB)...")
        T_noisy = add_gaussian_noise(T_true, noise_std=noise_std, rng=rng)

        cp = CP(T_noisy, config.num_sources).compute(
            n_iter_max=2000,
            tol=1e-9,
            random_state=config.seed,
            restore_physical_scale=config.restore_physical_scale,
        )
        align_factors(cp, A_true)

        user_pos_est, _ = extract_user_positions_from_A(
            cp.A, antenna_pos_true, area_side=config.area_side
        )

        extracted_users_per_noise.append(user_pos_est)
        cp_results.append((cp, T_noisy))

    out_file = Path(output_path)
    if out_file.suffix.lower() != ".pdf":
        out_file = out_file.with_suffix(".pdf")
    out_file.parent.mkdir(parents=True, exist_ok=True)

    with PdfPages(out_file) as pdf:
        # Page 1: Overlaid trajectory summary plot with detailed noise scale subtitle
        max_rel = noise_stds[-1] / max(1e-12, tensor_rms)
        min_snr = -20.0 * np.log10(max_rel)
        traj_title = (
            f"Overlaid User Trajectory under Increasing Additive Gaussian Noise\n"
            f"(R={config.num_sources}, I={config.num_antennas} | Noise Scale: 0% RMS [∞ dB SNR] → {max_rel:.0%} RMS [{min_snr:.1f} dB SNR])"
        )

        fig_traj, _ = plot_noise_degradation_trajectory(
            user_pos=user_pos_true,
            antenna_pos_true=antenna_pos_true,
            extracted_users_per_noise=extracted_users_per_noise,
            noise_stds=noise_stds,
            title=traj_title,
            save_path=None,
            show=False,
            area_side=config.area_side,
            tensor_rms=tensor_rms,
        )
        pdf.savefig(fig_traj, bbox_inches="tight")
        plt.close(fig_traj)

        # Pages 2 to 7: Detailed per-noise localization plots with distance circles
        for k, noise_std in enumerate(noise_stds):
            cp, _ = cp_results[k]
            rel_noise = noise_std / max(1e-12, tensor_rms)
            if rel_noise == 0:
                snr_desc = "Noiseless Baseline (0% RMS, SNR = ∞ dB)"
            else:
                snr_db = -20.0 * np.log10(rel_noise)
                snr_desc = f"Relative Noise = {rel_noise:.1%} RMS, SNR = {snr_db:.1f} dB"

            page_title = (
                f"Noise Level {k}/{K_noise - 1}: {snr_desc} (σ = {noise_std:.4f})\n"
                f"Tensor Rec. Error: {cp.rec_error:.4e}"
            )
            fig_page, _ = plot_antenna_and_radii(
                user_pos=user_pos_true,
                antenna_pos_true=antenna_pos_true,
                A_est=cp.A,
                S_est=cp.S,
                title=page_title,
                save_path=None,
                show=False,
                area_side=config.area_side,
            )
            pdf.savefig(fig_page, bbox_inches="tight")
            plt.close(fig_page)

    print(f"\nSUCCESS: Noise experiment PDF saved to: {out_file.resolve()}")
    return out_file









