"""
Unit test suite for exact rank-R DS-CDMA tensor generation.
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
    config = SimConfig(num_sources=3, num_antennas=2, spreading_gain=16, num_symbols=50, seed=123)
    generator = DSCDMADatasetGenerator(config)
    data = generator.generate()

    assert data['tensor'].shape == (2, 16, 50)
    assert data['A_true'].shape == (2, 3)
    assert data['C_true'].shape == (16, 3)
    assert data['S_true'].shape == (50, 3)

    assert np.issubdtype(data['tensor'].dtype, np.complexfloating)
    assert np.issubdtype(data['A_true'].dtype, np.complexfloating)


def test_walsh_orthogonality():
    config = SimConfig(num_sources=4, num_antennas=2, spreading_gain=16, num_symbols=10, seed=42)
    generator = DSCDMADatasetGenerator(config)
    data = generator.generate()

    C = data['C_true']
    gram = C.T @ C  # R x R
    # Off-diagonal elements should be exactly 0
    off_diag = gram - np.diag(np.diag(gram))
    np.testing.assert_allclose(off_diag, 0.0, atol=1e-12)


def test_bpsk_symbols():
    config = SimConfig(num_sources=3, num_antennas=2, spreading_gain=16, num_symbols=100, seed=42)
    generator = DSCDMADatasetGenerator(config)
    data = generator.generate()

    S = data['S_true']
    # All entries must be in {-1.0, 1.0}
    unique_vals = set(np.unique(S))
    assert unique_vals.issubset({-1.0, 1.0})


def test_exact_reconstruction():
    config = SimConfig(num_sources=3, num_antennas=4, spreading_gain=16, num_symbols=20, seed=42)
    generator = DSCDMADatasetGenerator(config)
    data = generator.generate()

    T = data['tensor']
    A = data['A_true']
    C = data['C_true']
    S = data['S_true']

    # Manually compute T_{ijk}
    I, J, K = T.shape
    R = data['rank_R']
    T_manual = np.zeros((I, J, K), dtype=complex)
    for r in range(R):
        for i in range(I):
            for j in range(J):
                for k in range(K):
                    T_manual[i, j, k] += A[i, r] * C[j, r] * S[k, r]

    np.testing.assert_allclose(T, T_manual, rtol=1e-12, atol=1e-12)


def test_exporter_roundtrip(tmp_path):
    config = SimConfig(num_sources=3, num_antennas=2, spreading_gain=16, num_symbols=30, seed=99)
    generator = DSCDMADatasetGenerator(config)
    data = generator.generate()

    file_path = tmp_path / "test_data.npz"
    save_dataset(data, file_path)
    loaded = load_dataset(file_path)

    np.testing.assert_allclose(data['tensor'], loaded['tensor'])
    np.testing.assert_allclose(data['A_true'], loaded['A_true'])
    np.testing.assert_allclose(data['C_true'], loaded['C_true'])
    np.testing.assert_allclose(data['S_true'], loaded['S_true'])
    assert loaded['rank_R'] == data['rank_R']
