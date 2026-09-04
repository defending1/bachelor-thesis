#!/usr/bin/env python3
"""
Numerical experiment to estimate the typical rank distribution of random tensors
of various formats (2x2x2, 3x3x2, 3x3x3, 3x3x5) under different entry distributions
(Normal N(0,1) and Uniform U(-1,1)) using TensorLy CP-ALS solver from experiments.utils.cp.
Generates a 1x4 publication plot.
"""

import os
import time
import json
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import scienceplots

from experiments.utils.cp import solve_cp_als

plt.style.use(['science', 'grid'])

script_dir = Path(__file__).parent


def fit_cp(T: np.ndarray, R: int, num_restarts: int = 15, max_iter: int = 300, tol: float = 1e-9):
    """
    Fits a CP decomposition of rank R with multiple restarts using TensorLy CP-ALS.
    """
    factors, rec_err = solve_cp_als(
        tensor=T,
        rank=R,
        n_iter_max=max_iter,
        tol=tol,
        n_restarts=num_restarts,
        restore_physical_scale=False,
    )
    return factors, rec_err


def estimate_rank(T: np.ndarray, max_rank: int = 7, tolerance: float = 1e-5, num_restarts: int = 15, max_iter: int = 300) -> int:
    """
    Estimates the CP rank of tensor T by finding the smallest rank r
    for which relative reconstruction error is below the tolerance.
    """
    for r in range(1, max_rank + 1):
        _, err = fit_cp(T, r, num_restarts=num_restarts, max_iter=max_iter, tol=tolerance)
        if err < tolerance:
            return r
    return max_rank + 1


def _eval_single(args):
    dist_name, shape, max_rank, num_restarts, max_iter, seed = args
    np.random.seed(seed)
    if dist_name == "Normal":
        T = np.random.normal(size=shape)
    elif dist_name == "Uniform":
        T = np.random.uniform(-1, 1, size=shape)
    else:
        raise ValueError(f"Unknown distribution {dist_name}")
    return estimate_rank(T, max_rank=max_rank, tolerance=1e-5, num_restarts=num_restarts, max_iter=max_iter)


def run_experiment(force_recompute=None):
    """
    Executes the typical rank estimation experiment across specified tensor formats.
    """
    base_seed = 42

    distributions = [
        {"name": "Normal", "label": r"Normal $\mathcal{N}(0, 1)$"},
        {"name": "Uniform", "label": r"Uniform $\mathcal{U}(-1, 1)$"}
    ]

    formats = [
        {"shape": (2, 2, 2), "num_samples": 200, "max_rank": 4, "num_restarts": 120, "max_iter": 500, "title": r"2 \times 2 \times 2"},
        {"shape": (3, 3, 2), "num_samples": 200, "max_rank": 5, "num_restarts": 120, "max_iter": 500, "title": r"3 \times 3 \times 2"},
        {"shape": (3, 3, 3), "num_samples": 100, "max_rank": 6, "num_restarts": 20, "max_iter": 300, "title": r"3 \times 3 \times 3"},
        {"shape": (3, 3, 5), "num_samples": 100, "max_rank": 7, "num_restarts": 120, "max_iter": 500, "title": r"3 \times 3 \times 5"}
    ]

    output_dir = script_dir
    json_path = output_dir / "experiment_results.json"

    results = {}
    if json_path.exists():
        print(f"Loading cached results from {json_path}...")
        with open(json_path, "r") as f:
            results = json.load(f)

    if force_recompute is None:
        force_recompute = {"2x2x2", "3x3x2"}

    print("Starting typical rank estimation experiment using TensorLy CP-ALS...")
    start_all = time.time()

    with ProcessPoolExecutor() as executor:
        for dist_idx, dist in enumerate(distributions):
            dist_name = dist["name"]
            if dist_name not in results:
                results[dist_name] = {}
            for fmt_idx, fmt in enumerate(formats):
                shape = fmt["shape"]
                shape_str = f"{shape[0]}x{shape[1]}x{shape[2]}"
                if shape_str in results[dist_name] and shape_str not in force_recompute:
                    print(f"Skipping {dist_name} format {shape_str} (using cached results).")
                    continue

                num_samples = fmt["num_samples"]
                max_rank = fmt["max_rank"]
                num_restarts = fmt.get("num_restarts", 15)
                max_iter = fmt.get("max_iter", 300)
                print(f"\nEvaluating {dist_name} distribution for format {shape} ({num_samples} samples, {num_restarts} restarts, {max_iter} max_iter)...")

                tasks = [
                    (dist_name, shape, max_rank, num_restarts, max_iter, base_seed + dist_idx * 10000 + fmt_idx * 1000 + i)
                    for i in range(num_samples)
                ]

                t0 = time.time()
                ranks = list(executor.map(_eval_single, tasks))
                t1 = time.time()
                print(f"Finished {dist_name} format {shape} in {t1 - t0:.2f} seconds.")
                results[dist_name][shape_str] = ranks

    total_time = time.time() - start_all
    print(f"\nEvaluations finished in {total_time:.2f} seconds.")

    with open(json_path, "w") as f:
        json.dump(results, f, indent=2)

    plot_from_results(results, distributions, formats, output_dir)


def plot_from_results(results, distributions, formats, output_dir):
    plt.rcParams.update({
        'font.family': 'serif',
        'font.serif': ['Computer Modern Roman', 'DejaVu Serif', 'Times New Roman', 'serif'],
        'text.usetex': False,
        'mathtext.fontset': 'cm',
        'axes.labelsize': 10.5,
        'axes.titlesize': 10.5,
        'xtick.labelsize': 9.5,
        'ytick.labelsize': 9.5,
        'figure.titlesize': 11
    })

    fig, axes = plt.subplots(1, 4, figsize=(9.6, 2.9), sharey=True)

    colors = {
        "Normal": "#2B5C8F",
        "Uniform": "#D96B27"
    }
    edge_colors = {
        "Normal": "#1A3B5C",
        "Uniform": "#8C4113"
    }

    bar_width = 0.36

    for col_idx, fmt in enumerate(formats):
        ax = axes[col_idx]
        shape = fmt["shape"]
        shape_str = f"{shape[0]}x{shape[1]}x{shape[2]}"

        normal_ranks = results["Normal"][shape_str]
        uniform_ranks = results["Uniform"][shape_str]

        u_norm, c_norm = np.unique(normal_ranks, return_counts=True)
        freq_norm = dict(zip(u_norm, c_norm / len(normal_ranks) * 100))

        u_unif, c_unif = np.unique(uniform_ranks, return_counts=True)
        freq_unif = dict(zip(u_unif, c_unif / len(uniform_ranks) * 100))

        all_ranks = sorted(list(set(u_norm) | set(u_unif)))

        ax.grid(False, axis='x')
        ax.grid(True, axis='y', linestyle='--', alpha=0.35, color='#CBD5E1', linewidth=0.7)
        ax.set_axisbelow(True)

        for r in all_ranks:
            f_n = freq_norm.get(r, 0.0)
            f_u = freq_unif.get(r, 0.0)

            if f_n > 0:
                ax.bar(
                    r - bar_width/2, f_n, width=bar_width,
                    color=colors["Normal"], edgecolor=edge_colors["Normal"],
                    linewidth=0.8, alpha=0.92, zorder=3
                )

            if f_u > 0:
                ax.bar(
                    r + bar_width/2, f_u, width=bar_width,
                    color=colors["Uniform"], edgecolor=edge_colors["Uniform"],
                    linewidth=0.8, alpha=0.92, zorder=3
                )

            if f_n == 100 and f_u == 100:
                ax.annotate(
                    "100%", xy=(r, 100),
                    xytext=(0, 3), textcoords="offset points",
                    ha='center', va='bottom', fontsize=8,
                    color='#1E293B'
                )
            else:
                if f_n > 0:
                    lbl_n = f"{f_n:.1f}%"
                    ax.annotate(
                        lbl_n, xy=(r - bar_width/2, f_n),
                        xytext=(-1, 2), textcoords="offset points",
                        ha='center', va='bottom', fontsize=7.2,
                        color='#1E293B', rotation=25
                    )
                if f_u > 0:
                    lbl_u = f"{f_u:.1f}%"
                    ax.annotate(
                        lbl_u, xy=(r + bar_width/2, f_u),
                        xytext=(1, 2), textcoords="offset points",
                        ha='center', va='bottom', fontsize=7.2,
                        color='#1E293B', rotation=25
                    )

        ax.set_title(rf"Format ${fmt['title']}$", fontsize=10.5, pad=8)

        ax.set_xticks(all_ranks)
        if len(all_ranks) == 1:
            ax.set_xlim(all_ranks[0] - 0.75, all_ranks[0] + 0.75)
        else:
            ax.set_xlim(min(all_ranks) - 0.6, max(all_ranks) + 0.6)

        ax.set_ylim(0, 118)

        show_y_ticks = (col_idx == 0)
        ax.tick_params(axis='x', which='both', top=False, bottom=True, labelsize=9.5, length=3.5, width=0.8)
        ax.tick_params(axis='y', which='both', left=show_y_ticks, right=False, labelsize=9.5, length=3.5, width=0.8)

        if not show_y_ticks:
            ax.spines['left'].set_visible(False)
        else:
            ax.spines['left'].set_linewidth(0.8)

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_linewidth(0.8)

    axes[0].set_ylabel(r"Empirical Frequency (%)", fontsize=10.5, labelpad=6)
    fig.text(0.5, 0.01, r"Tensor Rank ($r$)", ha='center', va='center', fontsize=10.5)

    legend_elements = [
        Patch(facecolor=colors["Normal"], edgecolor=edge_colors["Normal"], label=r"Normal $\mathcal{N}(0,1)$"),
        Patch(facecolor=colors["Uniform"], edgecolor=edge_colors["Uniform"], label=r"Uniform $\mathcal{U}(-1,1)$")
    ]
    fig.legend(
        handles=legend_elements,
        loc='upper center',
        bbox_to_anchor=(0.5, 1.05),
        ncol=2,
        frameon=False,
        fontsize=9.5
    )

    plt.tight_layout(rect=[0.01, 0.08, 0.99, 0.95])

    thesis_fig_dir = script_dir.parent.parent.parent / "Sources" / "Chapter1" / "figures"
    thesis_fig_dir.mkdir(parents=True, exist_ok=True)
    thesis_pdf = thesis_fig_dir / "typical_rank_distribution.pdf"

    plt.savefig(thesis_pdf, bbox_inches='tight', dpi=300)
    print(f"\nSuccess! Publication quality plot saved directly to {thesis_pdf}")


def main():
    run_experiment()


if __name__ == "__main__":
    main()
