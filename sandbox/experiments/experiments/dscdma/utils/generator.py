"""
Main dataset generator module for DS-CDMA noiseless real tensor synthesis.

Synthesizes exact rank-R 3-way real tensor T_ijk = sum_{r=1}^R a_ir * c_jr * s_kr
using spatial 2D channel matrix A, random binary codes C, and generic real signals S.
"""

from typing import Dict, Any, Optional
import numpy as np

from experiments.dscdma.config import SimConfig
from experiments.dscdma.solver.codes import generate_spreading_codes
from experiments.dscdma.solver.channel import generate_spatial_channel
from experiments.utils.cp import CP


def tensor_reconstruct(A: np.ndarray, C: np.ndarray, S: np.ndarray) -> np.ndarray:
    """
    Constructs dense 3D tensor T from factor matrices A, C, S using CP.reconstruct().
    """
    return CP(factors=[A, C, S]).reconstruct()


def add_gaussian_noise(
    tensor: np.ndarray,
    noise_std: float,
    rng: Optional[np.random.Generator] = None,
) -> np.ndarray:
    """
    Adds zero-mean additive Gaussian noise with standard deviation noise_std to the 3D tensor.
    T_noisy = T + W, where W_ijk ~ N(0, noise_std^2).
    """
    if noise_std <= 0.0:
        return tensor.copy()
    if rng is None:
        rng = np.random.default_rng()
    noise = rng.normal(loc=0.0, scale=noise_std, size=tensor.shape)
    return tensor + noise



class DSCDMADatasetGenerator:
    """
    DS-CDMA exact rank-R real tensor generator for blind deconvolution experiments.

    Generates the noiseless, memoryless 3D real tensor T of shape (I, J, K) alongside
    ground truth factor matrices A, C, and S.
    """

    def __init__(self, config: SimConfig):
        config.validate()
        self.config = config
        self.rng = np.random.default_rng(config.seed)

    def generate_signals(self) -> np.ndarray:
        """
        Generates real signals S of shape (K, R) with pure symbol payload data across all K rows.
        """
        K = self.config.num_symbols
        R = self.config.num_sources

        return self.rng.normal(0.0, 1.0, size=(K, R))

    def generate(self) -> Dict[str, Any]:
        A_true, antenna_pos, user_pos = generate_spatial_channel(
            self.config.num_antennas,
            self.config.num_sources,
            self.rng,
            self.config.area_side,
            self.config.min_dist,
        )

        C_true = generate_spreading_codes(
            self.config.spreading_gain,
            self.config.num_sources,
            self.rng,
        )

        S_true = self.generate_signals()
        cp = CP(rank=self.config.num_sources, factors=[A_true, C_true, S_true])
        tensor = cp.reconstruct()

        return {
            'tensor': tensor,
            'A_true': A_true,
            'C_true': C_true,
            'S_true': S_true,
            'antenna_pos': antenna_pos,
            'user_pos': user_pos,
            'rank_R': self.config.num_sources,
        }
