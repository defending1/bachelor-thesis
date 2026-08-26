#!/usr/bin/env python3
"""
Fluorescence Spectroscopy (EEM) CP Decomposition Rank Selection Experiment.

Loads the Excitation-Emission Matrix (EEM) dataset and fits CP tensor
decompositions of increasing rank R until a relative reconstruction error
<= target_error is reached. Uses the refactored 'src' modules.

Usage via uv:
    uv run python eem_cp_experiment.py --target-error 0.05 --max-rank 10
"""

import argparse
import json
import sys
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

# Add src folder to python path
script_dir = Path(__file__).parent
sys.path.append(str(script_dir / "src"))

from cp.decomposition import run_experiment
from plots.utils import setup_plot_style, get_wavelength_ranges

def plot_results(results: dict, output_dir: Path):
    """Generate and save plots for rank vs error and factor components using shared styles."""
    setup_plot_style()
    output_dir.mkdir(parents=True, exist_ok=True)
    
    history = results['rank_history']
    ranks = [h['rank'] for h in history]
    errors = [h['relative_error'] for h in history]
    fits = [h['fit_percentage'] for h in history]
    target_err = results['target_error']
    final_rank = results['final_rank']
    final_err = results['final_error']

    # 1. Plot Error & Fit vs Rank
    fig, ax1 = plt.subplots(figsize=(8, 5))

    color_err = '#d62728'
    ax1.set_xlabel('CP Rank ($R$)', fontsize=12, fontweight='bold')
    ax1.set_ylabel(r'Relative Error ($\|X - \hat{X}\| / \|X\|$)', color=color_err, fontsize=12, fontweight='bold')
    line1 = ax1.plot(ranks, errors, 'o-', color=color_err, linewidth=2, markersize=8, label='Relative Error')
    ax1.axhline(y=target_err, color='black', linestyle='--', linewidth=1.5, label=f'Target $\\epsilon$ ({target_err})')
    ax1.axvline(x=final_rank, color='gray', linestyle=':', linewidth=1.5, label=f'Final Rank ($R^*={final_rank}$)')
    ax1.tick_params(axis='y', labelcolor=color_err)
    ax1.grid(True, linestyle=':', alpha=0.6)

    ax2 = ax1.twinx()
    color_fit = '#1f77b4'
    ax2.set_ylabel('Fit Percentage (%)', color=color_fit, fontsize=12, fontweight='bold')
    line2 = ax2.plot(ranks, fits, 's--', color=color_fit, linewidth=2, markersize=6, label='Fit %')
    ax2.tick_params(axis='y', labelcolor=color_fit)

    # Combine legends
    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='center right', framealpha=0.9)

    plt.title(f'EEM CP Decomposition: Error vs Rank (Final $R^*={final_rank}$, $\\epsilon^*={final_err:.4f}$)',
              fontsize=13, fontweight='bold', pad=15)
    plt.tight_layout()
    error_plot_path = output_dir / 'eem_cp_error_vs_rank.png'
    plt.savefig(error_plot_path, dpi=300)
    plt.close()
    print(f"Saved plot: {error_plot_path}")

    # 2. Plot Factors for Final Rank
    final_cp = results['cp_models'][final_rank]
    weights, factors = final_cp

    mode_ranges = results['data']['mode_ranges']
    em_range, ex_range = get_wavelength_ranges(mode_ranges)

    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))

    # Mode 1: Samples
    for r in range(final_rank):
        axes[0].plot(range(1, 19), factors[0][:, r], 'o-', label=f'Comp {r+1}')
    axes[0].set_title('Mode 1: Samples (Loadings)', fontweight='bold')
    axes[0].set_xlabel('Sample Index (1..18)')
    axes[0].set_ylabel('Loading')
    axes[0].grid(True, linestyle=':', alpha=0.5)
    axes[0].legend()

    # Mode 2: Emission
    for r in range(final_rank):
        axes[1].plot(em_range, factors[1][:, r], linewidth=2, label=f'Comp {r+1}')
    axes[1].set_title('Mode 2: Emission Spectrum', fontweight='bold')
    axes[1].set_xlabel('Wavelength (nm)')
    axes[1].set_ylabel('Intensity (a.u.)')
    axes[1].grid(True, linestyle=':', alpha=0.5)
    axes[1].legend()

    # Mode 3: Excitation
    for r in range(final_rank):
        axes[2].plot(ex_range, factors[2][:, r], linewidth=2, label=f'Comp {r+1}')
    axes[2].set_title('Mode 3: Excitation Spectrum', fontweight='bold')
    axes[2].set_xlabel('Wavelength (nm)')
    axes[2].set_ylabel('Intensity (a.u.)')
    axes[2].grid(True, linestyle=':', alpha=0.5)
    axes[2].legend()

    plt.suptitle(f'CP Factor Components at Rank $R^*={final_rank}$', fontsize=14, fontweight='bold')
    plt.tight_layout()
    comp_plot_path = output_dir / f'eem_cp_components_R{final_rank}.png'
    plt.savefig(comp_plot_path, dpi=300)
    plt.close()
    print(f"Saved plot: {comp_plot_path}")


def main():
    parser = argparse.ArgumentParser(description="EEM Spectroscopy CP Approximation Experiment")
    parser.add_argument("--mat-path", type=Path, default=script_dir / "EEM18.mat",
                        help="Path to EEM18.mat dataset")
    parser.add_argument("--target-error", "-e", type=float, default=0.05,
                        help="Target relative error threshold epsilon (default: 0.05)")
    parser.add_argument("--max-rank", "-r", type=int, default=10,
                        help="Maximum rank R to test (default: 10)")
    parser.add_argument("--n-restarts", type=int, default=5,
                        help="Number of random restarts per rank (default: 5)")
    parser.add_argument("--n-iter-max", type=int, default=1000,
                        help="Maximum iterations for CP decomposition (default: 1000)")
    parser.add_argument("--output-json", type=Path, default=script_dir / "experiment_results.json",
                        help="Output path for JSON experiment summary")
    parser.add_argument("--plot-dir", type=Path, default=script_dir,
                        help="Output directory for plots")

    args = parser.parse_args()

    results = run_experiment(
        mat_path=args.mat_path,
        target_error=args.target_error,
        max_rank=args.max_rank,
        n_restarts=args.n_restarts,
        n_iter_max=args.n_iter_max
    )

    plot_results(results, args.plot_dir)

    # Save JSON summary (without numpy arrays)
    summary_data = {
        'final_rank': results['final_rank'],
        'final_error': results['final_error'],
        'target_error': results['target_error'],
        'nonnegative': results['nonnegative'],
        'rank_history': results['rank_history']
    }

    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    with open(args.output_json, 'w') as f:
        json.dump(summary_data, f, indent=2)

    print(f"\nExperiment finished.")
    print(f"Results saved to JSON: {args.output_json}")
    print(f"FINAL RESULT: Rank = {results['final_rank']}, Relative Error = {results['final_error']:.6f}")


if __name__ == '__main__':
    main()
