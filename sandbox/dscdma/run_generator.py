"""
CLI runner script to generate and save DS-CDMA synthetic datasets.

Usage:
    python run_generator.py --sources 3 --antennas 2 --spreading 16 --symbols 100 --out dataset.npz
"""

import argparse
from pathlib import Path

from config import SimConfig
from generator import DSCDMADatasetGenerator
from exporter import save_dataset, load_dataset


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate exact rank-R DS-CDMA tensor dataset for CP decomposition experiments."
    )
    parser.add_argument("-r", "--sources", type=int, default=3, help="Number of sources/users (R)")
    parser.add_argument("-i", "--antennas", type=int, default=2, help="Number of receiver antennas (I)")
    parser.add_argument("-j", "--spreading", type=int, default=16, help="Spreading factor / Walsh code length (J)")
    parser.add_argument("-k", "--symbols", type=int, default=100, help="Number of transmitted symbols (K)")
    parser.add_argument("-s", "--seed", type=int, default=42, help="Random seed")
    parser.add_argument("-o", "--out", type=str, default="dscdma_dataset.npz", help="Output .npz file path")

    args = parser.parse_args()

    config = SimConfig(
        num_sources=args.sources,
        num_antennas=args.antennas,
        spreading_gain=args.spreading,
        num_symbols=args.symbols,
        seed=args.seed
    )

    print("Generating DS-CDMA Dataset with parameters:")
    print(f"  R (Sources):  {config.num_sources}")
    print(f"  I (Antennas): {config.num_antennas}")
    print(f"  J (Chips):    {config.spreading_gain}")
    print(f"  K (Symbols):  {config.num_symbols}")
    print(f"  Seed:         {config.seed}")

    generator = DSCDMADatasetGenerator(config)
    data = generator.generate()

    out_path = save_dataset(data, args.out)
    print(f"\nDataset successfully saved to: {out_path.resolve()}")
    print(f"Tensor shape: {data['tensor'].shape}, dtype: {data['tensor'].dtype}")

    # Reload check
    reloaded = load_dataset(out_path)
    print(f"Reload check passed: Rank R = {reloaded['rank_R']}")


if __name__ == "__main__":
    main()
