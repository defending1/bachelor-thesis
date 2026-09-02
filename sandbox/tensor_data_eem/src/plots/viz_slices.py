import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
from pathlib import Path

from plots.colormaps import parula_map
from plots.utils import setup_plot_style, get_wavelength_ranges
from cp.decomposition import load_eem_data

def visualize_eem_slices(mat_path: Path = Path("EEM18.mat"),
                          output_pdf: Path = Path("X-slices.pdf"),
                          output_png: Path = Path("X-slices.png"),
                          var_name: str = "X",
                          sample_indices: list = None,
                          n_rows: int = 18):
    """
    Generate publication-quality stacked vertical grid of all EEM tensor slices
    compressed vertically matching the textbook style (Figure 1.7 in tensor_textbook.pdf / eem slices.png).
    Optimized for high readability when embedded in A4 LaTeX documents at width=0.60\\textwidth.
    """
    # Configure plotting style
    setup_plot_style()

    # Load data using central CP utility
    data = load_eem_data(mat_path)
    X = data[var_name] if var_name in data and data[var_name] is not None else data['X']
    mix = data['mixtures']
    mode_ranges = data['mode_ranges']

    # Get wavelength ranges
    em_range, ex_range = get_wavelength_ranges(mode_ranges)

    if sample_indices is None:
        sample_indices = list(range(min(n_rows, X.shape[0])))

    n_samples = len(sample_indices)

    # For 18 rows at 0.60\\textwidth, set tick_fontsize to exactly 13pt
    if n_samples >= 12:
        fig_width, fig_height = 6.0, 13.0
        strip_fontsize = 15.5
        box_y = 0.84
        hspace = 0.16
        tick_fontsize = 13.0
        axis_fontsize = 16.5
    else:
        fig_width, fig_height = 6.0, max(4.0, n_samples * 1.25)
        strip_fontsize = 16.0
        box_y = 0.88
        hspace = 0.18
        tick_fontsize = 13.0
        axis_fontsize = 17.0

    fig, axes = plt.subplots(n_samples, 1, figsize=(fig_width, fig_height), sharex=True, sharey=True)

    if n_samples == 1:
        axes = [axes]

    # Global min/max for uniform colorbar scale across all slices
    vmin = 0
    vmax = np.max(X)
    levels = np.linspace(vmin, vmax, 40)

    cf = None
    for idx, s_i in enumerate(sample_indices):
        ax = axes[idx]
        slice_data = X[s_i, :, :]  # Shape (251, 21)

        # Filled contour plot with parula colormap
        cf = ax.contourf(em_range, ex_range, slice_data.T, levels=levels, cmap=parula_map, extend='both')
        # Subtle contour lines for crisp vector rendering in PDF
        ax.contour(em_range, ex_range, slice_data.T, levels=levels[::4], colors='k', linewidths=0.2, alpha=0.25)

        # Concentration text in top-right corner in white without frame
        c1, c2, c3 = mix[s_i]
        box_text = f"{c1:.2f} / {c2:.2f} / {c3:.2f}"
        ax.text(0.97, box_y, box_text, transform=ax.transAxes, fontsize=strip_fontsize, fontweight='bold',
                color='white', va='top', ha='right')

        ax.set_yticks([230, 280])
        ax.set_ylim([ex_range[0], ex_range[-1]])
        ax.set_xlim([em_range[0], em_range[-1]])
        ax.tick_params(axis='both', which='major', labelsize=tick_fontsize)

    # Shared bottom X-axis tick labels (13pt)
    axes[-1].set_xticks(np.arange(250, 501, 10))
    axes[-1].set_xticklabels([str(x) for x in np.arange(250, 501, 10)], rotation=90, fontsize=tick_fontsize, fontweight='normal')

    # Grid layout spacing with added padding between subplots
    fig.subplots_adjust(left=0.15, right=0.82, top=0.96, bottom=0.08, hspace=hspace)

    # Colorbar layout matching textbook style with scientific exponent \times 10^5
    cbar_ax = fig.add_axes([0.84, 0.08, 0.035, 0.88])
    formatter = ticker.ScalarFormatter(useMathText=True)
    formatter.set_scientific(True)
    formatter.set_powerlimits((5, 5))

    cbar = fig.colorbar(cf, cax=cbar_ax, format=formatter)
    cbar.ax.tick_params(labelsize=tick_fontsize)
    cbar.set_ticks(np.linspace(0, 6e5, 7))
    cbar.ax.yaxis.get_offset_text().set_fontsize(strip_fontsize)
    cbar.ax.yaxis.get_offset_text().set_fontweight('bold')

    # Shared axis labels
    fig.text(0.02, 0.52, "Excitation wavelength (nm)", va="center", rotation="vertical", fontsize=axis_fontsize, fontweight="bold")
    axes[-1].set_xlabel("Emission wavelength (nm)", fontsize=axis_fontsize, fontweight="bold", labelpad=8)

    # Save PDF and PNG
    output_pdf.parent.mkdir(parents=True, exist_ok=True)
    output_png.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_pdf, format='pdf', bbox_inches='tight', dpi=300)
    plt.savefig(output_png, format='png', bbox_inches='tight', dpi=300)
    plt.close()
    print(f"Saved EEM Slices visualization ({n_samples} rows) to:")
    print(f"  PDF: {output_pdf}")
    print(f"  PNG: {output_png}")
