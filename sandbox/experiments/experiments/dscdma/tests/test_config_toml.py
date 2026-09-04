"""
Unit tests for SimConfig TOML loading and updated CLI entry points.
"""

from pathlib import Path
from experiments.dscdma.config import SimConfig
from experiments.dscdma.cli import run_generator_cli, run_plot_cli


def test_sim_config_defaults_and_toml(tmp_path):
    config = SimConfig.from_toml()
    assert config.num_sources == 3
    assert config.num_antennas == 4
    assert config.spreading_gain == 16
    assert config.num_symbols == 100

    # Write a custom TOML config
    toml_path = tmp_path / "test_config.toml"
    toml_path.write_text(
        """
[dscdma]
num_sources = 2
num_antennas = 3
spreading_gain = 8
num_symbols = 50
area_side = 50.0
min_dist = 0.2
seed = 123
dataset_output = "custom_dataset.npz"
plot_output = "custom_plot.pdf"
restore_physical_scale = false
"""
    )

    custom_config = SimConfig.from_toml(toml_path)
    assert custom_config.num_sources == 2
    assert custom_config.num_antennas == 3
    assert custom_config.spreading_gain == 8
    assert custom_config.num_symbols == 50
    assert custom_config.area_side == 50.0
    assert custom_config.min_dist == 0.2
    assert custom_config.seed == 123
    assert custom_config.dataset_output == "custom_dataset.npz"
    assert custom_config.plot_output == "custom_plot.pdf"
    assert custom_config.restore_physical_scale is False


def test_cli_generator_and_plot(tmp_path):
    toml_path = tmp_path / "sim.toml"
    out_npz = tmp_path / "out_dataset.npz"
    out_pdf = tmp_path / "out_plot.pdf"

    toml_path.write_text(
        f"""
[dscdma]
num_sources = 2
num_antennas = 3
spreading_gain = 8
num_symbols = 20
seed = 42
dataset_output = "{out_npz}"
plot_output = "{out_pdf}"
"""
    )

    run_generator_cli(str(toml_path))
    assert out_npz.exists()

    run_plot_cli(str(toml_path))
    assert out_pdf.exists()
