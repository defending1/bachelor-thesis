import matplotlib.pyplot as plt
import numpy as np

def setup_plot_style():
    """Configure matplotlib globally for publication-quality figures."""
    try:
        import scienceplots
        plt.style.use(['science', 'no-latex'])
    except Exception:
        plt.style.use('default')

    plt.rcParams.update({
        'font.family': 'serif',
        'font.serif': ['Computer Modern Roman', 'DejaVu Serif', 'Times New Roman'],
        'axes.labelsize': 11,
        'axes.titlesize': 12,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'legend.fontsize': 9,
        'figure.titlesize': 13
    })


def get_wavelength_ranges(mode_ranges):
    """
    Extract or generate excitation and emission wavelength ranges.
    
    Parameters:
        mode_ranges: Numpy array containing range information or None.
    Returns:
        em_range: 1D array of emission wavelengths.
        ex_range: 1D array of excitation wavelengths.
    """
    if mode_ranges is not None and len(mode_ranges) > 0:
        em_range = mode_ranges[0, 1].squeeze()
        ex_range = mode_ranges[0, 2].squeeze()
    else:
        # Fallbacks to standard dimensions
        em_range = np.linspace(250, 500, 251)
        ex_range = np.linspace(210, 310, 21)
    
    return em_range, ex_range
