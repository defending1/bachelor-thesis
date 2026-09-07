"""
DS-CDMA Tensor Factorization using CP-ALS (TensorLy), Channel Matrix Matching, and Code Matching.
"""

from typing import Tuple, Optional, Union
import numpy as np
from scipy.optimize import linear_sum_assignment

from experiments.utils.cp import CP, solve_cp_als, relative_error


def align_factors(
    cp: CP,
    A_true: np.ndarray,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Finds the optimal column permutation mapping A_true into cp.A via absolute cosine similarity
    and Hungarian matching over S_R, resolving sign ambiguities and updating cp.factors in-place.

    Formulation:
        1. Compute normalized correlation matrix rho_{k, r} = <A_est[:, k], A_true[:, r]> / (||A_est[:, k]|| * ||A_true[:, r]||)
        2. Cost matrix M_{k, r} = 1 - |rho_{k, r}|
        3. Solve optimal bipartite matching (Hungarian algorithm) over S_R
        4. Determine sign multiplier s_r = sign(<A_est_{perm[r]}, A_true_r>)
        5. Reorder and sign-correct factor matrices:
           A_aligned[:, r] = s_r * A_est[:, perm[r]]
           S_aligned[:, r] = s_r * S_est[:, perm[r]]
           C_aligned[:, r] = C_est[:, perm[r]]

    Args:
        cp (CP): Approximate CP tensor factorization object containing factors [A, C, S].
        A_true (np.ndarray): Ground-truth channel matrix of shape (I, R).

    Returns:
        Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
            - A_aligned: Aligned channel factor matrix (I, R).
            - C_aligned: Aligned code factor matrix (J, R).
            - S_aligned: Aligned symbol factor matrix (K, R).
            - perm: Permutation index vector of length R.
            - signs: Sign flipping vector of length R (+1 or -1).
    """
    A_est, C_est, S_est = cp.factors[0], cp.factors[1], cp.factors[2]

    I, R = A_true.shape
    norm_A_est = np.linalg.norm(A_est, axis=0, keepdims=True)  # (1, R)
    norm_A_true = np.linalg.norm(A_true, axis=0, keepdims=True)  # (1, R)

    norm_A_est = np.maximum(norm_A_est, 1e-12)
    norm_A_true = np.maximum(norm_A_true, 1e-12)

    inner_prods = A_est.T @ A_true  # (R, R)
    rho = inner_prods / (norm_A_est.T @ norm_A_true)

    # Cost matrix using absolute correlation: 1 - |rho|
    cost_matrix = 1.0 - np.abs(rho)

    row_ind, col_ind = linear_sum_assignment(cost_matrix)

    perm = np.zeros(R, dtype=int)
    for k_idx, r_idx in zip(row_ind, col_ind):
        perm[r_idx] = k_idx

    signs = np.zeros(R, dtype=np.float64)
    for r_idx in range(R):
        k_idx = perm[r_idx]
        ip = inner_prods[k_idx, r_idx]
        signs[r_idx] = 1.0 if ip >= 0 else -1.0

    A_aligned = A_est[:, perm] * signs[np.newaxis, :]
    C_aligned = C_est[:, perm]
    S_aligned = S_est[:, perm] * signs[np.newaxis, :]

    cp.factors = [A_aligned, C_aligned, S_aligned]

    return A_aligned, C_aligned, S_aligned, perm, signs


__all__ = [
    "solve_cp_als",
    "relative_error",
    "align_factors",
]
