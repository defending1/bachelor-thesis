"""
DS-CDMA 3D Tensor Synthesis and CP-ALS Factor Recovery.
"""

from experiments.dscdma.config import SimConfig
from experiments.dscdma.solver import (
    generate_spatial_channel,
    generate_spreading_codes,
    solve_cp_als,
    relative_error,
    align_factors_by_channel_matching,
    align_factors_by_code_matching,
    align_factors,
    extract_user_positions_from_A,
)
from experiments.dscdma.utils.generator import DSCDMADatasetGenerator, tensor_reconstruct
from experiments.dscdma.utils.exporter import save_dataset, load_dataset

__all__ = [
    "SimConfig",
    "generate_spatial_channel",
    "generate_spreading_codes",
    "DSCDMADatasetGenerator",
    "tensor_reconstruct",
    "solve_cp_als",
    "relative_error",
    "align_factors_by_channel_matching",
    "align_factors_by_code_matching",
    "align_factors",
    "extract_user_positions_from_A",
    "save_dataset",
    "load_dataset",
]

