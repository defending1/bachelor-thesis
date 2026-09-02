"""
CLI script for DS-CDMA CP decomposition and scatter plotting of users, true antennae,
recovered antennae, and distance circles centered around recovered antennae.

Usage:
    python run_plot_localization.py -r 3 -i 4 -j 16 -k 100 -s 42 -o output_plot.png
"""

import argparse
import numpy as np

from config import SimConfig
from generator import DSCDMADatasetGenerator
from cp_solver import solve_cp_als
from visualizer import estimate_antenna_positions, plot_antenna_and_radii


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Plot DS-CDMA Users, Antennae, Recovered Antennae, and Distance Circles."
    )
    parser.add_argument("-r", "--sources", type=int, default=3, help="Number of sources/users (R)")
    parser.add_argument("-i", "--antennas", type=int, default=4, help="Number of receiver antennas (I)")
    parser.add_argument("-j", "--spreading", type=int, default=16, help="Spreading factor (J)")
    parser.add_argument("-k", "--symbols", type=int, default=100, help="Number of symbols (K)")
    parser.add_argument("-s", "--seed", type=int, default=42, help="Random seed")
    parser.add_argument("--area", type=float, default=100.0, help="2D area side length")
    parser.add_argument("-o", "--output", type=str, default="antenna_localization_plot.pdf", help="Output PDF path")
    parser.add_argument("--no-scale", action="store_true", help="Disable physical scale restoration")

    args = parser.parse_args()

    config = SimConfig(
        num_sources=args.sources,
        num_antennas=args.antennas,
        spreading_gain=args.spreading,
        num_symbols=args.symbols,
        area_side=args.area,
        seed=args.seed,
    )

    print("=" * 70)
    print("DS-CDMA ANTENNA RECOVERY AND DISTANCE CIRCLE PLOTTING")
    print("=" * 70)
    print(f"  R (Sources/Users): {config.num_sources}")
    print(f"  I (Antennas):      {config.num_antennas}")
    print(f"  J (Chips):         {config.spreading_gain}")
    print(f"  K (Signals):       {config.num_symbols}")
    print(f"  2D Area Side:      {config.area_side}")
    print(f"  Seed:              {config.seed}")
    print(f"  Output Plot:       {args.output}")
    print(f"  Restore Scale:     {not args.no_scale}")
    print("-" * 70)

    # 1. Generate synthetic dataset
    generator = DSCDMADatasetGenerator(config)
    data = generator.generate()

    T_true = data["tensor"]
    user_pos = data["user_pos"]
    antenna_pos_true = data["antenna_pos"]

    # 2. Decompose tensor via CP-ALS
    print(">>> Solving CP-ALS decomposition...")
    (A_est, C_est, S_est), rec_err = solve_cp_als(
        T_true,
        rank=config.num_sources,
        n_iter_max=2000,
        tol=1e-9,
        random_state=config.seed,
        restore_physical_scale=not args.no_scale,
    )
    print(f"  Relative Tensor Reconstruction Error: {rec_err:.6e}")

    # 3. Estimate antenna positions from raw A_est
    antenna_pos_est = estimate_antenna_positions(user_pos, A_est)

    print("\n>>> POSITIONS:")
    print("  User Positions:")
    for r in range(config.num_sources):
        print(f"    U{r+1}: ({user_pos[r, 0]:.2f}, {user_pos[r, 1]:.2f})")

    print("  True Antenna Positions:")
    for i in range(config.num_antennas):
        print(f"    A{i+1}: ({antenna_pos_true[i, 0]:.2f}, {antenna_pos_true[i, 1]:.2f})")

    print("  Recovered Antenna Positions:")
    for i in range(config.num_antennas):
        print(f"    A{i+1}_rec: ({antenna_pos_est[i, 0]:.2f}, {antenna_pos_est[i, 1]:.2f})")

    # 4. Generate Plot
    title = f"DS-CDMA Antenna & User Scatter Plot with Distance Circles (R={args.sources}, I={args.antennas})"
    plot_antenna_and_radii(
        user_pos=user_pos,
        antenna_pos_true=antenna_pos_true,
        A_est=A_est,
        antenna_pos_est=antenna_pos_est,
        title=title,
        save_path=args.output,
        show=False,
    )

    print("\n" + "=" * 70)
    print(f"SUCCESS: Plot generated and saved to '{args.output}'")
    print("=" * 70)


if __name__ == "__main__":
    main()
