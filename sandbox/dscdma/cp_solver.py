"""
DS-CDMA Tensor Factorization using CP-ALS (TensorLy).

Performs CP decomposition on the 3D real tensor T of shape (I, J, K)
to extract factor matrices (A_est, C_est, S_est) and compute relative reconstruction error.
"""

from typing import Tuple, Optional
import numpy as np
import tensorly as tl
from tensorly.decomposition import parafac


def relative_error(T_true: np.ndarray, T_approx: np.ndarray) -> float:
    """
    Computes Frobenius relative reconstruction error ||T_true - T_approx||_F / ||T_true||_F.
    """
    diff_norm = float(np.linalg.norm(T_true - T_approx))
    true_norm = float(np.linalg.norm(T_true))
    if true_norm == 0:
        return 0.0
    return diff_norm / true_norm


def solve_cp_als(
    tensor: np.ndarray,
    rank: int,
    n_iter_max: int = 2000,
    tol: float = 1e-9,
    random_state: Optional[int] = 42,
) -> Tuple[Tuple[np.ndarray, np.ndarray, np.ndarray], float]:
    """
    Decomposes real 3D tensor T into factor matrices A, C, S using TensorLy CP-ALS.

    Args:
        tensor (np.ndarray): Real tensor T of shape (I, J, K).
        rank (int): CP rank R (number of sources).
        n_iter_max (int): Maximum ALS iterations.
        tol (float): Convergence tolerance.
        random_state (Optional[int]): Random seed for ALS initialization.

    Returns:
        Tuple[Tuple[np.ndarray, np.ndarray, np.ndarray], float]:
            - (A_est, C_est, S_est): Estimated factor matrices of shapes (I, R), (J, R), (K, R)
            - rec_error: Relative tensor reconstruction error ||T - T_rec||_F / ||T||_F
    """
    cp_tensor = parafac(
        tensor,
        rank=rank,
        n_iter_max=n_iter_max,
        tol=tol,
        init='random',
        random_state=random_state,
    )

    weights, factors = cp_tensor
    A_est, C_est, S_est = factors[0], factors[1], factors[2]

    # Reconstruct tensor from CP factors using TensorLy
    T_rec = tl.cp_to_tensor((weights, factors))
    rec_error = relative_error(tensor, T_rec)

    return (A_est, C_est, S_est), rec_error
