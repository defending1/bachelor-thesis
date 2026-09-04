"""
Metrics and norms for CP tensor decomposition.
"""

import numpy as np


def relative_error(T_true: np.ndarray, T_approx: np.ndarray) -> float:
    """
    Computes Frobenius relative reconstruction error ||T_true - T_approx||_F / ||T_true||_F.

    Args:
        T_true (np.ndarray): Original target tensor.
        T_approx (np.ndarray): Reconstructed approximate tensor.

    Returns:
        float: Relative error in [0, inf).
    """
    diff_norm = float(np.linalg.norm(T_true - T_approx))
    true_norm = float(np.linalg.norm(T_true))
    if true_norm == 0.0:
        return 0.0
    return diff_norm / true_norm


def tensor_norm(T: np.ndarray) -> float:
    """
    Computes the Frobenius norm of tensor T.

    Args:
        T (np.ndarray): Input tensor.

    Returns:
        float: Frobenius norm.
    """
    return float(np.linalg.norm(T))
