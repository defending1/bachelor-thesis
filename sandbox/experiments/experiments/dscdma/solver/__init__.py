"""
DS-CDMA Solvers package containing channel synthesis, code generation, CP-ALS factorization, and user position extraction via trilateration.
"""

from experiments.dscdma.solver.channel import generate_spatial_channel
from experiments.dscdma.solver.codes import generate_spreading_codes
from experiments.dscdma.solver.cp_solver import (
    solve_cp_als,
    relative_error,
    align_factors_by_channel_matching,
    align_factors_by_code_matching,
    align_factors,
)
from experiments.dscdma.solver.localization import extract_user_positions_from_A

__all__ = [
    "generate_spatial_channel",
    "generate_spreading_codes",
    "solve_cp_als",
    "relative_error",
    "align_factors_by_channel_matching",
    "align_factors_by_code_matching",
    "align_factors",
    "extract_user_positions_from_A",
]
