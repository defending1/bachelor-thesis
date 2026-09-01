"""
Spatial distance-based channel matrix generation module.

This module scatters receiver antennae and transmitting users on a 2D plane,
computes Euclidean distances between each antenna i and user r,
and constructs the real channel gain matrix A of shape (I, R) with:
    a_{ir} = Real_part(1 / dist(antenna_i, user_r))
"""

from typing import Tuple
import numpy as np


def generate_spatial_channel(
    num_antennas: int,
    num_sources: int,
    rng: np.random.Generator,
    area_side: float = 100.0,
    min_dist: float = 0.1,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Generates a real channel gain matrix A based on 2D Euclidean distances.

    1. Antenna positions p_i ~ Uniform([0, area_side]^2) for i = 1..I
    2. User positions p_r ~ Uniform([0, area_side]^2) for r = 1..R
    3. Distance matrix D where d_ir = max(||p_i - p_r||_2, min_dist)
    4. Channel matrix A where a_ir = Re(1 / d_ir) = 1 / d_ir

    Args:
        num_antennas (int): Number of receiver antennas (I).
        num_sources (int): Number of active sources/users (R).
        rng (np.random.Generator): NumPy random number generator instance.
        area_side (float): Bounding box side length for 2D plane. Default 100.0.
        min_dist (float): Minimum distance lower bound to avoid divide-by-zero. Default 0.1.

    Returns:
        Tuple[np.ndarray, np.ndarray, np.ndarray]:
            - A: Real channel matrix of shape (I, R) with a_ir = 1 / d_ir
            - antenna_pos: Antenna coordinates of shape (I, 2)
            - user_pos: User coordinates of shape (R, 2)
    """
    antenna_pos = rng.uniform(0.0, area_side, size=(num_antennas, 2))
    user_pos = rng.uniform(0.0, area_side, size=(num_sources, 2))

    # Compute Euclidean distance matrix D of shape (I, R)
    # diff: (I, 1, 2) - (1, R, 2) -> (I, R, 2)
    diff = antenna_pos[:, np.newaxis, :] - user_pos[np.newaxis, :, :]
    distances = np.linalg.norm(diff, axis=2)

    # Apply lower bound threshold to avoid division by zero
    distances = np.maximum(distances, min_dist)

    # Channel gain: Real part of 1 / distance (since distance is real scalar > 0, 1/d is real)
    A = 1.0 / distances
    return A, antenna_pos, user_pos
