"""
Plotting and visualization subpackage for DS-CDMA.
"""

from experiments.dscdma.plot.stickman import draw_stickman
from experiments.dscdma.solver.localization import extract_user_positions_from_A
from experiments.dscdma.plot.localization import (
    plot_antenna_and_radii,
    plot_antenna_localization_multi,
    generate_multi_plot_pdf,
    plot_noise_degradation_trajectory,
    plot_noise_degradation_multi,
    generate_dscdma_noise_experiment_pdf,
    generate_dscdma_noise_multi_experiment_pdf,
)

__all__ = [
    "draw_stickman",
    "extract_user_positions_from_A",
    "plot_antenna_and_radii",
    "plot_antenna_localization_multi",
    "generate_multi_plot_pdf",
    "plot_noise_degradation_trajectory",
    "plot_noise_degradation_multi",
    "generate_dscdma_noise_experiment_pdf",
    "generate_dscdma_noise_multi_experiment_pdf",
]






