"""
Command-line interface helpers and reusable entry points for DS-CDMA tasks.
"""

import argparse
from pathlib import Path
from typing import Optional, Dict, Any
import numpy as np

from dscdma.config import SimConfig
from dscdma.generator import DSCDMADatasetGenerator
from dscdma.cp_solver import solve_cp_als
from dscdma.exporter import save_dataset, load_dataset
from dscdma.plot import estimate_antenna_positions, plot_antenna_and_radii


def parse_seed(value: Optional[str]) -> Optional[int]:
    """
    Parses seed argument value converting string representations of None to None.
    """
    if value is None or (isinstance(value, str) and value.lower() in ("none", "null", "random", "")):
        return None
    return int(value)


def build_common_parser(description: str) -> argparse.ArgumentParser:
    """
    Creates an ArgumentParser pre-populated with standard DS-CDMA parameters.
    """
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-r", "--sources", type=int, default=3, help="Number of sources/users (R)")
    parser.add_argument("-i", "--antennas", type=int, default=4, help="Number of receiver antennas (I)")
    parser.add_argument("-j", "--spreading", type=int, default=16, help="Spreading factor / Walsh code length (J)")
    parser.add_argument("-k", "--symbols", type=int, default=100, help="Number of transmitted real signals (K)")
    parser.add_argument("-s", "--seed", type=parse_seed, default=None, help="Random seed (int, or 'none' for random on each run)")
    parser.add_argument("--presentation", action="store_true", help="Use fixed reproducible seed (seed=42) for presentation demo")
    parser.add_argument("--area", type=float, default=100.0, help="2D area side length")
    return parser


def config_from_args(args: argparse.Namespace) -> SimConfig:
    """
    Constructs and validates a SimConfig from parsed CLI arguments.
    """
    seed = 42 if (getattr(args, "presentation", False) and args.seed is None) else args.seed
    config = SimConfig(
        num_sources=args.sources,
        num_antennas=args.antennas,
        spreading_gain=args.spreading,
        num_symbols=args.symbols,
        area_side=args.area,
        seed=seed,
    )
    config.validate()
    return config


def print_sim_banner(title: str, config: SimConfig, extra_info: Optional[Dict[str, Any]] = None) -> None:
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


def run_generator_cli(args_list: Optional[list] = None) -> None:
    """
    CLI runner logic for generating synthetic DS-CDMA datasets.
    """
    parser = build_common_parser("Generate exact rank-R DS-CDMA real tensor dataset for CP decomposition experiments.")
    parser.add_argument("-o", "--out", type=str, default="dscdma_dataset.npz", help="Output .npz file path")

    args = parser.parse_args(args_list)
    config = config_from_args(args)

    print_sim_banner("DS-CDMA Spatial Real Dataset Generator", config, {"Output File": args.out})

    generator = DSCDMADatasetGenerator(config)
    data = generator.generate()

    out_path = save_dataset(data, args.out)
    print(f"\nDataset successfully saved to: {out_path.resolve()}")
    print(f"Tensor shape: {data['tensor'].shape}, dtype: {data['tensor'].dtype}")

    reloaded = load_dataset(out_path)
    print(f"Reload check passed: Rank R = {reloaded['rank_R']}")


def run_solver_cli(args_list: Optional[list] = None) -> None:
    """
    CLI runner logic for factorizing DS-CDMA real tensors via CP-ALS.
    """
    parser = build_common_parser("Factorize DS-CDMA Real Tensor using TensorLy CP-ALS.")
    args = parser.parse_args(args_list)
    config = config_from_args(args)

    print_sim_banner("DS-CDMA Tensor Decomposition (CP-ALS via TensorLy)", config)

    generator = DSCDMADatasetGenerator(config)
    data = generator.generate()

    T_true = data["tensor"]

    print(f"Generated Real Tensor Shape: {T_true.shape}")
    print(f"Tensor Frobenius Norm:      {np.linalg.norm(T_true):.4f}\n")

    print(">>> EXECUTING TENSORLY CP-ALS DECOMPOSITION...")
    (A_est, C_est, S_est), rec_err = solve_cp_als(
        T_true,
        rank=config.num_sources,
        n_iter_max=2000,
        tol=1e-9,
        random_state=config.seed,
    )

    print("\n>>> ESTIMATED FACTOR SHAPES:")
    print(f"  A_est shape: {A_est.shape}")
    print(f"  C_est shape: {C_est.shape}")
    print(f"  S_est shape: {S_est.shape}")
    print(f"\n  Relative Tensor Reconstruction Error: {rec_err:.6e}")

    print("\n" + "=" * 70)
    if rec_err < 1e-4:
        print("SUCCESS: Low Reconstruction Error Achieved!")
    print("=" * 70)


def run_plot_cli(args_list: Optional[list] = None) -> None:
    """
    CLI runner logic for antenna localization scatter plotting.
    """
    parser = build_common_parser("Plot DS-CDMA Users, Antennae, Recovered Antennae, and Distance Circles.")
    parser.add_argument("-o", "--output", type=str, default="antenna_localization_plot.pdf", help="Output PDF path")
    parser.add_argument("--no-scale", action="store_true", help="Disable physical scale restoration")

    args = parser.parse_args(args_list)
    config = config_from_args(args)

    output_path = Path(args.output)
    if output_path.suffix.lower() != ".pdf":
        output_path = output_path.with_suffix(".pdf")

    print_sim_banner(
        "DS-CDMA Antenna Recovery and Distance Circle Plotting",
        config,
        {
            "Output Plot": str(output_path),
            "Restore Scale": not args.no_scale,
        },
    )

    generator = DSCDMADatasetGenerator(config)
    data = generator.generate()

    T_true = data["tensor"]
    user_pos = data["user_pos"]
    antenna_pos_true = data["antenna_pos"]

    print(">>> Solving CP-ALS decomposition...")
    (A_est, _, S_est), rec_err = solve_cp_als(
        T_true,
        rank=config.num_sources,
        n_iter_max=2000,
        tol=1e-9,
        random_state=config.seed,
        restore_physical_scale=not args.no_scale,
    )
    print(f"  Relative Tensor Reconstruction Error: {rec_err:.6e}")

    antenna_pos_est, user_pos_est = estimate_antenna_positions(S_est, A_est, config.area_side)

    print("\n>>> POSITIONS:")
    print("  True User Positions:")
    for r in range(config.num_sources):
        print(f"    U{r + 1}: ({user_pos[r, 0]:.2f}, {user_pos[r, 1]:.2f})")

    print("  Recovered User Positions (Extracted from S_est):")
    for r in range(config.num_sources):
        print(f"    U{r + 1}_rec: ({user_pos_est[r, 0]:.2f}, {user_pos_est[r, 1]:.2f})")

    print("  True Antenna Positions:")
    for i in range(config.num_antennas):
        print(f"    A{i + 1}: ({antenna_pos_true[i, 0]:.2f}, {antenna_pos_true[i, 1]:.2f})")

    print("  Recovered Antenna Positions:")
    for i in range(config.num_antennas):
        print(f"    A{i + 1}_rec: ({antenna_pos_est[i, 0]:.2f}, {antenna_pos_est[i, 1]:.2f})")

    title = f"Antenna & User Scatter Plot with Distance Circles (R={config.num_sources}, I={config.num_antennas})"
    plot_antenna_and_radii(
        user_pos=user_pos,
        antenna_pos_true=antenna_pos_true,
        A_est=A_est,
        S_est=S_est,
        antenna_pos_est=antenna_pos_est,
        title=title,
        save_path=str(output_path),
        show=False,
        area_side=config.area_side,
    )

    print("\n" + "=" * 70)
    print(f"SUCCESS: Plot generated and saved to '{output_path}'")
    print("=" * 70)
