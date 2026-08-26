import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

from plots.colormaps import parula_map
from plots.utils import setup_plot_style, get_wavelength_ranges
from cp.decomposition import load_eem_data

def visualize_eem_piled(mat_path: Path = Path("EEM18.mat"),
                         output_pdf: Path = Path("piled_tensor.pdf"),
                         output_png: Path = Path("piled_tensor.png"),
                         step: int = 14):
    """
    Generate a publication-quality 3D piled representation of the EEM tensor,
    matching the textbook style.
    """
    # Configure plotting style
    setup_plot_style()

    # Load data using central CP utility
    data = load_eem_data(mat_path)
    X = data['X']
    mode_ranges = data['mode_ranges']

    # Get wavelength ranges
    em_range, ex_range = get_wavelength_ranges(mode_ranges)
    sample_range = np.arange(1, 19)

    fig = plt.figure(figsize=(10, 4.5))
    ax = fig.add_subplot(111, projection='3d')
    fig.subplots_adjust(left=-0.03, right=1.03, bottom=-0.03, top=1.03)

    # Hide default axis ticks, plane, background, and grid
    ax.set_axis_off()

    # Choose slice indices
    slice_indices = np.arange(0, len(em_range), step)
    print(f"Generating piled tensor visualization: {len(slice_indices)} slices with step {step}")

    vmax = np.max(X)
    vmin = np.min(X)

    # Grid for the slices (YY is excitations, ZZ is samples)
    YY, ZZ = np.meshgrid(ex_range, sample_range)

    # Draw slices
    for idx in slice_indices:
        em_val = em_range[idx]
        slice_data = X[:, idx, :]  # Shape: (18, 21)

        # Normalize slice data to [0, 1] relative to the overall tensor maximum
        norm_data = (slice_data - vmin) / (vmax - vmin)
        colors = parula_map(norm_data)

        # Apply non-linear opacity mapping for depth clarity (more visible slices)
        base_alpha = 0.22
        colors[..., 3] = base_alpha + (0.90 - base_alpha) * (norm_data ** 1.2)

        XX = np.full_like(YY, em_val)

        # Plot 3D surface representing the lateral slice panel
        ax.plot_surface(XX, YY, ZZ, facecolors=colors, shade=False,
                        rstride=1, cstride=1, antialiased=True,
                        edgecolor='none', linewidth=0)

        # Draw a subtle violet outline around the panel
        bx = [em_val, em_val, em_val, em_val, em_val]
        by = [ex_range[0], ex_range[-1], ex_range[-1], ex_range[0], ex_range[0]]
        bz = [sample_range[0], sample_range[0], sample_range[-1], sample_range[-1], sample_range[0]]
        ax.plot3D(bx, by, bz, color='#3b0066', alpha=0.3, linewidth=0.6)

    # Bounding box limits
    x_min, x_max = em_range[0], em_range[-1]
    y_min, y_max = ex_range[0], ex_range[-1]
    z_min, z_max = sample_range[0], sample_range[-1]

    corners = {
        '000': (x_min, y_min, z_min),
        '100': (x_max, y_min, z_min),
        '110': (x_max, y_max, z_min),
        '010': (x_min, y_max, z_min),
        '001': (x_min, y_min, z_max),
        '101': (x_max, y_min, z_max),
        '111': (x_max, y_max, z_max),
        '011': (x_min, y_max, z_max)
    }

    edges = [
        ('000', '100'), ('100', '110'), ('110', '010'), ('010', '000'), # bottom face
        ('001', '101'), ('101', '111'), ('111', '011'), ('011', '001'), # top face
        ('000', '001'), ('100', '101'), ('110', '111'), ('010', '011')  # vertical edges
    ]

    # Draw the main bounding box wireframe
    for start, end in edges:
        p1 = corners[start]
        p2 = corners[end]
        ax.plot3D([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]],
                  color='#2c0a4d', alpha=0.8, linewidth=1.5)

    # Configure explicit axis limits to prevent clipping of labels and arrows
    ax.set_xlim([228, 555])
    ax.set_ylim([198, 320])
    ax.set_zlim([-1.0, 19])

    # Draw custom arrows and labels for axes
    # 1. 18 samples (vertical, pointing downwards)
    arrow_x = x_min - 3
    arrow_y = y_min - 2
    ax.plot3D([arrow_x, arrow_x], [arrow_y, arrow_y], [z_max, z_min], color='black', linewidth=1.0)
    # Downward arrowhead
    dz = 0.6
    dx = 2.5
    ax.plot3D([arrow_x, arrow_x - dx], [arrow_y, arrow_y], [z_min, z_min + dz], color='black', linewidth=1.0)
    ax.plot3D([arrow_x, arrow_x + dx], [arrow_y, arrow_y], [z_min, z_min + dz], color='black', linewidth=1.0)
    ax.text(arrow_x - 3, arrow_y, (z_max + z_min)/2, "18 samples",
            color='black', fontsize=8, ha='right', va='center', fontfamily='sans-serif', zdir='z')

    # 2. 251 emissions (horizontal, spanning the bottom front edge)
    arrow_z = z_min - 0.4
    arrow_y2 = y_min - 2
    ax.plot3D([x_min, x_max], [arrow_y2, arrow_y2], [arrow_z, arrow_z], color='black', linewidth=1.0)
    # Double-headed arrowheads
    dx_head = 6
    dy_head = 2
    # Left head
    ax.plot3D([x_min, x_min + dx_head], [arrow_y2, arrow_y2 - dy_head], [arrow_z, arrow_z], color='black', linewidth=1.0)
    ax.plot3D([x_min, x_min + dx_head], [arrow_y2, arrow_y2 + dy_head], [arrow_z, arrow_z], color='black', linewidth=1.0)
    # Right head
    ax.plot3D([x_max, x_max - dx_head], [arrow_y2, arrow_y2 - dy_head], [arrow_z, arrow_z], color='black', linewidth=1.0)
    ax.plot3D([x_max, x_max - dx_head], [arrow_y2, arrow_y2 + dy_head], [arrow_z, arrow_z], color='black', linewidth=1.0)
    ax.text((float(x_min) + float(x_max))/2, arrow_y2 - 2, arrow_z - 0.1, "251 emissions",
            color='black', fontsize=8, ha='center', va='top', fontfamily='sans-serif', zdir='x')

    # 3. 21 excitations (diagonal, along bottom right edge, pointing away)
    arrow_x3 = x_max + 3
    arrow_z3 = z_min - 0.3
    ax.plot3D([arrow_x3, arrow_x3], [y_min, y_max], [arrow_z3, arrow_z3], color='black', linewidth=1.0)
    # Arrowhead pointing away (towards y_max) - branch in Z for 3D projection rendering
    dy_head3 = 4
    dz_head3 = 0.3
    ax.plot3D([arrow_x3, arrow_x3], [y_max, y_max - dy_head3], [arrow_z3, arrow_z3 + dz_head3], color='black', linewidth=1.0)
    ax.plot3D([arrow_x3, arrow_x3], [y_max, y_max - dy_head3], [arrow_z3, arrow_z3 - dz_head3], color='black', linewidth=1.0)
    ax.text(arrow_x3 + 3, (float(y_min) + float(y_max))/2, arrow_z3, "21 excitations",
            color='black', fontsize=8, ha='left', va='center', fontfamily='sans-serif', zdir='y')

    # Perspective parameters to match textbook figure 1.7 (X-axis horizontal)
    ax.view_init(elev=10, azim=-70)
    # Zoom in by reducing camera distance to remove empty 3D space
    ax.dist = 2.8

    # Box aspect ratio to represent standard physical dimensions (wider than tall/deep)
    ax.set_box_aspect((3.0, 0.7, 0.9))

    # Save outputs
    output_pdf.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_pdf, format='pdf', bbox_inches='tight', dpi=300)
    plt.savefig(output_png, format='png', bbox_inches='tight', dpi=300)
    plt.close()
    print(f"Saved piled tensor visualization to:")
    print(f"  PDF: {output_pdf}")
    print(f"  PNG: {output_png}")
