#!/usr/bin/env python3
"""
Publication-Quality EEM Tensor Slices Visualization (Python equivalent of MATLAB viz_slices).

Replicates viz_slices(X, mixtures, 1, 'X-slices') with SciencePlots publication styling
and exports vector PDF ('X-slices.pdf') and PNG ('X-slices.png').

Usage via uv:
    uv run python viz_slices.py
"""

from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import scipy.io as sio

# Use SciencePlots for publication quality if available
try:
    import scienceplots
    plt.style.use(['science', 'no-latex', 'grid'])
except Exception as e:
    print(f"SciencePlots warning: {e}. Falling back to standard publication style.")
    plt.style.use('default')


def visualize_eem_slices(mat_path: Path = Path("EEM18.mat"),
                          output_pdf: Path = Path("X-slices.pdf"),
                          output_png: Path = Path("X-slices.png"),
                          var_name: str = "X"):
    """
    Generate publication-quality 3x6 grid of EEM tensor slices.
    """
    if not mat_path.exists():
        raise FileNotFoundError(f"MAT file not found: {mat_path}")

    mat = sio.loadmat(str(mat_path))
    x_obj = mat[var_name][0, 0]
    X = np.asarray(x_obj['data'], dtype=np.float64)  # Shape (18, 251, 21)
    mixtures = mat['mixtures']  # Shape (18, 3)

    # Coordinates
    excitation = np.linspace(210, 310, 21)  # 210:5:310 nm
    emission = np.linspace(250, 500, 251)   # 250:1:500 nm
    XX, YY = np.meshgrid(excitation, emission)

    # Grid dimensions
    n_samples = X.shape[0]
    n_rows, n_cols = 3, 6

    # Global min/max for uniform colorbar scale across all slices
    vmin = 0
    vmax = np.max(X)
    levels = np.linspace(vmin, vmax, 25)

    # Figure dimensions for publication layout
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(14, 7.5), sharex=True, sharey=True)
    axes_flat = axes.flatten()

    cax = None
    for i in range(n_samples):
        ax = axes_flat[i]
        slice_data = X[i, :, :]  # Shape (251, 21)

        # Filled contour plot
        cf = ax.contourf(XX, YY, slice_data, levels=levels, cmap='viridis', extend='both')
        # Subtle contour lines for crisp vector rendering in PDF
        ax.contour(XX, YY, slice_data, levels=levels[::2], colors='k', linewidths=0.3, alpha=0.3)

        # Title with compound mixture concentrations
        c1, c2, c3 = mixtures[i]
        ax.set_title(f"S{i+1}: [{c1:.2f}, {c2:.2f}, {c3:.2f}]", fontsize=8.5, pad=3)

        ax.set_xlim([210, 310])
        ax.set_ylim([250, 500])
        ax.tick_params(axis='both', which='major', labelsize=8)

    # Remove any extra axes if n_samples < rows*cols
    for j in range(n_samples, len(axes_flat)):
        fig.delaxes(axes_flat[j])

    # Shared axis labels
    for row in range(n_rows):
        axes[row, 0].set_ylabel("Emission (nm)", fontsize=10, fontweight='bold')
    for col in range(n_cols):
        axes[n_rows - 1, col].set_xlabel("Excitation (nm)", fontsize=10, fontweight='bold')

    # Colorbar layout
    fig.subplots_adjust(right=0.90, left=0.06, top=0.93, bottom=0.08, hspace=0.30, wspace=0.15)
    cbar_ax = fig.add_axes([0.92, 0.12, 0.018, 0.76])
    cbar = fig.colorbar(cf, cax=cbar_ax)
    cbar.set_label("Fluorescence Intensity (a.u.)", fontsize=10, fontweight='bold')
    cbar.ax.tick_params(labelsize=8)

    fig.suptitle(f"Excitation-Emission Matrix (EEM) Slices - Dataset '{var_name}' (18 Samples)",
                 fontsize=13, fontweight='bold', y=0.98)

    # Save PDF and PNG
    plt.savefig(output_pdf, format='pdf', bbox_inches='tight', dpi=300)
    plt.savefig(output_png, format='png', bbox_inches='tight', dpi=300)
    plt.close()

    print(f"Successfully generated publication-quality slice plots:")
    print(f"  PDF (Vector): {output_pdf.resolve()}")
    print(f"  PNG (Preview): {output_png.resolve()}")


if __name__ == '__main__':
    visualize_eem_slices()
