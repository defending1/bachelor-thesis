"""
Unit tests for DS-CDMA visualizer, user position extraction from S, and antenna position estimation.
"""

from pathlib import Path
import numpy as np

from dscdma.config import SimConfig
from dscdma.generator import DSCDMADatasetGenerator
from dscdma.cp_solver import solve_cp_als
from dscdma.plot import extract_user_positions, estimate_antenna_positions, plot_antenna_and_radii


def test_extract_user_positions_from_S():
    """
    Tests extraction of user 2D positions from signal matrix S_true.
    """
    config = SimConfig(num_sources=3, num_antennas=4, seed=42)
    generator = DSCDMADatasetGenerator(config)
    data = generator.generate()

    user_pos_true = data["user_pos"]
    S_true = data["S_true"]
    A_true = data["A_true"]

    user_pos_est, _, _ = extract_user_positions(S_true, A_true, area_side=config.area_side)

    np.testing.assert_allclose(user_pos_est, user_pos_true, atol=1e-5)


def test_estimate_antenna_positions_from_S_and_A():
    """
    Tests antenna position estimation using factors S_true and A_true without ground-truth user_pos.
    """
    config = SimConfig(num_sources=3, num_antennas=4, seed=42)
    generator = DSCDMADatasetGenerator(config)
    data = generator.generate()

    antenna_pos_true = data["antenna_pos"]
    S_true = data["S_true"]
    A_true = data["A_true"]

    antenna_pos_est, user_pos_est = estimate_antenna_positions(S_true, A_true, area_side=config.area_side)

    np.testing.assert_allclose(user_pos_est, data["user_pos"], atol=1e-4)
    np.testing.assert_allclose(antenna_pos_est, antenna_pos_true, atol=1e-4)


def test_estimate_antenna_positions_after_cp_als():
    """
    Tests full pipeline: CP-ALS decomposition -> user extraction from S_est -> antenna trilateration.
    """
    config = SimConfig(num_sources=3, num_antennas=4, seed=42)
    generator = DSCDMADatasetGenerator(config)
    data = generator.generate()

    (A_est, _, S_est), rec_err = solve_cp_als(data["tensor"], rank=3, random_state=42)
    assert rec_err < 1e-4

    antenna_pos_est, user_pos_est = estimate_antenna_positions(S_est, A_est, area_side=config.area_side)

    # Verify extracted user positions and antenna positions match true positions closely
    np.testing.assert_allclose(user_pos_est, data["user_pos"], atol=1e-2)
    np.testing.assert_allclose(antenna_pos_est, data["antenna_pos"], atol=1e-1)


def test_plot_antenna_and_radii(tmp_path: Path):
    """
    Tests figure generation and saving to disk with embedded S_est.
    """
    config = SimConfig(num_sources=3, num_antennas=2, seed=123)
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
