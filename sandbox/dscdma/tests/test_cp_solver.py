"""
Unit tests for DS-CDMA TensorLy CP-ALS factor decomposition and reconstruction error.
"""

from dscdma.config import SimConfig
from dscdma.generator import DSCDMADatasetGenerator
from dscdma.cp_solver import solve_cp_als, relative_error


def test_solve_cp_als_reconstruction():
    """
    Tests relative reconstruction error of TensorLy CP-ALS on noiseless 3D real tensor.
    """
    config = SimConfig(num_sources=3, num_antennas=4, spreading_gain=16, num_symbols=100, seed=42)
    generator = DSCDMADatasetGenerator(config)
    data = generator.generate()

    T_true = data['tensor']

    (A_est, C_est, S_est), rec_err = solve_cp_als(
        T_true, rank=3, n_iter_max=2000, tol=1e-9, random_state=42
    )

    assert A_est.shape == (4, 3)
    assert C_est.shape == (16, 3)
    assert S_est.shape == (100, 3)
    assert rec_err < 1e-4


def test_solve_cp_als_multiple_dimensions():
    """
    Tests CP-ALS reconstruction across multiple tensor dimensions.
    """
    for R, I, J, K in [(2, 3, 8, 50), (3, 5, 16, 80)]:
        config = SimConfig(num_sources=R, num_antennas=I, spreading_gain=J, num_symbols=K, seed=100)
        generator = DSCDMADatasetGenerator(config)
        data = generator.generate()

        (A_est, C_est, S_est), rec_err = solve_cp_als(
            data['tensor'], rank=R, n_iter_max=2000, tol=1e-9, random_state=100
        )

        assert A_est.shape == (I, R)
        assert C_est.shape == (J, R)
        assert S_est.shape == (K, R)
        assert rec_err < 1e-3
