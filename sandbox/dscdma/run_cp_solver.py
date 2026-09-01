"""
Demonstration script for DS-CDMA CP-ALS Factor Recovery and Tensor Reconstruction.

Generates 2D planar user/antenna positions, spatial channel matrix A, random binary codes C,
generic real signal matrix S, and 3D real tensor T. Then decomposes T using TensorLy CP-ALS.

Usage:
    python run_cp_solver.py -r 3 -i 4 -j 16 -k 100 -s 42
"""

import argparse
import numpy as np

from config import SimConfig
from generator import DSCDMADatasetGenerator
from cp_solver import solve_cp_als


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Factorize DS-CDMA Real Tensor using TensorLy CP-ALS."
    )
    parser.add_argument("-r", "--sources", type=int, default=3, help="Number of sources (R)")
    parser.add_argument("-i", "--antennas", type=int, default=4, help="Number of antennas (I)")
    parser.add_argument("-j", "--spreading", type=int, default=16, help="Spreading factor (J)")
    parser.add_argument("-k", "--symbols", type=int, default=100, help="Number of real signals/symbols (K)")
    parser.add_argument("-s", "--seed", type=int, default=42, help="Random seed")
    parser.add_argument("--area", type=float, default=100.0, help="2D area side length")

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
    print("DS-CDMA TENSOR DECOMPOSITION (CP-ALS via TensorLy)")
    print("=" * 70)
    print(f"  R (Sources):    {config.num_sources}")
    print(f"  I (Antennas):   {config.num_antennas}")
    print(f"  J (Chips):      {config.spreading_gain}")
    print(f"  K (Signals):    {config.num_symbols}")
    print(f"  2D Area Side:   {config.area_side}")
    print(f"  Seed:           {config.seed}")
    print("-" * 70)

    # 1. Generate Dataset
    generator = DSCDMADatasetGenerator(config)
    data = generator.generate()

    T_true = data["tensor"]

    print(f"Generated Real Tensor Shape: {T_true.shape}")
    print(f"Tensor Frobenius Norm:      {np.linalg.norm(T_true):.4f}\n")

    # 2. Factorize via CP-ALS
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


if __name__ == "__main__":
    main()
