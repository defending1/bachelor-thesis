"""
Unit tests for DS-CDMA pure payload S matrix, antenna positions matrix P, user position extraction via trilateration, and visualization.
"""

from pathlib import Path
import numpy as np

from experiments.dscdma.config import SimConfig
from experiments.dscdma.utils.generator import DSCDMADatasetGenerator
from experiments.dscdma.solver.cp_solver import solve_cp_als
from experiments.dscdma.plot import extract_user_positions_from_A, plot_antenna_and_radii






def test_pure_payload_S_and_antenna_matrix_P():
    config = SimConfig(num_sources=3, num_antennas=4, spreading_gain=16, num_symbols=50, seed=42)
    generator = DSCDMADatasetGenerator(config)
    data = generator.generate()

    S_true = data["S_true"]
    antenna_pos = data["antenna_pos"]

    assert S_true.shape == (50, 3)
    for r in range(3):
        col_norm = float(np.linalg.norm(S_true[:, r]))
        np.testing.assert_allclose(col_norm, np.sqrt(50), rtol=1e-5)

    assert antenna_pos.shape == (4, 2)


def test_extract_user_positions_from_A_noiseless():
    config = SimConfig(num_sources=3, num_antennas=4, seed=42)
    generator = DSCDMADatasetGenerator(config)
    data = generator.generate()

    user_pos_true = data["user_pos"]
    antenna_pos = data["antenna_pos"]
    A_true = data["A_true"]

    user_pos_est, scale_factors = extract_user_positions_from_A(
        A_true, antenna_pos, area_side=config.area_side
    )

    np.testing.assert_allclose(user_pos_est, user_pos_true, atol=1e-4)
    np.testing.assert_allclose(scale_factors, np.ones(3), atol=1e-4)


def test_extract_user_positions_from_A_after_cp_als():
    config = SimConfig(num_sources=3, num_antennas=5, seed=123)
    generator = DSCDMADatasetGenerator(config)
    data = generator.generate()

    (A_est, _, _), rec_err = solve_cp_als(
        data["tensor"], rank=3, random_state=123, restore_physical_scale=True
    )
    assert rec_err < 1e-4

    user_pos_est, scale_factors = extract_user_positions_from_A(
        A_est, data["antenna_pos"], area_side=config.area_side
    )

    # Check that each extracted position corresponds to one of the true user positions (unpermuted or permuted)
    dists = np.linalg.norm(
        user_pos_est[:, np.newaxis, :] - data["user_pos"][np.newaxis, :, :], axis=2
    )
    min_dists = np.min(dists, axis=1)
    np.testing.assert_array_less(min_dists, 1.0)


def test_plot_antenna_and_radii(tmp_path: Path):
    config = SimConfig(num_sources=3, num_antennas=4, seed=123)
    generator = DSCDMADatasetGenerator(config)
    data = generator.generate()

    output_file = tmp_path / "test_plot.pdf"
    fig, ax = plot_antenna_and_radii(
        user_pos=data["user_pos"],
        antenna_pos_true=data["antenna_pos"],
        A_est=data["A_true"],
        S_est=data["S_true"],
        save_path=str(output_file),
        show=False,
    )

    assert output_file.exists()
    assert output_file.stat().st_size > 0





