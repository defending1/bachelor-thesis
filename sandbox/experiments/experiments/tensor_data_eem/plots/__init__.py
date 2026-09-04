"""
Plotting module for EEM spectroscopy tensor data.
"""

from experiments.tensor_data_eem.plots.colormaps import parula_map
from experiments.tensor_data_eem.plots.utils import setup_plot_style, get_wavelength_ranges
from experiments.tensor_data_eem.plots.viz_eem_cp import visualize_eem_cp
from experiments.tensor_data_eem.plots.viz_piled import visualize_eem_piled
from experiments.tensor_data_eem.plots.viz_slices import visualize_eem_slices

__all__ = [
    "parula_map",
    "setup_plot_style",
    "get_wavelength_ranges",
    "visualize_eem_cp",
    "visualize_eem_piled",
    "visualize_eem_slices",
]
