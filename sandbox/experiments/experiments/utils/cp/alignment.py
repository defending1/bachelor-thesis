"""
Factor matrix column alignment based on cosine similarity matching.
"""

import numpy as np


def align_components(norm_A: np.ndarray, norm_mixtures: np.ndarray) -> np.ndarray:
    """
    For each computed component column in norm_A, find the best matching reference column
    in norm_mixtures (maximizing absolute cosine similarity).

    Args:
        norm_A (np.ndarray): Computed factor matrix of shape (N, R).
        norm_mixtures (np.ndarray): Ground truth or reference matrix of shape (N, M).

    Returns:
        np.ndarray: Matched reference array of shape (N, R).
    """
    n_comp = norm_A.shape[1]
    n_mixtures = norm_mixtures.shape[1]
    matched_mixtures = np.zeros_like(norm_A)
    for j in range(n_comp):
        similarities = [
            np.abs(np.dot(norm_A[:, j], norm_mixtures[:, k]))
            for k in range(n_mixtures)
        ]
        best_k = int(np.argmax(similarities))
        matched_mixtures[:, j] = norm_mixtures[:, best_k]
    return matched_mixtures
