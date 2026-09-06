"""
CP Tensor Decomposition utilities (CP class, metrics, ALS solvers, factor alignment).
"""

from .CP import CP
from .metrics import relative_error, tensor_norm
from .als import solve_cp_als, solve_nonnegative_cp_als
from .alignment import align_components

__all__ = [
    "CP",
    "relative_error",
    "tensor_norm",
    "solve_cp_als",
    "solve_nonnegative_cp_als",
    "align_components",
]
