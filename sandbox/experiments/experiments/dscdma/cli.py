"""
Command-line interface helpers and reusable entry points for DS-CDMA tasks.
Reads configuration parameters directly from a .toml config file.
"""

import sys
from pathlib import Path
from typing import Optional, Dict, Any, Union

from experiments.dscdma.config import SimConfig
from experiments.dscdma.utils.generator import DSCDMADatasetGenerator
from experiments.dscdma.solver import align_factors
from experiments.utils.cp import CP
from experiments.dscdma.utils.exporter import save_dataset, load_dataset
from experiments.dscdma.plot import plot_antenna_and_radii


def print_sim_banner(
    title: str, config: SimConfig, extra_info: Optional[Dict[str, Any]] = None
) -> None:
    """
    Prints a formatted summary banner for DS-CDMA simulation runs.
    """
    print("=" * 70)
    print(title.upper())
    print("=" * 70)
    print(f"  R (Sources/Users): {config.num_sources}")
    print(f"  I (Antennas):      {config.num_antennas}")
    print(f"  J (Chips):         {config.spreading_gain}")
    print(f"  K (Signals):       {config.num_symbols}")
    print(f"  2D Area Side:      {config.area_side}")
    print(f"  Seed:              {config.seed}")
    if extra_info:
        for key, val in extra_info.items():
            print(f"  {key:<18}: {val}")
    print("-" * 70)


def resolve_config_path(
    config_arg: Optional[Union[str, Path, list]] = None
) -> Optional[Union[str, Path]]:
    """
    Resolves config path from direct argument or command line args.
    """
    if isinstance(config_arg, (str, Path)):
        return config_arg
    if isinstance(config_arg, list) and len(config_arg) > 0:
        return config_arg[0]
    if len(sys.argv) > 1 and not sys.argv[1].startswith("-"):
        return sys.argv[1]
    return None


def run_generator_cli(config_arg: Optional[Union[str, Path, list]] = None) -> None:
    """
    CLI runner logic for generating synthetic DS-CDMA datasets using config.toml.
    """
    config_path = resolve_config_path(config_arg)
    config = SimConfig.from_toml(config_path)

    out_file = config.dataset_output

    print_sim_banner(
        "DS-CDMA Spatial Real Dataset Generator", config, {"Output File": out_file}
    )

    generator = DSCDMADatasetGenerator(config)
    data = generator.generate()

    out_path = save_dataset(data, out_file)
    print(f"\nDataset successfully saved to: {out_path.resolve()}")
    print(f"Tensor shape: {data['tensor'].shape}, dtype: {data['tensor'].dtype}")

    reloaded = load_dataset(out_path)
    print(f"Reload check passed: Rank R = {reloaded['rank_R']}")


def run_plot_cli(config_arg: Optional[Union[str, Path, list]] = None) -> None:
    """
    CLI runner logic for antenna localization scatter plotting using config.toml.
    """
    config_path = resolve_config_path(config_arg)
    config = SimConfig.from_toml(config_path)

    output_path = Path(config.plot_output)
    if output_path.suffix.lower() != ".pdf":
        output_path = output_path.with_suffix(".pdf")

    print_sim_banner(
        "DS-CDMA Antenna Recovery and Distance Circle Plotting",
        config,
        {
            "Output Plot": str(output_path),
            "Restore Scale": config.restore_physical_scale,
        },
    )

    generator = DSCDMADatasetGenerator(config)
    data = generator.generate()

    T_true = data["tensor"]
    user_pos = data["user_pos"]
    antenna_pos_true = data["antenna_pos"]

    print(">>> Solving CP-ALS decomposition...")
    cp = CP(T_true, config.num_sources).compute(
        n_iter_max=2000,
        tol=1e-9,
        random_state=config.seed,
        restore_physical_scale=config.restore_physical_scale,
    )
    print(f"  Relative Tensor Reconstruction Error: {cp.rec_error:.6e}")

    print(">>> Aligning recovered factors with ground-truth channel...")
    align_factors(cp, data["A_true"])

    title = f"Antenna & User Scatter Plot with Distance Circles (R={config.num_sources}, I={config.num_antennas})"
    plot_antenna_and_radii(
        user_pos=user_pos,
        antenna_pos_true=antenna_pos_true,
        A_est=cp.A,
        S_est=cp.S,
        title=title,
        save_path=str(output_path),
        show=False,
        area_side=config.area_side,
    )


    print("\n" + "=" * 70)
    print(f"SUCCESS: Plot generated and saved to '{output_path}'")
    print("=" * 70)

