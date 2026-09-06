"""
DS-CDMA Tensor Factorization using CP-ALS (TensorLy), Channel Matrix Matching, and Code Matching.
"""

from typing import Tuple, Optional, Union
import numpy as np
from scipy.optimize import linear_sum_assignment

from experiments.utils.cp import CP, solve_cp_als, relative_error


def align_factors_by_channel_matching(
    A_est: np.ndarray,
    C_est: np.ndarray,
    S_est: np.ndarray,
    A_true: np.ndarray,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Finds the optimal column permutation mapping A_true into A_est via absolute cosine similarity
    and Hungarian matching over S_R, resolving sign ambiguities to restore positive channel gains.

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
        A_est (np.ndarray): Recovered channel matrix of shape (I, R).
        C_est (np.ndarray): Recovered code matrix of shape (J, R).
        S_est (np.ndarray): Recovered symbol matrix of shape (K, R).
        A_true (np.ndarray): Ground-truth channel matrix of shape (I, R).

    Returns:
        Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
            - A_aligned: Aligned channel factor matrix (I, R).
            - C_aligned: Aligned code factor matrix (J, R).
            - S_aligned: Aligned symbol factor matrix (K, R).
            - perm: Permutation index vector of length R.
            - signs: Sign flipping vector of length R (+1 or -1).
    """
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

    return A_aligned, C_aligned, S_aligned, perm, signs


def align_factors_by_code_matching(
    A_est: np.ndarray,
    C_est: np.ndarray,
    S_est: np.ndarray,
    C_true: np.ndarray,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Permutes and sign-corrects the columns of CP factor matrices (A_est, C_est, S_est)
    by matching recovered code matrix C_est against known true spreading codes C_true.
    """
    J, R = C_true.shape
    norm_C_est = np.linalg.norm(C_est, axis=0, keepdims=True)
    norm_C_est = np.maximum(norm_C_est, 1e-12)

    inner_prods = C_est.T @ C_true  # (R, R)
    rho = inner_prods / (norm_C_est.T * np.sqrt(J))

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
    C_aligned = C_est[:, perm] * signs[np.newaxis, :]
    S_aligned = S_est[:, perm] * signs[np.newaxis, :]

    return A_aligned, C_aligned, S_aligned, perm, signs


def align_factors(
    A_est: Union[np.ndarray, CP],
    C_est: Optional[np.ndarray] = None,
    S_est: Optional[np.ndarray] = None,
    A_true: Optional[np.ndarray] = None,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Aligns CP factor matrices (A_est, C_est, S_est) against ground-truth channel matrix A_true
    using channel matching, resolving column permutation and sign ambiguities.
    Supports passing a CP instance as the first argument.
    """
    if isinstance(A_est, CP):
        cp_obj = A_est
        A_val = cp_obj.A
        C_val = cp_obj.C
        S_val = cp_obj.S
        target_A_true = C_est if A_true is None else A_true
    else:
        A_val = A_est
        C_val = C_est
        S_val = S_est
        target_A_true = A_true

    A_aligned, C_aligned, S_aligned, perm, signs = align_factors_by_channel_matching(
        A_val, C_val, S_val, target_A_true
    )

    if isinstance(A_est, CP):
        A_est.factors = [A_aligned, C_aligned, S_aligned]

    return A_aligned, C_aligned, S_aligned, perm, signs


__all__ = [
    "solve_cp_als",
    "relative_error",
    "align_factors_by_channel_matching",
    "align_factors_by_code_matching",
    "align_factors",
]
