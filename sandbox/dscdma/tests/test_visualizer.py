"""
Unit tests for DS-CDMA visualizer and antenna position estimation.
"""

from pathlib import Path
import numpy as np

from dscdma.config import SimConfig
from dscdma.generator import DSCDMADatasetGenerator
from dscdma.plot import estimate_antenna_positions, plot_antenna_and_radii


def test_estimate_antenna_positions():
    """
    Tests antenna position estimation from exact channel matrix A_true.
    """
    config = SimConfig(num_sources=3, num_antennas=4, seed=42)
    generator = DSCDMADatasetGenerator(config)
    data = generator.generate()

    user_pos = data["user_pos"]
    antenna_pos_true = data["antenna_pos"]
    A_true = data["A_true"]

    antenna_pos_est = estimate_antenna_positions(user_pos, A_true)

    # When using exact A_true, antenna positions should be recovered perfectly
    np.testing.assert_allclose(antenna_pos_est, antenna_pos_true, atol=1e-4)


def test_plot_antenna_and_radii(tmp_path: Path):
    """
    Tests figure generation and saving to disk.
    """
    config = SimConfig(num_sources=3, num_antennas=2, seed=123)
    generator = DSCDMADatasetGenerator(config)
    data = generator.generate()

    output_file = tmp_path / "test_plot.pdf"
    fig, ax = plot_antenna_and_radii(
        user_pos=data["user_pos"],
        antenna_pos_true=data["antenna_pos"],
        A_est=data["A_true"],
        save_path=str(output_file),
        show=False,
    )

    assert output_file.exists()
    assert output_file.stat().st_size > 0
