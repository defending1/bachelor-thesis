# /// script
# dependencies = [
#   "matplotlib",
#   "numpy",
#   "scienceplots",
# ]
# ///

"""Benchmark plotting script for the matrix multiplication exponent omega timeline (Slide Version).

Optimized for 16:9 presentation slides with larger typography, crisp line widths,
and clear author annotations.
"""

import os
import matplotlib.pyplot as plt
import numpy as np
import scienceplots


def latex_escape(s: str) -> str:
    """Escapes special LaTeX characters for LaTeX rendering."""
    s = s.replace("&", r"\&")
    s = s.replace("ï", r'\"i')
    s = s.replace("ö", r'\"o')
    return s


def main() -> None:
    def s2y(x): return (x - 133.5) / 24.4 + 1970
    def s2o(y): return 3.0 - (y - 28.5) / 1380

    step_data = [
        (1965, 3.0), (1969, 3.0), (1969, 2.8074), (1978, 2.8074), (1978, 2.796),
        (1979, 2.796), (1979, 2.780), (1981, 2.780), (1981, 2.522), (1981, 2.517),
        (1981, 2.496), (1986, 2.496), (1986, 2.479), (1990, 2.479), (1990, 2.3755),
        (2010, 2.3755), (2010, 2.3737), (2012, 2.3737), (2012, 2.3729), (2014, 2.3729),
        (2014, 2.3728639), (2020, 2.3728639), (2020, 2.3728596), (2022, 2.3728596),
        (2022, 2.371866), (2024, 2.371866), (2024, 2.371552), (2024, 2.371339),
        (2026, 2.371339), (2026, 2.371177),
    ]

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
        (2026, 2.371177),
    ]

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
        (1410.8, 900.6, '   Duan, Wu, Zhou', 'black', 0.0),
        (1434.8, 900.6, '   Williams, Xu, Xu, Zhou', 'black', 0.0),
        (1459.8, 900.6, '   Alman, Duan, Williams, Xu, Xu, Zhou', 'black', 0.0),
        (1508.8, 900.6, '   Alman, Vassilevska Williams et al.', 'black', 0.0),
    ]

    plt.style.use(["science"])
    latex_active = True

    # 16:9 slide canvas size (8.5 x 4.8 inches)
    fig, ax = plt.subplots(figsize=(8.5, 4.8), dpi=300)
    ax.set_facecolor("white")

    ax.grid(True, which="major", color="#e2e8f0", linewidth=0.6, linestyle="--", zorder=0)

    years = [p[0] for p in step_data]
    omegas = [p[1] for p in step_data]
    ax.step(years, omegas, where="post", color="#D9534F", linewidth=2.0, zorder=2)

    m_years = [p[0] for p in milestones]
    m_omegas = [p[1] for p in milestones]
    ax.scatter(m_years, m_omegas, color="#D9534F", edgecolors="#D9534F", s=25, linewidths=0.6, zorder=3)

    ax.set_xlim(1965, 2033)
    ax.set_ylim(2.34, 3.09)

    ax.set_xticks(range(1970, 2031, 5))
    ax.set_yticks(np.arange(2.4, 3.05, 0.1))
    ax.get_xaxis().set_major_formatter(plt.ScalarFormatter())

    ax.set_xlabel("Anno", fontsize=12, labelpad=6)
    ax.set_ylabel(r"Esponente $\omega$", fontsize=13, labelpad=6)

    ax.axhline(y=3.0, color="#94a3b8", linestyle="--", linewidth=1.0, zorder=1)
    naive_label = r"$\omega = 3$ (classico)"
    if latex_active:
        naive_label = latex_escape(naive_label)
    ax.text(2032.0, 3.015, naive_label, fontsize=9.5, color="#64748b", ha="right", va="bottom")

    offset_dist = 5.0  # padding distance in points along 60-degree direction
    dx_offset = offset_dist * np.cos(np.radians(60))
    dy_offset = offset_dist * np.sin(np.radians(60))

    for x, y, text, col, dy in labels_data:
        clean_text = text.strip()
        if clean_text == "naive":
            clean_text = "naïve"

        if latex_active:
            display_text = latex_escape(clean_text)
        else:
            display_text = clean_text

        yr = s2y(x)
        om = s2o(y) + dy

        ax.annotate(
            display_text,
            xy=(yr, om),
            xytext=(dx_offset, dy_offset),
            textcoords="offset points",
            fontsize=8.5,
            color=col,
            ha="left",
            va="bottom",
            rotation=60,
            rotation_mode="anchor",
            zorder=4,
        )

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#4A6B82")
    ax.spines["bottom"].set_color("#4A6B82")
    ax.tick_params(axis="both", which="both", length=0, width=0, colors="#4A6B82", labelsize=10)

    plt.tight_layout()

    # Save outputs
    script_dir = os.path.dirname(os.path.abspath(__file__))
    slides_fig_dir = os.path.join(script_dir, "..", "..", "slides", "figures")
    os.makedirs(slides_fig_dir, exist_ok=True)

    pdf_path = os.path.join(slides_fig_dir, "matrix_multiplication_timeline_slides.pdf")
    png_path = os.path.join(slides_fig_dir, "matrix_multiplication_timeline_slides.png")

    fig.savefig(pdf_path, bbox_inches="tight", dpi=300)
    fig.savefig(png_path, bbox_inches="tight", dpi=300)

    print(f"Saved slide plot PDF to: {pdf_path}")
    print(f"Saved slide plot PNG to: {png_path}")

    plt.close(fig)


if __name__ == "__main__":
    main()
