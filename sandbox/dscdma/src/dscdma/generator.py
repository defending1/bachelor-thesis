"""
Main dataset generator module for DS-CDMA noiseless real tensor synthesis.

Synthesizes exact rank-R 3-way real tensor T_ijk = sum_{r=1}^R a_ir * c_jr * s_kr
using spatial 2D channel matrix A, random binary codes C, and generic real signals S.
"""

from typing import Dict, Any
import numpy as np

from dscdma.config import SimConfig
from dscdma.codes import generate_spreading_codes
from dscdma.channel import generate_spatial_channel


def tensor_reconstruct(A: np.ndarray, C: np.ndarray, S: np.ndarray) -> np.ndarray:
    """
    Constructs dense 3D tensor T from factor matrices A, C, S.

    Formulation:
        R_mat = Khatri-Rao(S, C) of shape (K * J, R)
        Y = A @ R_mat.T          of shape (I, K * J) -> Unfolding T_{(1)}
        T = reshape(Y)           of shape (I, J, K)

    Args:
        A: Channel gain matrix of shape (I, R)
        C: Spreading code matrix of shape (J, R)
        S: Transmitted signal matrix of shape (K, R)

    Returns:
        np.ndarray: Real 3D tensor of shape (I, J, K)
    """
    I, R = A.shape
    J = C.shape[0]
    K = S.shape[0]

    # 1. R_mat = Khatri-Rao(S, C) of shape (K * J, R)
    R_mat = np.einsum('kr,jr->kjr', S, C).reshape(K * J, R)

    # 2. Y = A @ R_mat.T of shape (I, K * J)
    Y = A @ R_mat.T

    # 3. Reshape into 3D tensor (I, J, K)
    tensor = Y.reshape(I, K, J).transpose(0, 2, 1)
    return tensor


class DSCDMADatasetGenerator:
    """
    DS-CDMA exact rank-R real tensor generator for blind deconvolution experiments.

    Generates the noiseless, memoryless 3D real tensor T of shape (I, J, K) alongside
    ground truth factor matrices A, C, and S.
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

    def generate_signals(self, user_pos: np.ndarray) -> np.ndarray:
        """
        Generates real signals S of shape (K, R) with embedded 2D user coordinates in rows 0 and 1.

        Args:
            user_pos (np.ndarray): User 2D coordinates of shape (R, 2).

        Returns:
            np.ndarray: Real matrix S of shape (K, R).
        """
        K = self.config.num_symbols
        R = self.config.num_sources
        area = self.config.area_side

        signals = np.zeros((K, R), dtype=np.float64)

        for r in range(R):
            # Embed normalized user coordinates in rows 0 and 1
            x_norm = user_pos[r, 0] / area
            y_norm = user_pos[r, 1] / area
            signals[0, r] = x_norm
            signals[1, r] = y_norm

            # Generate random payload symbols for remaining rows
            if K > 2:
                payload = self.rng.normal(0.0, 1.0, size=(K - 2,))
                # Scale payload energy so total column norm equals sqrt(K)
                pos_energy = x_norm**2 + y_norm**2
                target_payload_energy = max(float(K) - pos_energy, 1e-6)
                current_payload_norm = float(np.linalg.norm(payload))
                if current_payload_norm > 1e-12:
                    payload = payload * (np.sqrt(target_payload_energy) / current_payload_norm)
                signals[2:, r] = payload
            else:
                col_norm = float(np.linalg.norm(signals[:, r]))
                if col_norm > 1e-12:
                    signals[:, r] = signals[:, r] * (np.sqrt(K) / col_norm)

        return signals

    def generate(self) -> Dict[str, Any]:
        """
        Synthesizes exact rank-R tensor T and returns factor matrices and spatial coordinates.

        Returns:
            Dict[str, Any]: Dictionary containing:
                - 'tensor': 3D real array of shape (I, J, K)
                - 'A_true': Factor matrix A of shape (I, R), dtype float64
                - 'C_true': Factor matrix C of shape (J, R), dtype float64
                - 'S_true': Factor matrix S of shape (K, R), dtype float64
                - 'antenna_pos': Antenna 2D positions of shape (I, 2)
                - 'user_pos': User 2D positions of shape (R, 2)
                - 'rank_R': Integer R
        """
        A_true, antenna_pos, user_pos = generate_spatial_channel(
            self.config.num_antennas,
            self.config.num_sources,
            self.rng,
            self.config.area_side,
            self.config.min_dist,
        )  # (I, R)

        C_true = generate_spreading_codes(
            self.config.spreading_gain,
            self.config.num_sources,
            self.rng,
        )  # (J, R)

        S_true = self.generate_signals(user_pos)  # (K, R)

        # Synthesize tensor T using tensor_reconstruct
        tensor = tensor_reconstruct(A_true, C_true, S_true)

        return {
            'tensor': tensor,
            'A_true': A_true,
            'C_true': C_true,
            'S_true': S_true,
            'antenna_pos': antenna_pos,
            'user_pos': user_pos,
            'rank_R': self.config.num_sources,
        }
