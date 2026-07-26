# /// script
# dependencies = [
#   "matplotlib",
#   "numpy",
#   "pandas",
#   "scienceplots",
# ]
# ///

"""Benchmark plotting script for the timeline of the matrix multiplication exponent omega.

Generates a publication-ready line plot showing the historical bounds on omega
since 1969, styled in red with 60-degree diagonal annotations exactly matching example.svg
and translated to Italian for integration into the thesis.
"""

import os
import sys
import matplotlib.pyplot as plt
import numpy as np

import plot_utils


def latex_escape(s: str) -> str:
    """Escapes special LaTeX characters if LaTeX rendering is active."""
    s = s.replace("&", r"\&")
    s = s.replace("ï", r'\"i')
    s = s.replace("ö", r'\"o')
    return s


def main() -> None:
    # SVG-to-data coordinate conversion functions matching example.svg
    def s2y(x): return (x - 133.5) / 24.4 + 1970
    def s2o(y): return 3.0 - (y - 28.5) / 1380

    # 1. Timeline Data (Year, Exponent omega)
    step_data = [
        (1965, 3.0), (1969, 3.0), (1969, 2.8074), (1978, 2.8074), (1978, 2.796),
        (1979, 2.796), (1979, 2.780), (1981, 2.780), (1981, 2.522), (1981, 2.517),
        (1981, 2.496), (1986, 2.496), (1986, 2.479), (1990, 2.479), (1990, 2.3755),
        (2010, 2.3755), (2010, 2.3737), (2012, 2.3737), (2012, 2.3729), (2014, 2.3729),
        (2014, 2.3728639), (2020, 2.3728639), (2020, 2.3728596), (2022, 2.3728596),
        (2022, 2.371866), (2024, 2.371866), (2024, 2.371552), (2024, 2.371339),
    ]

    # Milestones for scatter points: (Year, Exponent)
    milestones = [
        (1969, 2.8074),
        (1978, 2.796),
        (1979, 2.780),
        (1981, 2.522),
        (1981, 2.517),
        (1981, 2.496),
        (1986, 2.479),
        (1990, 2.3755),
        (2010, 2.3737),
        (2012, 2.3729),
        (2014, 2.3728639),
        (2020, 2.3728596),
        (2022, 2.371866),
        (2024, 2.371552),
        (2024, 2.371339),
    ]

    # SVG-matched Label coordinates: (svg_x, svg_y, text, color, dy)
    labels_data = [
        (81.66, 90.63, 'naive   ', 'black', 0.0),
        (115.2, 298.9, '   Strassen', 'black', 0.0),
        (335.5, 313.9, '   Pan', 'black', 0.0),
        (359.5, 335.9, '   Bini, Capovani, Romani, Lotti', 'black', 0.0),
        (334.5, 799.8, 'Schönhage   ', 'black', 0.0),
        (408.6, 699.3, '   Romani', 'black', 0.0),
        (420.6, 728.4, '   Coppersmith, Winograd', 'black', 0.0),
        (530.7, 752.4, '   Strassen', 'black', 0.0),
        (628.8, 895.6, '   Coppersmith, Winograd', 'black', 0.0),
        (1117.4, 897.6, '   Stothers', 'black', 0.0),
        (1166.5, 898.6, '   Williams   ', 'black', 0.0),
        (1215.5, 898.6, '   Le Gall', 'black', 0.0),
        (1361.7, 898.6, '   Alman, Williams', 'black', 0.0),
        (1410.8, 900.6, '   Duan, Wu, Zhou', '#666666', 0.0),
        (1434.8, 900.6, '   Williams, Xu, Xu, Zhou', '#666666', 0.0),
        (1459.8, 900.6, '   Alman, Duan, Williams, Xu, Xu, Zhou', '#666666', 0.0),
    ]

    # Setup matplotlib formatting
    latex_active = plot_utils.setup_matplotlib_style()

    # Create canvas (7.0 x 4.0 inches matching example.svg)
    fig, ax = plt.subplots(figsize=(7.0, 4.0), dpi=300)
    ax.set_facecolor("none")

    # Major grid lines
    ax.grid(True, which="major", color="#e2e8f0", linewidth=0.5, linestyle="--", zorder=0)

    # Red step line matching example.svg
    years = [p[0] for p in step_data]
    omegas = [p[1] for p in step_data]
    ax.step(years, omegas, where="post", color="red", linewidth=1.5, zorder=2)

    # Red milestone points matching example.svg
    m_years = [p[0] for p in milestones]
    m_omegas = [p[1] for p in milestones]
    ax.scatter(m_years, m_omegas, color="red", edgecolors="red", s=18, linewidths=0.5, zorder=3)

    # Limits matching example.svg ticks and spacing
    ax.set_xlim(1965, 2032.5)
    ax.set_ylim(2.35, 3.08)

    ax.set_xticks(range(1970, 2031, 5))
    ax.set_yticks(np.arange(2.4, 3.05, 0.1))
    ax.get_xaxis().set_major_formatter(plt.ScalarFormatter())

    # Translated labels (Italian)
    ax.set_xlabel("Anno", labelpad=5)
    ax.set_ylabel(r"Esponente $\omega$", labelpad=5)

    # Trivial naive bound dashed helper line (translated to Italian)
    ax.axhline(y=3.0, color="#94a3b8", linestyle="--", linewidth=0.8, zorder=1)
    naive_label = r"$\omega = 3$ (classico)"
    if latex_active:
        naive_label = latex_escape(naive_label)
    ax.text(2031.5, 3.015, naive_label, fontsize=8, color="#64748b", ha="right", va="bottom")

    # Annotate milestones rotated by 60 degrees diagonal as in example.svg
    for x, y, text, col, dy in labels_data:
        display_text = text
        if text.strip() == "naive":
            display_text = "naïve" + text[5:] # Keep spaces

        if latex_active:
            display_text = latex_escape(display_text)

        # Convert coordinates
        yr = s2y(x)
        om = s2o(y) + dy

        ax.text(
            yr,
            om,
            display_text,
            fontsize=7.5,
            color=col,
            ha="left",
            va="bottom",
            rotation=60,
            rotation_mode="anchor",
            zorder=4,
        )
    # Clean axes boundary frame
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#64748b")
    ax.spines["bottom"].set_color("#64748b")
    ax.tick_params(colors="#64748b", size=3, width=0.5)

    plt.tight_layout()

    # Save figure inside report/figures and generated/plots
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    output_path = os.path.join(project_root, "generated", "plots", "matrix_multiplication_timeline.pdf")

    plot_utils.save_plot(fig, output_path)

    # Also save as PNG in report/figures/ for quick previews if needed
    report_figures_dir = os.path.join(project_root, "report", "figures")
    png_output_path = os.path.join(report_figures_dir, "matrix_multiplication_timeline.png")
    fig.savefig(png_output_path, bbox_inches="tight", dpi=300)
    print(f"Also saved PNG preview to: {png_output_path}")

    # Copy to thesis directory if present
    thesis_fig_dir = "/home/alberto/Data/pisa/tesi/Sources/Chapter3/figures"
    if os.path.exists(thesis_fig_dir):
        import shutil
        shutil.copy2(os.path.join(project_root, "generated", "plots", "matrix_multiplication_timeline.pdf"),
                     os.path.join(thesis_fig_dir, "matrix_multiplication_timeline.pdf"))
        shutil.copy2(png_output_path,
                     os.path.join(thesis_fig_dir, "matrix_multiplication_timeline.png"))
        print(f"Copied PDF and PNG to thesis figures folder: {thesis_fig_dir}")

    plt.close(fig)


if __name__ == "__main__":
    main()
