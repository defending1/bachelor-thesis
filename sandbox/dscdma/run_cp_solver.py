"""
Demonstration script for DS-CDMA CP-ALS Factor Recovery and Tensor Reconstruction.

Usage:
    python run_cp_solver.py -r 3 -i 4 -j 16 -k 100 -s 42
"""

from dscdma.cli import run_solver_cli

if __name__ == "__main__":
    run_solver_cli()
