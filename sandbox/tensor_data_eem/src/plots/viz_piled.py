import matplotlib.pyplot as plt
from matplotlib.transforms import Affine2D
import numpy as np
from pathlib import Path

from plots.colormaps import parula_map
from plots.utils import setup_plot_style
from cp.decomposition import load_eem_data

def visualize_eem_piled(mat_path: Path = Path("EEM18.mat"),
                         output_pdf: Path = Path("piled_tensor.pdf"),
                         output_png: Path = Path("piled_tensor.png"),
                         step: int = 14):
    """
    Generate a publication-quality piled 3D-oblique representation of the EEM tensor,
    matching textbook figure 1.7 (eem.png), extended horizontally.
    """
    # Configure plotting style
    setup_plot_style()

    # Load data using central CP utility
    data = load_eem_data(mat_path)
    X = data['X'] # Shape: (18, 251, 21)

    n_samples, n_emissions, n_excitations = X.shape

    # Choose slice indices
    slice_indices = np.arange(0, n_emissions, step)
    if slice_indices[-1] != n_emissions - 1:
        slice_indices = np.append(slice_indices, n_emissions - 1)

    print(f"Generating piled tensor visualization: {len(slice_indices)} slices with step {step}")

    vmax = np.max(X)
    vmin = np.min(X)

    # Setup 2D canvas with equal aspect ratio for precise oblique geometry (extended horizontally)
    fig, ax = plt.subplots(figsize=(15.5, 3.6), dpi=300)
    ax.set_aspect('equal')
    ax.axis('off')

    # Oblique projection geometry matching eem.png (extended horizontal width W = 18.0)
    W = 18.0       # Horizontal width (251 emissions) - extended horizontally
    H = 1.6        # Vertical height (18 samples)
    D = 1.05       # Oblique depth (21 excitations)
    theta = np.radians(38.0) # Angle of depth vector
    cos_t = np.cos(theta)
    sin_t = np.sin(theta)
    dx = D * cos_t
    dy = D * sin_t

    # 1. Outer faces of main cuboid
    top_poly = plt.Polygon([[0, H], [W, H], [W + dx, H + dy], [dx, H + dy]],
                           facecolor='#8e92e3', alpha=0.35, edgecolor='none', zorder=1)
    bot_poly = plt.Polygon([[0, 0], [W, 0], [W + dx, dy], [dx, dy]],
                           facecolor='#8a8de0', alpha=0.30, edgecolor='none', zorder=1)
    back_poly = plt.Polygon([[dx, dy], [W + dx, dy], [W + dx, H + dy], [dx, H + dy]],
                            facecolor='#261c6b', alpha=0.20, edgecolor='none', zorder=1)

    ax.add_patch(bot_poly)
    ax.add_patch(top_poly)
    ax.add_patch(back_poly)

    # 2. Draw lateral slices back-to-front (left to right)
    for idx in slice_indices:
        u_xk = idx / float(n_emissions - 1)
        slice_data = X[:, idx, :]  # Shape: (18, 21)

        # Power-law normalization to enhance visibility of spectral peaks (matching MATLAB / textbook)
        norm_val = np.clip((slice_data - vmin) / (vmax - vmin), 0, 1)
        norm_display = norm_val ** 0.6

        # Map colors with parula
        colors = parula_map(norm_display)

        # Opacity mapping: background slices alpha ~ 0.75, signal peaks ~ 0.95
        alpha = 0.75 + 0.20 * (norm_display ** 0.8)
        colors[..., 3] = alpha

        x_f = u_xk * W

        # 2D affine transform matrix mapping slice rectangle to oblique parallelogram
        tr_matrix = np.array([
            [cos_t, 0.0, x_f],
            [sin_t, 1.0, 0.0],
            [0.0,   0.0, 1.0]
        ])
        tr = Affine2D(tr_matrix) + ax.transData

        ax.imshow(colors, extent=(0, D, 0, H), origin='lower',
                  transform=tr, interpolation='nearest', aspect='auto', zorder=2)

        # Crisp black outline around slice frame
        slice_poly = plt.Polygon([[x_f, 0], [x_f, H], [x_f + dx, H + dy], [x_f + dx, dy]],
                                 facecolor='none', edgecolor='black', linewidth=1.2, zorder=3)
        ax.add_patch(slice_poly)

    # 3. Main cuboid outer wireframe
    # Front face
    ax.plot([0, W, W, 0, 0], [0, 0, H, H, 0], color='black', linewidth=1.8, zorder=5)
    # Back face
    ax.plot([dx, W+dx, W+dx, dx, dx], [dy, dy, H+dy, H+dy, dy], color='black', linewidth=1.8, zorder=5)
    # Connecting edges
    ax.plot([0, dx], [0, dy], color='black', linewidth=1.8, zorder=5)
    ax.plot([W, W+dx], [0, dy], color='black', linewidth=1.8, zorder=5)
    ax.plot([0, dx], [H, H+dy], color='black', linewidth=1.8, zorder=5)
    ax.plot([W, W+dx], [H, H+dy], color='black', linewidth=1.8, zorder=5)

    # 4. Axis labels & arrows matching eem.png
    # Left: 18 samples (vertical line pointing down)
    arrow_x = -0.4
    ax.annotate('', xy=(arrow_x, 0), xytext=(arrow_x, H),
                arrowprops=dict(arrowstyle='->', color='#333333', lw=1.2))
    ax.text(arrow_x - 0.25, H / 2, '18 samples', rotation=90, ha='right', va='center',
            fontsize=11, color='#333333', fontfamily='sans-serif')

    # Bottom: 251 emissions (horizontal line with right arrow)
    arrow_y = -0.4
    ax.annotate('', xy=(W, arrow_y), xytext=(0, arrow_y),
                arrowprops=dict(arrowstyle='->', color='#333333', lw=1.2))
    ax.text(W / 2, arrow_y - 0.35, '251 emissions', ha='center', va='top',
            fontsize=11, color='#333333', fontfamily='sans-serif')

    # Right: 21 excitations (slanted line parallel to depth, label tilted at +50 degrees)
    start_p = (W + 0.25, -0.05)
    end_p = (W + dx + 0.25, dy - 0.05)
    ax.annotate('', xy=end_p, xytext=start_p,
                arrowprops=dict(arrowstyle='->', color='#333333', lw=1.2))

    ax.text(W + dx * 0.25 + 0.275, dy * 0.25 - 0.07, '21 excitations', rotation=50.0,
            ha='left', va='top', fontsize=11, color='#333333', fontfamily='sans-serif')

    ax.set_xlim(-1.2, W + dx + 2.5)
    ax.set_ylim(-1.1, H + dy + 0.2)

    # Save outputs
    output_pdf.parent.mkdir(parents=True, exist_ok=True)
    output_png.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_pdf, format='pdf', bbox_inches='tight', dpi=300)
    plt.savefig(output_png, format='png', bbox_inches='tight', dpi=300)
    plt.close()
    print(f"Saved piled tensor visualization to:")
    print(f"  PDF: {output_pdf}")
    print(f"  PNG: {output_png}")
