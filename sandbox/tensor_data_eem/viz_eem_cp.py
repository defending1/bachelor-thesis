#!/usr/bin/env python3
"""
Publication-Quality EEM CP Decomposition Visualization (Python port of MATLAB viz_eem_cp).

This script performs rank-3 Non-negative CP decomposition of the EEM dataset,
aligns the computed components with the true mixtures, and generates a publication-quality
3x3 grid of subplots matching the MATLAB visualization structure.
"""

from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import scipy.io as sio
import tensorly as tl
from tensorly.decomposition import non_negative_parafac
from scipy.optimize import linear_sum_assignment

# Use SciencePlots for publication quality if available
try:
    import scienceplots
    plt.style.use(['science', 'no-latex'])
except Exception as e:
    print(f"SciencePlots warning: {e}. Falling back to default matplotlib style.")
    plt.style.use('default')

# Adjust default font settings for clean publication plots
plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Computer Modern Roman', 'DejaVu Serif', 'Times New Roman', 'serif'],
    'axes.labelsize': 11,
    'axes.titlesize': 12,
    'xtick.labelsize': 9.5,
    'ytick.labelsize': 9.5,
    'legend.fontsize': 9.5,
})


def load_eem_data(mat_path: Path):
    """Load preprocessed EEM tensor data and mixtures from EEM18.mat."""
    if not mat_path.exists():
        raise FileNotFoundError(f"Dataset file not found at {mat_path}")

    mat = sio.loadmat(str(mat_path))

    # Extract X (MatlabObject / struct with field 'data')
    x_obj = mat['X'][0, 0]
    x_tensor = np.asarray(x_obj['data'], dtype=np.float64)
    mixtures = mat['mixtures']  # Shape (18, 3)
    mode_ranges = mat.get('mode_ranges', None)

    return x_tensor, mixtures, mode_ranges


def align_components(computed_A: np.ndarray, true_mixtures: np.ndarray):
    """
    Find the optimal permutation of the computed components to match the true mixtures,
    based on cosine similarity (maximizing absolute dot product).
    """
    # Normalize columns to unit L2 norm
    comp_norm = computed_A / np.linalg.norm(computed_A, axis=0, keepdims=True)
    true_norm = true_mixtures / np.linalg.norm(true_mixtures, axis=0, keepdims=True)

    # Compute similarity matrix
    similarity = np.abs(comp_norm.T @ true_norm)

    # Use Hungarian algorithm to find best matching
    row_ind, col_ind = linear_sum_assignment(-similarity)

    # Reorder computed components: permutation[j] is the computed component that maps to true mixture j
    permutation = np.zeros(len(col_ind), dtype=int)
    permutation[col_ind] = row_ind

    return permutation


def main():
    script_dir = Path(__file__).parent
    mat_path = script_dir / "EEM18.mat"
    output_png = Path("/home/alberto/Data/pisa/tesi/Sources/Chapter4/figures/eem_model.png")
    output_pdf = Path("/home/alberto/Data/pisa/tesi/Sources/Chapter4/figures/eem_model.pdf")

    X, mixtures, mode_ranges = load_eem_data(mat_path)

    # Fit Rank-3 Non-negative CP with multiple restarts to avoid local minima
    print("Fitting Rank-3 Non-negative CP decomposition...")
    best_error = float('inf')
    best_cp = None
    x_norm = tl.norm(X)

    for trial in range(5):
        random_state = 42 + trial * 100
        cp_tensor = non_negative_parafac(
            X, rank=3, n_iter_max=1000, tol=1e-7,
            init='random', random_state=random_state
        )
        reconstruction = tl.cp_to_tensor(cp_tensor)
        rel_error = float(tl.norm(X - reconstruction) / x_norm)
        if rel_error < best_error:
            best_error = rel_error
            best_cp = cp_tensor

    _, factors = best_cp
    # factors[0]: Sample loadings (18, 3)
    # factors[1]: Emission spectra (251, 3)
    # factors[2]: Excitation spectra (21, 3)

    # 1. Normalize the columns of each factor matrix and accumulate the scales in weights
    n_modes = len(factors)
    rank = 3
    computed_weights = np.ones(rank)
    norm_factors = []
    for mode in range(n_modes):
        factor = factors[mode]
        col_norms = np.linalg.norm(factor, axis=0)
        # Avoid division by zero
        col_norms = np.where(col_norms == 0, 1e-12, col_norms)
        computed_weights *= col_norms
        norm_factors.append(factor / col_norms)

    # 2. Sort components by weight (scale) in descending order to match MATLAB's output order
    sort_idx = np.argsort(computed_weights)[::-1]
    sorted_weights = computed_weights[sort_idx]
    norm_A = norm_factors[0][:, sort_idx]
    norm_B = norm_factors[1][:, sort_idx]
    norm_C = norm_factors[2][:, sort_idx]

    # Normalize true mixtures to unit L2 norm
    norm_mixtures = mixtures / np.linalg.norm(mixtures, axis=0, keepdims=True)

    # 3. For each sorted computed component, find the best matching true mixture column
    # (maximizing cosine similarity) so we can plot them side-by-side
    matched_mixtures = np.zeros_like(norm_A)
    for j in range(3):
        similarities = [np.abs(np.dot(norm_A[:, j], norm_mixtures[:, k])) for k in range(3)]
        best_k = np.argmax(similarities)
        matched_mixtures[:, j] = norm_mixtures[:, best_k]
        print(f"Computed component {j} (weight: {sorted_weights[j]:.2f}) matched to true mixture column {best_k}")

    # Relative weights (row labels on the left), normalized by the maximum weight (which is at index 0 after sorting)
    rel_weights = sorted_weights / sorted_weights[0]

    # Setup wavelengths
    em_range = np.linspace(250, 500, 251) if mode_ranges is None else mode_ranges[0, 1].squeeze()
    ex_range = np.linspace(210, 310, 21) if mode_ranges is None else mode_ranges[0, 2].squeeze()

    # Create the 3x3 subplot layout
    fig, axes = plt.subplots(3, 3, figsize=(10, 6.5), sharex='col')

    # Color definitions (MATLAB lines colormap equivalents)
    color_computed = '#0072BD'  # Standard MATLAB blue
    color_true = '#D95319'      # Standard MATLAB orange

    for j in range(3):
        # --- Mode 1: Samples ---
        ax_sample = axes[j, 0]
        # Plot grouped bar chart
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
        
        # Configure x-axis for samples
        ax_sample.set_xlim([0.5, 18.5])
        ax_sample.set_xticks([5, 10, 15])

        # --- Mode 2: Emission ---
        ax_emission = axes[j, 1]
        ax_emission.plot(em_range, norm_B[:, j], '.-', color=color_computed, linewidth=1, markersize=3)
        ax_emission.axhline(0, color='k', linestyle=':', linewidth=0.8)
        ax_emission.set_xlim([250, 500])
        ax_emission.set_xticks([275, 325, 375, 425, 475])
        ax_emission.set_ylabel("Intensity (a.u.)", fontsize=10)

        if j == 0:
            ax_emission.set_title("Emission", fontweight='bold', pad=10)

        # --- Mode 3: Excitation ---
        ax_excitation = axes[j, 2]
        ax_excitation.plot(ex_range, norm_C[:, j], '.-', color=color_computed, linewidth=1, markersize=3)
        ax_excitation.axhline(0, color='k', linestyle=':', linewidth=0.8)
        ax_excitation.set_xlim([210, 310])
        ax_excitation.set_xticks([220, 240, 260, 280, 300])
        ax_excitation.set_ylabel("Intensity (a.u.)", fontsize=10)

        if j == 0:
            ax_excitation.set_title("Excitation", fontweight='bold', pad=10)

    # Set bottom labels
    axes[2, 0].set_xlabel("Sample Index", labelpad=8)
    axes[2, 1].set_xlabel("Wavelength (nm)", labelpad=8)
    axes[2, 2].set_xlabel("Wavelength (nm)", labelpad=8)

    plt.tight_layout()
    plt.savefig(output_png, dpi=300, bbox_inches='tight')
    plt.savefig(output_pdf, format='pdf', bbox_inches='tight')
    print(f"Successfully generated and saved publication-quality plots:")
    print(f"  PNG: {output_png.resolve()}")
    print(f"  PDF (Vector): {output_pdf.resolve()}")


if __name__ == '__main__':
    main()
