"""
Spreading code generation module for DS-CDMA systems.

Generates random binary spreading matrix C of shape (J, R) with entries in {-1.0, +1.0}.
"""

import numpy as np


def generate_spreading_codes(
    spreading_gain: int,
    num_sources: int,
    rng: np.random.Generator,
) -> np.ndarray:
    """
    Generates a J x R matrix C containing random binary spreading sequences in {-1.0, +1.0}.

    Args:
        spreading_gain (int): Spreading factor / chip length (J).
        num_sources (int): Number of active sources/users (R).
        rng (np.random.Generator): NumPy random number generator instance.

    Returns:
        np.ndarray: Real matrix C of shape (J, R) with entries in {-1.0, +1.0}.
    """
    if spreading_gain <= 0:
        raise ValueError(f"Spreading gain J must be > 0, got {spreading_gain}")
    if num_sources <= 0:
        raise ValueError(f"Number of sources R must be > 0, got {num_sources}")

    codes = rng.choice([-1.0, 1.0], size=(spreading_gain, num_sources))
    return codes
