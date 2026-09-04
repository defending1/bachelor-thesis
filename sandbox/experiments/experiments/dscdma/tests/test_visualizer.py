"""
Unit tests for DS-CDMA pure payload S matrix, antenna positions matrix P, and visualization.
"""

from pathlib import Path
import numpy as np

from experiments.dscdma.config import SimConfig
from experiments.dscdma.generator import DSCDMADatasetGenerator
from experiments.dscdma.cp_solver import solve_cp_als
from experiments.dscdma.plot import plot_antenna_and_radii


def test_pure_payload_S_and_antenna_matrix_P():
    config = SimConfig(num_sources=3, num_antennas=4, spreading_gain=16, num_symbols=50, seed=42)
    generator = DSCDMADatasetGenerator(config)
    data = generator.generate()

    S_true = data["S_true"]
    antenna_pos = data["antenna_pos"]

    # Verify S_true shape and that columns are pure symbols (norm ~ sqrt(K))
    assert S_true.shape == (50, 3)
    for r in range(3):
        col_norm = float(np.linalg.norm(S_true[:, r]))
        np.testing.assert_allclose(col_norm, np.sqrt(50), rtol=1e-5)

    # Verify antenna_pos matrix P shape (I, 2)
    assert antenna_pos.shape == (4, 2)


def test_plot_antenna_and_radii(tmp_path: Path):
    config = SimConfig(num_sources=3, num_antennas=2, seed=123)
    generator = DSCDMADatasetGenerator(config)
    data = generator.generate()

    output_file = tmp_path / "test_plot.pdf"
    fig, ax = plot_antenna_and_radii(
        user_pos=data["user_pos"],
        antenna_pos_true=data["antenna_pos"],
        A_est=data["A_true"],
        S_est=data["S_true"],
        antenna_pos_est=data["antenna_pos"],
        save_path=str(output_file),
        show=False,
    )

    assert output_file.exists()
    assert output_file.stat().st_size > 0
