"""
CLI runner script to generate and save real DS-CDMA synthetic datasets.

Usage:
    python run_generator.py --sources 3 --antennas 4 --spreading 16 --symbols 100 --out dataset.npz
"""

from dscdma.cli import run_generator_cli

if __name__ == "__main__":
    run_generator_cli()
