#!/usr/bin/env python3
"""
Fluorescence Spectroscopy (EEM) CP Decomposition Rank Selection Experiment.

This script loads the Excitation-Emission Matrix (EEM) dataset from EEM18.mat
and fits CP (CANDECOMP/PARAFAC) tensor decompositions of increasing rank R
until a relative reconstruction error <= target_error (epsilon) is reached.

Usage via uv:
    uv run python sandbox/tensor_data_eem/eem_cp_experiment.py --target-error 0.05 --max-rank 10
"""

import argparse
import json
import time
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import scipy.io as sio
import tensorly as tl
from tensorly.decomposition import non_negative_parafac, parafac


def load_eem_data(mat_path: Path):
    """Load preprocessed EEM tensor data and metadata from EEM18.mat."""
    if not mat_path.exists():
        raise FileNotFoundError(f"Dataset file not found at {mat_path}")

    mat = sio.loadmat(str(mat_path))

    # Extract X (MatlabObject / struct with field 'data')
    x_obj = mat['X'][0, 0]
    x_tensor = np.asarray(x_obj['data'], dtype=np.float64)

    # Extract metadata if available
    mixtures = mat.get('mixtures', None)
    compound_names = mat.get('compound_names', None)
    mode_ranges = mat.get('mode_ranges', None)
    mode_titles = mat.get('mode_titles', None)

    return {
        'X': x_tensor,
        'mixtures': mixtures,
        'compound_names': compound_names,
        'mode_ranges': mode_ranges,
        'mode_titles': mode_titles
    }


def fit_cp_with_restarts(X: np.ndarray, rank: int, nonnegative: bool = True,
                         n_iter_max: int = 1000, n_restarts: int = 5, tol: float = 1e-7):
    """
    Fit CP decomposition of specified rank with multiple random initializations
    to avoid local minima. Returns the best tensor factor representation and error.
    """
    best_error = float('inf')
    best_cp = None
    best_time = 0.0

    x_norm = tl.norm(X)

    for trial in range(n_restarts):
        start_t = time.time()
        random_state = 42 + trial * 100

        if nonnegative:
            cp_tensor = non_negative_parafac(
                X, rank=rank, n_iter_max=n_iter_max, tol=tol,
                init='random', random_state=random_state
            )
        else:
            cp_tensor = parafac(
                X, rank=rank, n_iter_max=n_iter_max, tol=tol,
                init='random', random_state=random_state
            )

        elapsed = time.time() - start_t

        reconstruction = tl.cp_to_tensor(cp_tensor)
        rel_error = float(tl.norm(X - reconstruction) / x_norm)

        if rel_error < best_error:
            best_error = rel_error
            best_cp = cp_tensor
            best_time = elapsed

    return best_cp, best_error, best_time


def run_experiment(mat_path: Path, target_error: float, max_rank: int,
                   nonnegative: bool, n_restarts: int, n_iter_max: int):
    """
    Run experiment: test CP decomposition of increasing rank R = 1..max_rank
    until relative error <= target_error.
    """
    data = load_eem_data(mat_path)
    X = data['X']

    print("=" * 65)
    print(f"EEM Tensor Spectroscopy Experiment")
    print(f"Tensor Shape: {X.shape} (Samples x Emission x Excitation)")
    print(f"Target Error Epsilon: {target_error:.4f} ({target_error * 100:.2f}%)")
    print(f"Decomposition Type: {'Non-negative CP (NCP)' if nonnegative else 'Standard CP-ALS'}")
    print(f"Max Rank: {max_rank}")
    print("=" * 65)

    rank_history = []
    final_rank = None
    final_error = None
    best_cp_models = {}

    for rank in range(1, max_rank + 1):
        cp_model, rel_error, elapsed = fit_cp_with_restarts(
            X, rank=rank, nonnegative=nonnegative,
            n_iter_max=n_iter_max, n_restarts=n_restarts
        )

        fit_percentage = (1.0 - rel_error) * 100.0
        best_cp_models[rank] = cp_model

        rank_history.append({
            'rank': rank,
            'relative_error': rel_error,
            'fit_percentage': fit_percentage,
            'fit_time_sec': elapsed
        })

        print(f"Rank {rank:2d}: Relative Error = {rel_error:.6f} | Fit = {fit_percentage:6.2f}% | Time = {elapsed:.3f}s")

        if rel_error <= target_error and final_rank is None:
            final_rank = rank
            final_error = rel_error
            print(f"\n>>> Target error threshold reached at Rank {final_rank}! Final Error = {final_error:.6f} <<<")
            break

    if final_rank is None:
        # If target error not reached within max_rank
        final_rank = max_rank
        final_error = rank_history[-1]['relative_error']
        print(f"\n>>> Target error not reached within max_rank={max_rank}. Final Rank = {final_rank}, Error = {final_error:.6f} <<<")

    return {
        'final_rank': final_rank,
        'final_error': final_error,
        'target_error': target_error,
        'nonnegative': nonnegative,
        'rank_history': rank_history,
        'cp_models': best_cp_models,
        'data': data
    }


def plot_results(results: dict, output_dir: Path):
    """Generate and save plots for rank vs error and factor components."""
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
    # factors[0]: Sample loadings (18, R)
    # factors[1]: Emission spectra (251, R)
    # factors[2]: Excitation spectra (21, R)

    mode_ranges = results['data']['mode_ranges']
    em_range = np.linspace(250, 500, 251) if mode_ranges is None else mode_ranges[0, 1].squeeze()
    ex_range = np.linspace(210, 310, 21) if mode_ranges is None else mode_ranges[0, 2].squeeze()

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
    parser.add_argument("--mat-path", type=Path, default=Path("EEM18.mat"),
                        help="Path to EEM18.mat dataset (default: EEM18.mat)")
    parser.add_argument("--target-error", "-e", type=float, default=0.05,
                        help="Target relative error threshold epsilon (default: 0.05)")
    parser.add_argument("--max-rank", "-r", type=int, default=10,
                        help="Maximum rank R to test (default: 10)")
    parser.add_argument("--standard-cp", action="store_true",
                        help="Use standard unconstrained CP-ALS instead of Non-negative CP")
    parser.add_argument("--n-restarts", type=int, default=5,
                        help="Number of random restarts per rank (default: 5)")
    parser.add_argument("--n-iter-max", type=int, default=1000,
                        help="Maximum iterations for CP decomposition (default: 1000)")
    parser.add_argument("--output-json", type=Path, default=Path("experiment_results.json"),
                        help="Output path for JSON experiment summary (default: experiment_results.json)")
    parser.add_argument("--plot-dir", type=Path, default=Path("."),
                        help="Output directory for plots (default: .)")

    args = parser.parse_args()

    nonnegative = not args.standard_cp
    results = run_experiment(
        mat_path=args.mat_path,
        target_error=args.target_error,
        max_rank=args.max_rank,
        nonnegative=nonnegative,
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
