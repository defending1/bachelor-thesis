"""
Main dataset generator module for DS-CDMA noiseless tensor synthesis.

Synthesizes the exact rank-R 3-way tensor T_ijk = sum_{r=1}^R a_ir * c_jr * s_kr
matching Chapter 4 (Section 4.3) of the thesis.
"""

from typing import Dict, Any
import numpy as np

from config import SimConfig
from codes import generate_walsh_codes
from channel import generate_channel_matrix


class DSCDMADatasetGenerator:
    """
    DS-CDMA exact rank-R tensor generator for blind deconvolution experiments.

    Generates the noiseless, memoryless 3D tensor T of shape (I, J, K) alongside
    the ground truth factor matrices A, C, and S.
    """

    def __init__(self, config: SimConfig):
        """
        Initializes the generator with a given SimConfig configuration.

        Args:
            config (SimConfig): Simulation parameters object.
        """
        config.validate()
        self.config = config
        self.rng = np.random.default_rng(config.seed)

    def generate_symbols(self) -> np.ndarray:
        """
        Generates BPSK symbols S in {-1, +1} of shape (K, R).

        Returns:
            np.ndarray: Integer matrix S of shape (K, R) with entries in {-1, +1}.
        """
        K = self.config.num_symbols
        R = self.config.num_sources
        symbols = self.rng.choice([-1.0, 1.0], size=(K, R))
        return symbols

    def generate(self) -> Dict[str, Any]:
        """
        Synthesizes the exact rank-R tensor T and ground truth factor matrices.

        Computes:
            T_{ijk} = sum_{r=1}^R a_{ir} * c_{jr} * s_{kr}
        using numpy.einsum.

        Returns:
            Dict[str, Any]: Dictionary containing:
                - 'tensor': 3D complex array of shape (I, J, K)
                - 'A_true': Factor matrix A of shape (I, R), dtype complex128
                - 'C_true': Factor matrix C of shape (J, R), dtype float64
                - 'S_true': Factor matrix S of shape (K, R), dtype float64
                - 'rank_R': Integer R
        """
        # 1. Generate Ground Truth factor matrices
        A_true = generate_channel_matrix(
            self.config.num_antennas, 
            self.config.num_sources, 
            self.rng
        )  # (I, R)

        C_true = generate_walsh_codes(
            self.config.spreading_gain, 
            self.config.num_sources
        )  # (J, R)

        S_true = self.generate_symbols()  # (K, R)

        # 2. Synthesize noiseless tensor T of shape (I, J, K)
        # T_{ijk} = sum_r A_{ir} * C_{jr} * S_{kr}
        tensor = np.einsum('ir,jr,kr->ijk', A_true, C_true, S_true, optimize=True)

        return {
            'tensor': tensor,
            'A_true': A_true,
            'C_true': C_true,
            'S_true': S_true,
            'rank_R': self.config.num_sources
        }
