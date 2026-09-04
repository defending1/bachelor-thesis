"""
DS-CDMA Tensor Factorization using CP-ALS (TensorLy).

Re-exports unified CP-ALS solver and relative reconstruction error from experiments.utils.cp.
"""

from experiments.utils.cp import solve_cp_als, relative_error

__all__ = ["solve_cp_als", "relative_error"]
