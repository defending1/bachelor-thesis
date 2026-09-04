"""
CP Tensor Decomposition utilities (metrics, ALS solvers, factor alignment).
"""

from .metrics import relative_error, tensor_norm
from .als import solve_cp_als, solve_nonnegative_cp_als
from .alignment import align_components

__all__ = [
    "relative_error",
    "tensor_norm",
    "solve_cp_als",
    "solve_nonnegative_cp_als",
    "align_components",
]
