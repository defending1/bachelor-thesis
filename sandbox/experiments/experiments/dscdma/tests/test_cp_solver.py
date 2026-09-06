"""
Unit tests for DS-CDMA TensorLy CP-ALS factor decomposition and reconstruction error.
"""

import numpy as np
from experiments.dscdma.config import SimConfig
from experiments.dscdma.utils.generator import DSCDMADatasetGenerator
from experiments.dscdma.solver.cp_solver import (
    solve_cp_als,
    relative_error,
    align_factors_by_channel_matching,
    align_factors_by_code_matching,
)


def test_solve_cp_als_reconstruction():
    config = SimConfig(num_sources=3, num_antennas=4, spreading_gain=16, num_symbols=100, seed=42)
    generator = DSCDMADatasetGenerator(config)
    data = generator.generate()

    T_true = data['tensor']

    (A_est, C_est, S_est), rec_err = solve_cp_als(
        T_true, rank=3, n_iter_max=2000, tol=1e-9, random_state=42, restore_physical_scale=True
    )

    assert A_est.shape == (4, 3)
    assert C_est.shape == (16, 3)
    assert S_est.shape == (100, 3)
    assert rec_err < 1e-4


def test_solve_cp_als_multiple_dimensions():
    for R, I, J, K in [(2, 3, 8, 50), (3, 5, 16, 80)]:
        config = SimConfig(num_sources=R, num_antennas=I, spreading_gain=J, num_symbols=K, seed=100)
        generator = DSCDMADatasetGenerator(config)
        data = generator.generate()

        (A_est, C_est, S_est), rec_err = solve_cp_als(
            data['tensor'], rank=R, n_iter_max=2000, tol=1e-9, random_state=100, restore_physical_scale=True
        )

        assert A_est.shape == (I, R)
        assert C_est.shape == (J, R)
        assert S_est.shape == (K, R)
        assert rec_err < 1e-3


def test_align_factors_by_channel_matching():
    config = SimConfig(num_sources=3, num_antennas=4, spreading_gain=16, num_symbols=100, seed=42)
    generator = DSCDMADatasetGenerator(config)
    data = generator.generate()

    A_true = data["A_true"]
    C_true = data["C_true"]
    S_true = data["S_true"]

    (A_est, C_est, S_est), rec_err = solve_cp_als(
        data["tensor"], rank=3, n_iter_max=2000, tol=1e-9, random_state=42, restore_physical_scale=True
    )
    assert rec_err < 1e-4

    A_aligned, C_aligned, S_aligned, perm, signs = align_factors_by_channel_matching(
        A_est, C_est, S_est, A_true
    )


    assert A_aligned.shape == A_true.shape
    assert C_aligned.shape == C_true.shape
    assert S_aligned.shape == S_true.shape
    assert len(perm) == 3
    assert set(perm) == {0, 1, 2}

    for r in range(3):
        corr_A = float(np.dot(A_aligned[:, r], A_true[:, r])) / (
            np.linalg.norm(A_aligned[:, r]) * np.linalg.norm(A_true[:, r])
        )
        assert corr_A > 0.98, f"Column {r} channel correlation is {corr_A}, expected > 0.98"


def test_align_factors_by_code_matching():
    config = SimConfig(num_sources=3, num_antennas=4, spreading_gain=16, num_symbols=100, seed=42)
    generator = DSCDMADatasetGenerator(config)
    data = generator.generate()

    C_true = data["C_true"]
    (A_est, C_est, S_est), rec_err = solve_cp_als(
        data["tensor"], rank=3, n_iter_max=2000, tol=1e-9, random_state=42, restore_physical_scale=True
    )
    assert rec_err < 1e-4

    A_aligned, C_aligned, S_aligned, perm, signs = align_factors_by_code_matching(
        A_est, C_est, S_est, C_true
    )

    assert len(perm) == 3
    assert set(perm) == {0, 1, 2}


def test_cp_class_compute():
    from experiments.utils.cp import CP
    config = SimConfig(num_sources=3, num_antennas=4, spreading_gain=16, num_symbols=100, seed=42)
    generator = DSCDMADatasetGenerator(config)
    data = generator.generate()

    cp = CP(data["tensor"], rank=3).compute(n_iter_max=2000, tol=1e-9, random_state=42)
    assert cp.A is not None
    assert cp.B is not None
    assert cp.C is not None
    assert cp.rec_error < 1e-4
    assert len(cp.factors) == 3

    reconstructed_tensor = cp.reconstruct()
    assert reconstructed_tensor.shape == data["tensor"].shape

