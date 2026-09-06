"""
TensorLy-powered CP-ALS solvers (Standard and Non-Negative CP) returning CP container instances.
"""

import time
from typing import Tuple, Optional, Any
import numpy as np
import tensorly as tl
from tensorly.decomposition import parafac, non_negative_parafac

from .metrics import relative_error
from .CP import CP


def solve_cp_als(
    tensor: np.ndarray,
    rank: int,
    n_iter_max: int = 2000,
    tol: float = 1e-9,
    random_state: Optional[int] = 42,
    restore_physical_scale: bool = False,
    n_restarts: int = 10,
) -> CP:
    """
    Decomposes a tensor into CP factor matrices using TensorLy CP-ALS with restarts,
    returning a CP object encapsulating factors and reconstruction error.

    Args:
        tensor (np.ndarray): Target tensor of shape (I, J, K, ...).
        rank (int): CP decomposition rank R.
        n_iter_max (int): Maximum ALS iterations per restart run.
        tol (float): Convergence tolerance.
        random_state (Optional[int]): Base random seed.
        restore_physical_scale (bool): If True for 3D tensors, transfers norm power from
            modes 1 & 2 (C and S) into mode 0 (A).
        n_restarts (int): Number of initialization restarts.

    Returns:
        CP: Encapsulated CP factorization result.
    """
    start_t = time.time()
    best_rec_err = float("inf")
    best_factors = None
    best_weights = None

    base_seed = random_state

    for run_idx in range(max(1, n_restarts)):
        init_mode = "svd" if run_idx == 0 else "random"
        seed = (base_seed + run_idx) if (base_seed is not None and init_mode == "random") else base_seed

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
                best_factors = [f.copy() for f in factors]
                best_weights = weights.copy() if weights is not None else None
        except Exception:
            continue

    if best_factors is None:
        raise RuntimeError("CP-ALS factorization failed for all restarts.")

    elapsed = time.time() - start_t
    factors = list(best_factors)

    if restore_physical_scale and len(factors) == 3:
        A_est, C_est, S_est = factors[0], factors[1], factors[2]
        J, K = tensor.shape[1], tensor.shape[2]
        norm_C = np.linalg.norm(C_est, axis=0, keepdims=True)
        norm_S = np.linalg.norm(S_est, axis=0, keepdims=True)
        norm_C = np.maximum(norm_C, 1e-12)
        norm_S = np.maximum(norm_S, 1e-12)

        scale_factor = (norm_C * norm_S) / (np.sqrt(J) * np.sqrt(K))
        A_est = A_est * scale_factor
        C_est = (C_est / norm_C) * np.sqrt(J)
        S_est = (S_est / norm_S) * np.sqrt(K)
        factors = [A_est, C_est, S_est]

    return CP(
        tensor=tensor,
        rank=rank,
        factors=factors,
        weights=best_weights,
        rec_error=best_rec_err,
        runtime=elapsed,
    )


def solve_nonnegative_cp_als(
    tensor: np.ndarray,
    rank: int,
    n_iter_max: int = 1000,
    tol: float = 1e-7,
    n_restarts: int = 5,
    random_state: Optional[int] = 42,
) -> CP:
    """
    Fits non-negative CP decomposition of specified rank with multiple random restarts
    using TensorLy's non_negative_parafac, returning a CP object.

    Args:
        tensor (np.ndarray): Non-negative tensor X.
        rank (int): Target CP rank.
        n_iter_max (int): Max iterations.
        tol (float): Convergence tolerance.
        n_restarts (int): Number of restarts.
        random_state (Optional[int]): Base random seed.

    Returns:
        CP: Encapsulated non-negative CP factorization result.
    """
    best_error = float("inf")
    best_factors = None
    best_weights = None
    best_time = 0.0

    base_seed = random_state

    for trial in range(max(1, n_restarts)):
        start_t = time.time()
        seed = (base_seed + trial * 100) if base_seed is not None else None

        cp_tensor = non_negative_parafac(
            tensor,
            rank=rank,
            n_iter_max=n_iter_max,
            tol=tol,
            init="random",
            random_state=seed,
        )

        elapsed = time.time() - start_t
        weights, factors = cp_tensor
        reconstruction = tl.cp_to_tensor(cp_tensor)
        rel_err = relative_error(tensor, reconstruction)

        if rel_err < best_error:
            best_error = rel_err
            best_factors = [f.copy() for f in factors]
            best_weights = weights.copy() if weights is not None else None
            best_time = elapsed

    return CP(
        tensor=tensor,
        rank=rank,
        factors=best_factors,
        weights=best_weights,
        rec_error=best_error,
        runtime=best_time,
    )
