"""
Channel gain matrix generation module for line-of-sight DS-CDMA systems.

This module generates the complex antenna gain matrix A of shape (I, R)
where entries are sampled from a complex Gaussian distribution CN(0, 1).
"""

import numpy as np


def generate_channel_matrix(
    num_antennas: int, 
    num_sources: int, 
    rng: np.random.Generator
) -> np.ndarray:
    """
    Generates a complex channel matrix A of shape (I, R) with Rayleigh fading.

    Each entry a_ir = x_ir + j * y_ir is a complex Gaussian variable where
    x_ir, y_ir ~ N(0, 1/2), ensuring E[|a_ir|^2] = 1.

    Args:
        num_antennas (int): Number of receiver antennas (I).
        num_sources (int): Number of active sources/users (R).
        rng (np.random.Generator): NumPy random number generator instance.

    Returns:
        np.ndarray: Complex matrix A of shape (I, R) and dtype complex128.
    """
    real_part = rng.normal(0.0, np.sqrt(0.5), size=(num_antennas, num_sources))
    imag_part = rng.normal(0.0, np.sqrt(0.5), size=(num_antennas, num_sources))
    channel_matrix = real_part + 1j * imag_part
    return channel_matrix
