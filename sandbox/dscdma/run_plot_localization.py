"""
CLI script for DS-CDMA CP decomposition and scatter plotting of users, true antennae,
recovered antennae, and distance circles centered around recovered antennae.

Usage:
    python run_plot_localization.py -r 3 -i 4 -j 16 -k 100 -s none -o antenna_localization_plot.pdf
"""

from dscdma.cli import run_plot_cli

if __name__ == "__main__":
    run_plot_cli()
