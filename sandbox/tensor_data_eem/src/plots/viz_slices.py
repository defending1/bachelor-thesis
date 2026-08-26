import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

from plots.colormaps import parula_map
from plots.utils import setup_plot_style, get_wavelength_ranges
from cp.decomposition import load_eem_data

def visualize_eem_slices(mat_path: Path = Path("EEM18.mat"),
                          output_pdf: Path = Path("X-slices.pdf"),
                          output_png: Path = Path("X-slices.png"),
                          var_name: str = "X"):
    """
    Generate publication-quality 3x6 grid of EEM tensor slices.
    """
    # Configure plotting style
    setup_plot_style()

    # Load data using central CP utility
    data = load_eem_data(mat_path)
    X = data['X']
    mixtures = data['mixtures']
    mode_ranges = data['mode_ranges']

    # Get wavelength ranges
    em_range, ex_range = get_wavelength_ranges(mode_ranges)
    XX, YY = np.meshgrid(ex_range, em_range)

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

    cf = None
    for i in range(n_samples):
        ax = axes_flat[i]
        slice_data = X[i, :, :]  # Shape (251, 21)

        # Filled contour plot
        cf = ax.contourf(XX, YY, slice_data, levels=levels, cmap=parula_map, extend='both')
        # Subtle contour lines for crisp vector rendering in PDF
        ax.contour(XX, YY, slice_data, levels=levels[::2], colors='k', linewidths=0.3, alpha=0.3)

        # Title with compound mixture concentrations
        c1, c2, c3 = mixtures[i]
        ax.set_title(f"S{i+1}: [{c1:.2f}, {c2:.2f}, {c3:.2f}]", fontsize=8.5, pad=3)

        ax.set_xlim([ex_range[0], ex_range[-1]])
        ax.set_ylim([em_range[0], em_range[-1]])
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
    output_pdf.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_pdf, format='pdf', bbox_inches='tight', dpi=300)
    plt.savefig(output_png, format='png', bbox_inches='tight', dpi=300)
    plt.close()
    print(f"Saved EEM Slices visualization to:")
    print(f"  PDF: {output_pdf}")
    print(f"  PNG: {output_png}")
