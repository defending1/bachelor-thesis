"""
Spreading code generation module using Walsh-Hadamard matrices.

This module provides functions to construct orthogonal spreading matrices C for DS-CDMA
without external dependencies beyond NumPy.
"""

import numpy as np


def _hadamard_matrix(n: int) -> np.ndarray:
    """
    Constructs a Sylvester-type Hadamard matrix of order n using pure NumPy.

    Args:
        n (int): Order of Hadamard matrix (must be a power of 2).

    Returns:
        np.ndarray: Hadamard matrix of shape (n, n) with values in {-1.0, +1.0}.
    """
    H = np.array([[1.0]], dtype=np.float64)
    while H.shape[0] < n:
        H = np.block([[H, H], [H, -H]])
    return H


def generate_walsh_codes(spreading_gain: int, num_sources: int) -> np.ndarray:
    """
    Generates a J x R matrix C containing orthogonal Walsh-Hadamard spreading sequences.

    Args:
        spreading_gain (int): Spreading factor (J). Must be a power of 2.
        num_sources (int): Number of active sources/users (R).

    Returns:
        np.ndarray: Matrix C of shape (J, R) with entries in {-1, +1}.

    Raises:
        ValueError: If J is not a power of 2 or if R > J.
    """
    if spreading_gain <= 0 or (spreading_gain & (spreading_gain - 1)) != 0:
        raise ValueError(f"Spreading gain J must be a power of 2, got {spreading_gain}")
    if num_sources > spreading_gain:
        raise ValueError(f"Number of sources R ({num_sources}) cannot exceed J ({spreading_gain})")

    # Generate full Hadamard matrix of size J x J
    full_hadamard = _hadamard_matrix(spreading_gain)

    # Select the first R columns as spreading sequences
    spreading_matrix = full_hadamard[:, :num_sources]
    return spreading_matrix
