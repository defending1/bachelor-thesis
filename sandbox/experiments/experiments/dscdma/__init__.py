"""
DS-CDMA 3D Tensor Synthesis and CP-ALS Factor Recovery.
"""

from experiments.dscdma.config import SimConfig
from experiments.dscdma.channel import generate_spatial_channel
from experiments.dscdma.codes import generate_spreading_codes
from experiments.dscdma.generator import DSCDMADatasetGenerator, tensor_reconstruct
from experiments.dscdma.cp_solver import solve_cp_als, relative_error
from experiments.dscdma.exporter import save_dataset, load_dataset

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
