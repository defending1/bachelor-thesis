import matplotlib.pyplot as plt
import numpy as np
import tensorly as tl
from pathlib import Path

from plots.utils import setup_plot_style, get_wavelength_ranges
from cp.decomposition import load_eem_data, fit_cp_with_restarts, align_components

def visualize_eem_cp(mat_path: Path = Path("EEM18.mat"),
                     output_pdf: Path = Path("eem_model.pdf"),
                     output_png: Path = Path("eem_model.png")):
    """
    Fit rank-3 NN-CP model, sort components by weight, align factors with true mixtures,
    and output a publication-quality 3x3 plot of loadings/spectra.
    """
    setup_plot_style()

    data = load_eem_data(mat_path)
    X = data['X']
    mixtures = data['mixtures']
    mode_ranges = data['mode_ranges']

    # 1. Fit CP
    print("Fitting Rank-3 Non-negative CP decomposition...")
    best_cp, _, _ = fit_cp_with_restarts(X, rank=3, n_restarts=5)

    # 2. Extract and Normalize factor matrices to unit L2 norm
    weights, factors = best_cp
    # factors[0] (Samples): (18, 3)
    # factors[1] (Emission): (251, 3)
    # factors[2] (Excitation): (21, 3)

    norm_factors = []
    mode_norms = []
    for mode in range(3):
        col_norms = np.linalg.norm(factors[mode], axis=0)
        mode_norms.append(col_norms)
        norm_factors.append(factors[mode] / col_norms)

    # Move scaling to weights
    weights = weights * np.prod(mode_norms, axis=0)

    # Sort components by weight in descending order
    sorted_idx = np.argsort(weights)[::-1]
    sorted_weights = weights[sorted_idx]
    norm_A = norm_factors[0][:, sorted_idx]
    norm_B = norm_factors[1][:, sorted_idx]
    norm_C = norm_factors[2][:, sorted_idx]

    # Normalize true mixtures columns to unit L2 norm for comparison
    norm_mixtures = mixtures / np.linalg.norm(mixtures, axis=0)

    # 3. Align components using similarity
    matched_mixtures = align_components(norm_A, norm_mixtures)

    # Normalize weights by the maximum weight (which is at index 0 after sorting)
    rel_weights = sorted_weights / sorted_weights[0]

    # Get wavelengths
    em_range, ex_range = get_wavelength_ranges(mode_ranges)

    # Create layout
    fig, axes = plt.subplots(3, 3, figsize=(10, 6.5), sharex='col')

    # Color definitions (MATLAB lines colormap equivalents)
    color_computed = '#0072BD'  # Standard MATLAB blue
    color_true = '#D95319'      # Standard MATLAB orange

    for j in range(3):
        # --- Mode 1: Samples ---
        ax_sample = axes[j, 0]
        x_indices = np.arange(1, 19)
        width = 0.35
        ax_sample.bar(x_indices - width/2, norm_A[:, j], width, color=color_computed, edgecolor='k', linewidth=0.5, label='Computed')
        ax_sample.bar(x_indices + width/2, matched_mixtures[:, j], width, color=color_true, edgecolor='k', linewidth=0.5, label='True')

        ax_sample.set_ylabel("Relative Loading", fontsize=10)
        ax_sample.set_yticks([])  # Hide y-ticks to match MATLAB
        ax_sample.text(-0.35, 0.5, f"{rel_weights[j]:.2f}", transform=ax_sample.transAxes,
                       fontsize=12, fontweight='bold', ha='right', va='center')

        if j == 0:
            ax_sample.legend(loc='upper right', frameon=True, facecolor='white', edgecolor='k', framealpha=0.9)
            ax_sample.set_title("Sample", fontweight='bold', pad=10)
        
        ax_sample.set_xlim([0.5, 18.5])
        ax_sample.set_xticks([5, 10, 15])

        # --- Mode 2: Emission ---
        ax_emission = axes[j, 1]
        ax_emission.plot(em_range, norm_B[:, j], '.-', color=color_computed, linewidth=1, markersize=3)
        ax_emission.axhline(0, color='k', linestyle=':', linewidth=0.8)
        ax_emission.set_xlim([em_range[0], em_range[-1]])
        ax_emission.set_xticks([275, 325, 375, 425, 475])
        ax_emission.set_ylabel("Intensity (a.u.)", fontsize=10)

        if j == 0:
            ax_emission.set_title("Emission", fontweight='bold', pad=10)

        # --- Mode 3: Excitation ---
        ax_excitation = axes[j, 2]
        ax_excitation.plot(ex_range, norm_C[:, j], '.-', color=color_computed, linewidth=1, markersize=3)
        ax_excitation.axhline(0, color='k', linestyle=':', linewidth=0.8)
        ax_excitation.set_xlim([ex_range[0], ex_range[-1]])
        ax_excitation.set_xticks([220, 240, 260, 280, 300])
        ax_excitation.set_ylabel("Intensity (a.u.)", fontsize=10)

        if j == 0:
            ax_excitation.set_title("Excitation", fontweight='bold', pad=10)

    # Bottom labels
    axes[2, 0].set_xlabel("Sample Index", labelpad=8)
    axes[2, 1].set_xlabel("Wavelength (nm)", labelpad=8)
    axes[2, 2].set_xlabel("Wavelength (nm)", labelpad=8)

    plt.tight_layout()
    output_pdf.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_png, dpi=300, bbox_inches='tight')
    plt.savefig(output_pdf, format='pdf', bbox_inches='tight')
    plt.close()
    
    print(f"Successfully generated and saved publication-quality plots:")
    print(f"  PNG: {output_png.resolve()}")
    print(f"  PDF (Vector): {output_pdf.resolve()}")
