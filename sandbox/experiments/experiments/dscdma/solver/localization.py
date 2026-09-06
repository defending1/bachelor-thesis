"""
Localization module for extracting 2D user positions from recovered channel factor matrix A.
"""

from typing import Tuple
import numpy as np
from scipy.optimize import least_squares


def extract_user_positions_from_A(
    A_est: np.ndarray,
    antenna_pos: np.ndarray,
    area_side: float = 100.0,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Extracts 2D user positions by solving non-linear least squares trilateration
    for each column of channel factor A_est against known fixed antenna positions matrix P (antenna_pos).

    Formulation:
        For column r of A_est (shape I, R):
            |a_{i, r}| ~ c_r / ||antenna_pos[i] - u_r||_2

        We solve for u_r = (x_r, y_r) in R^2 and scalar gain c_r > 0:
            min_{u_r, c_r} sum_{i=1}^I (|a_{i, r}| - c_r / ||p_i - u_r||_2)^2

    Args:
        A_est (np.ndarray): Channel gain factor matrix of shape (I, R).
        antenna_pos (np.ndarray): Fixed antenna coordinates matrix P of shape (I, 2).
        area_side (float): Bounding side length of 2D region. Default 100.0.

    Returns:
        Tuple[np.ndarray, np.ndarray]:
            - user_pos_est: Estimated user positions matrix of shape (R, 2).
            - scale_factors: Estimated scalar gain factors c of shape (R,).
    """
    I, R = A_est.shape
    user_pos_est = np.zeros((R, 2), dtype=np.float64)
    scale_factors = np.zeros(R, dtype=np.float64)

    # Multi-start initial candidates to avoid local minima in non-linear least squares
    grid = np.linspace(0.2 * area_side, 0.8 * area_side, 3)
    grid_pts = np.array(np.meshgrid(grid, grid)).T.reshape(-1, 2)
    candidate_inits = np.vstack([np.mean(antenna_pos, axis=0)[np.newaxis, :], antenna_pos, grid_pts])

    for r in range(R):
        a_col = np.abs(A_est[:, r])

        best_cost = float("inf")
        best_pos = np.mean(antenna_pos, axis=0)
        best_c = 1.0

        for init_pos in candidate_inits:
            init_dists = np.linalg.norm(antenna_pos - init_pos, axis=1)
            init_c = float(np.median(a_col * np.maximum(init_dists, 0.1)))
            theta_0 = np.array([init_pos[0], init_pos[1], max(init_c, 1e-3)], dtype=np.float64)

            def residuals(theta: np.ndarray) -> np.ndarray:
                pos = theta[:2]
                c = max(theta[2], 1e-6)
                dists = np.linalg.norm(antenna_pos - pos, axis=1)
                dists = np.maximum(dists, 1e-4)
                expected_a = c / dists
                return a_col - expected_a

            res = least_squares(
                residuals,
                theta_0,
                bounds=([0.0, 0.0, 1e-6], [area_side * 2.0, area_side * 2.0, np.inf]),
            )

            if res.cost < best_cost:
                best_cost = float(res.cost)
                best_pos = res.x[:2]
                best_c = float(res.x[2])

        user_pos_est[r] = best_pos
        scale_factors[r] = best_c

    return user_pos_est, scale_factors
