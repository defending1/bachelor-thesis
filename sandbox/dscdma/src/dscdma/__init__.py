"""
DS-CDMA 3D Tensor Synthesis and CP-ALS Factor Recovery.
"""

from dscdma.config import SimConfig
from dscdma.channel import generate_spatial_channel
from dscdma.codes import generate_spreading_codes
from dscdma.generator import DSCDMADatasetGenerator, tensor_reconstruct
from dscdma.cp_solver import solve_cp_als, relative_error
from dscdma.exporter import save_dataset, load_dataset

__all__ = [
    "SimConfig",
    "generate_spatial_channel",
    "generate_spreading_codes",
    "DSCDMADatasetGenerator",
    "tensor_reconstruct",
    "solve_cp_als",
    "relative_error",
    "save_dataset",
    "load_dataset",
]
