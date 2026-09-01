"""
Unit test suite for exact rank-R real DS-CDMA spatial tensor generation.
"""

import sys
from pathlib import Path
import numpy as np
import pytest

# Ensure parent directory is in python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import SimConfig
from generator import DSCDMADatasetGenerator
from exporter import save_dataset, load_dataset


def test_tensor_shape_and_dtypes():
    config = SimConfig(num_sources=3, num_antennas=4, spreading_gain=15, num_symbols=50, seed=123)
    generator = DSCDMADatasetGenerator(config)
    data = generator.generate()

    assert data['tensor'].shape == (4, 15, 50)
    assert data['A_true'].shape == (4, 3)
    assert data['C_true'].shape == (15, 3)
    assert data['S_true'].shape == (50, 3)
    assert data['antenna_pos'].shape == (4, 2)
    assert data['user_pos'].shape == (3, 2)

    # Real matrices & real tensor
    assert np.issubdtype(data['tensor'].dtype, np.floating)
    assert np.issubdtype(data['A_true'].dtype, np.floating)
    assert np.issubdtype(data['C_true'].dtype, np.floating)
    assert np.issubdtype(data['S_true'].dtype, np.floating)


def test_spatial_channel_matrix():
    config = SimConfig(num_sources=3, num_antennas=4, area_side=100.0, seed=42)
    generator = DSCDMADatasetGenerator(config)
    data = generator.generate()

    A = data['A_true']
    antenna_pos = data['antenna_pos']
    user_pos = data['user_pos']

    # Check a_ir = 1 / dist(antenna_i, user_r)
    for i in range(4):
        for r in range(3):
            dist = np.linalg.norm(antenna_pos[i] - user_pos[r])
            expected_a = 1.0 / max(dist, config.min_dist)
            np.testing.assert_allclose(A[i, r], expected_a, rtol=1e-10)


def test_binary_spreading_codes():
    config = SimConfig(num_sources=4, num_antennas=2, spreading_gain=10, num_symbols=10, seed=42)
    generator = DSCDMADatasetGenerator(config)
    data = generator.generate()

    C = data['C_true']
    unique_vals = set(np.unique(C))
    assert unique_vals.issubset({-1.0, 1.0})


def test_exact_reconstruction():
    config = SimConfig(num_sources=3, num_antennas=4, spreading_gain=12, num_symbols=20, seed=42)
    generator = DSCDMADatasetGenerator(config)
    data = generator.generate()

    T = data['tensor']
    A = data['A_true']
    C = data['C_true']
    S = data['S_true']

    # Manually compute T_{ijk}
    I, J, K = T.shape
    R = data['rank_R']
    T_manual = np.zeros((I, J, K), dtype=float)
    for r in range(R):
        for i in range(I):
            for j in range(J):
                for k in range(K):
                    T_manual[i, j, k] += A[i, r] * C[j, r] * S[k, r]

    np.testing.assert_allclose(T, T_manual, rtol=1e-12, atol=1e-12)


def test_exporter_roundtrip(tmp_path):
    config = SimConfig(num_sources=3, num_antennas=4, spreading_gain=16, num_symbols=30, seed=99)
    generator = DSCDMADatasetGenerator(config)
    data = generator.generate()

    file_path = tmp_path / "test_spatial_data.npz"
    save_dataset(data, file_path)
    loaded = load_dataset(file_path)

    np.testing.assert_allclose(data['tensor'], loaded['tensor'])
    np.testing.assert_allclose(data['A_true'], loaded['A_true'])
    np.testing.assert_allclose(data['C_true'], loaded['C_true'])
    np.testing.assert_allclose(data['S_true'], loaded['S_true'])
    np.testing.assert_allclose(data['antenna_pos'], loaded['antenna_pos'])
    np.testing.assert_allclose(data['user_pos'], loaded['user_pos'])
    assert loaded['rank_R'] == data['rank_R']
