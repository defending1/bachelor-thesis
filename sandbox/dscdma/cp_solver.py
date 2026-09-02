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
    restore_physical_scale: bool = True,
    n_restarts: int = 10,
) -> Tuple[Tuple[np.ndarray, np.ndarray, np.ndarray], float]:
    """
    Decomposes real 3D tensor T into factor matrices A, C, S using TensorLy CP-ALS.
    Performs multiple restarts to find the decomposition with minimum reconstruction error.

    Args:
        tensor (np.ndarray): Real tensor T of shape (I, J, K).
        rank (int): CP rank R (number of sources).
        n_iter_max (int): Maximum ALS iterations.
        tol (float): Convergence tolerance.
        random_state (Optional[int]): Base random seed for ALS initialization.
        restore_physical_scale (bool): If True, restores physical norm scaling to C (sqrt(J))
            and S (sqrt(K)), transferring the channel gain power back into A.
        n_restarts (int): Number of initialization restarts.

    Returns:
        Tuple[Tuple[np.ndarray, np.ndarray, np.ndarray], float]:
            - (A_est, C_est, S_est): Estimated factor matrices of shapes (I, R), (J, R), (K, R)
            - rec_error: Relative tensor reconstruction error ||T - T_rec||_F / ||T||_F
    """
    best_rec_err = float("inf")
    best_factors = None

    base_seed = random_state if random_state is not None else 42

    for run_idx in range(max(1, n_restarts)):
        init_mode = "svd" if run_idx == 0 else "random"
        seed = base_seed + run_idx if init_mode == "random" else base_seed

        try:
            cp_tensor = parafac(
                tensor,
                rank=rank,
                n_iter_max=n_iter_max,
                tol=tol,
                init=init_mode,
                random_state=seed,
            )
            weights, factors = cp_tensor
            T_rec = tl.cp_to_tensor((weights, factors))
            rec_err = relative_error(tensor, T_rec)

            if rec_err < best_rec_err:
                best_rec_err = rec_err
                best_factors = (weights, factors)
        except Exception:
            continue

    if best_factors is None:
        raise RuntimeError("CP-ALS factorization failed for all restarts.")

    weights, factors = best_factors
    A_est, C_est, S_est = factors[0].copy(), factors[1].copy(), factors[2].copy()

    if restore_physical_scale:
        J, K = tensor.shape[1], tensor.shape[2]
        if weights is not None:
            A_est = A_est * weights[np.newaxis, :]
        norm_C = np.linalg.norm(C_est, axis=0, keepdims=True)
        norm_S = np.linalg.norm(S_est, axis=0, keepdims=True)
        norm_C = np.maximum(norm_C, 1e-12)
        norm_S = np.maximum(norm_S, 1e-12)

        scale_factor = (norm_C * norm_S) / (np.sqrt(J) * np.sqrt(K))
        A_est = A_est * scale_factor
        C_est = (C_est / norm_C) * np.sqrt(J)
        S_est = (S_est / norm_S) * np.sqrt(K)

    return (A_est, C_est, S_est), best_rec_err
