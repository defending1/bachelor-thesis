"""
Core CP Decomposition and data loading logic for EEM Spectroscopy.
"""

from pathlib import Path
import numpy as np
import scipy.io as sio

from experiments.utils.cp import solve_nonnegative_cp_als, align_components


def load_eem_data(mat_path: Path):
    """Load preprocessed EEM tensor data and metadata from EEM18.mat."""
    if not mat_path.exists():
        raise FileNotFoundError(f"Dataset file not found at {mat_path}")

    mat = sio.loadmat(str(mat_path))

    x_obj = mat['X'][0, 0]
    x_tensor = np.asarray(x_obj['data'], dtype=np.float64)

    mixtures = mat.get('mixtures', None)
    compound_names = mat.get('compound_names', None)
    mode_ranges = mat.get('mode_ranges', None)
    mode_titles = mat.get('mode_titles', None)

    return {
        'X': x_tensor,
        'mixtures': mixtures,
        'compound_names': compound_names,
        'mode_ranges': mode_ranges,
        'mode_titles': mode_titles
    }


def fit_cp_with_restarts(X: np.ndarray, rank: int,
                         n_iter_max: int = 1000, n_restarts: int = 5, tol: float = 1e-7):
    """
    Fit non-negative CP decomposition of specified rank using central utils.cp solver.
    """
    return solve_nonnegative_cp_als(
        tensor=X,
        rank=rank,
        n_iter_max=n_iter_max,
        tol=tol,
        n_restarts=n_restarts,
        random_state=42,
    )


def run_experiment(mat_path: Path, target_error: float, max_rank: int,
                   n_restarts: int, n_iter_max: int):
    """
    Run experiment: test non-negative CP decomposition of increasing rank R = 1..max_rank
    until relative error <= target_error.
    """
    data = load_eem_data(mat_path)
    X = data['X']

    print("=" * 65)
    print(f"EEM Tensor Spectroscopy Experiment")
    print(f"Tensor Shape: {X.shape} (Samples x Emission x Excitation)")
    print(f"Target Error Epsilon: {target_error:.4f} ({target_error * 100:.2f}%)")
    print(f"Decomposition Type: Non-negative CP (NCP)")
    print(f"Max Rank: {max_rank}")
    print("=" * 65)

    rank_history = []
    final_rank = None
    final_error = None
    best_cp_models = {}

    for rank in range(1, max_rank + 1):
        cp_model, rel_error, elapsed = fit_cp_with_restarts(
            X, rank=rank,
            n_iter_max=n_iter_max, n_restarts=n_restarts
        )

        fit_percentage = (1.0 - rel_error) * 100.0
        best_cp_models[rank] = cp_model

        rank_history.append({
            'rank': rank,
            'relative_error': rel_error,
            'fit_percentage': fit_percentage,
            'fit_time_sec': elapsed
        })

        print(f"Rank {rank:2d}: Relative Error = {rel_error:.6f} | Fit = {fit_percentage:6.2f}% | Time = {elapsed:.3f}s")

        if rel_error <= target_error and final_rank is None:
            final_rank = rank
            final_error = rel_error
            print(f"\n>>> Target error threshold reached at Rank {final_rank}! Final Error = {final_error:.6f} <<<")

    if final_rank is None:
        final_rank = max_rank
        final_error = rank_history[-1]['relative_error']
        print(f"\n>>> Target error not reached within max_rank={max_rank}. Final Rank = {final_rank}, Error = {final_error:.6f} <<<")

    return {
        'final_rank': final_rank,
        'final_error': final_error,
        'target_error': target_error,
        'nonnegative': True,
        'rank_history': rank_history,
        'cp_models': best_cp_models,
        'data': data
    }
