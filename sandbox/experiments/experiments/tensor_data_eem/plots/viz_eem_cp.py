import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import tensorly as tl
from pathlib import Path

from experiments.tensor_data_eem.plots.utils import setup_plot_style, get_wavelength_ranges
from experiments.tensor_data_eem.decomposition import load_eem_data, fit_cp_with_restarts
from experiments.utils.cp import align_components


def visualize_eem_cp(mat_path: Path = Path("EEM18.mat"),
                     output_pdf: Path = Path("eem_model.pdf"),
                     output_png: Path = Path("eem_model.png")):
    setup_plot_style()

    data = load_eem_data(mat_path)
    X = data['X']
    mixtures = data['mixtures']
    mode_ranges = data['mode_ranges']

    print("Fitting Rank-3 Non-negative CP decomposition (stopping tolerance tol=1e-4)...")
    best_cp, best_error, elapsed = fit_cp_with_restarts(X, rank=3, n_restarts=5, tol=1e-4)
    print(f"CP fit complete: Relative Error = {best_error:.6f} in {elapsed:.3f}s")

    weights, factors = best_cp

    norm_factors = []
    mode_norms = []
    for mode in range(3):
        col_norms = np.linalg.norm(factors[mode], axis=0)
        mode_norms.append(col_norms)
        norm_factors.append(factors[mode] / col_norms)

    weights = weights * np.prod(mode_norms, axis=0)

    sorted_idx = np.argsort(weights)[::-1]
    norm_A = norm_factors[0][:, sorted_idx]
    norm_B = norm_factors[1][:, sorted_idx]
    norm_C = norm_factors[2][:, sorted_idx]

    norm_mixtures = mixtures / np.linalg.norm(mixtures, axis=0)

    matched_mixtures_unscaled = align_components(norm_A, mixtures)
    matched_mixtures_norm = align_components(norm_A, norm_mixtures)

    scaled_A = np.zeros_like(norm_A)
    scaled_mixtures = np.zeros_like(matched_mixtures_norm)
    for j in range(3):
        scale_j = np.max(matched_mixtures_unscaled[:, j]) * 1e6
        max_a = np.max(norm_A[:, j])
        scaled_A[:, j] = (norm_A[:, j] / max_a) * scale_j
        scaled_mixtures[:, j] = matched_mixtures_unscaled[:, j] * 1e6

    compound_names = ["Phe", "Trp-Gly", "Val-Tyr-Val"]
    em_range, ex_range = get_wavelength_ranges(mode_ranges)

    fig, axes = plt.subplots(3, 3, figsize=(9.5, 6.8), sharex='col')

    color_computed = '#0072BD'
    color_true = '#D95319'
    color_watermark = '#FDB87D'

    for j in range(3):
        ax_emission = axes[j, 1]
        ax_emission.text(0.5, 0.45, compound_names[j], transform=ax_emission.transAxes,
                        fontsize=50, fontweight='bold', color=color_watermark, alpha=0.50,
                        ha='center', va='center', zorder=0, clip_on=False)

        ax_sample = axes[j, 0]
        x_indices = np.arange(1, 19)
        width = 0.35
        ax_sample.bar(x_indices - width/2, scaled_A[:, j], width, color=color_computed, edgecolor='k', linewidth=0.5, label='Computed', zorder=2)
        ax_sample.bar(x_indices + width/2, scaled_mixtures[:, j], width, color=color_true, edgecolor='k', linewidth=0.5, label='True', zorder=2)

        ax_sample.set_ylabel("")
        ax_sample.set_ylim([0, 7.0e6])
        ax_sample.set_yticks([0, 2e6, 4e6, 6e6])
        ax_sample.set_yticklabels(['0', '2', '4', '6'], fontsize=9)
        ax_sample.text(0.0, 1.04, r"$\cdot 10^6$", transform=ax_sample.transAxes,
                       fontsize=10, ha='left', va='bottom')

        if j == 0:
            ax_sample.legend(loc='upper right', frameon=True, facecolor='white', edgecolor='k', framealpha=0.9)
            ax_sample.set_title("Campione", fontweight='normal', pad=10)

        ax_sample.set_xlim([0.5, 18.5])
        ax_sample.set_xticks([5, 10, 15])

        ax_emission.plot(em_range, norm_B[:, j], '.-', color=color_computed, linewidth=1, markersize=3, zorder=2)
        ax_emission.axhline(0, color='k', linestyle=':', linewidth=0.8, zorder=1)
        ax_emission.set_xlim([em_range[0], em_range[-1]])
        ax_emission.set_xticks([275, 325, 375, 425, 475])
        ax_emission.set_ylabel("")

        if j == 0:
            ax_emission.set_title("Emissione", fontweight='normal', pad=10)

        ax_excitation = axes[j, 2]
        ax_excitation.plot(ex_range, norm_C[:, j], '.-', color=color_computed, linewidth=1, markersize=3, zorder=2)
        ax_excitation.axhline(0, color='k', linestyle=':', linewidth=0.8, zorder=1)
        ax_excitation.set_xlim([ex_range[0], ex_range[-1]])
        ax_excitation.set_xticks([220, 240, 260, 280, 300])
        ax_excitation.set_ylabel("")

        if j == 0:
            ax_excitation.set_title("Eccitazione", fontweight='normal', pad=10)

    axes[2, 0].set_xlabel("Sample Index", labelpad=8)
    axes[2, 1].set_xlabel("Wavelength (nm)", labelpad=8)
    axes[2, 2].set_xlabel("Wavelength (nm)", labelpad=8)

    fig.subplots_adjust(left=0.07, right=0.96, top=0.94, bottom=0.08, wspace=0.20, hspace=0.25)

    output_pdf.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_png, dpi=300, bbox_inches='tight')
    plt.savefig(output_pdf, format='pdf', bbox_inches='tight')
    plt.close()

    print(f"Successfully generated and saved publication-quality plots:")
    print(f"  PNG: {output_png.resolve()}")
    print(f"  PDF (Vector): {output_pdf.resolve()}")
