#!/usr/bin/env python3
"""
Numerical experiment to estimate the typical rank distribution of random tensors
of various formats (2x2x2, 3x3x2, 3x3x3, 3x3x5) under different entry distributions
(Normal N(0,1) and Uniform U(-1,1)) using a custom NumPy-based CP-ALS solver.
Generates a 2x4 grid plot.
"""

import os
import time
import shutil
import json
from concurrent.futures import ProcessPoolExecutor
import numpy as np
import matplotlib.pyplot as plt
import scienceplots

plt.style.use(['science', 'grid'])

def khatri_rao(A, B):
    """
    Computes the Khatri-Rao product of two matrices A and B with the same number of columns.
    A: (I, R), B: (J, R) -> returns: (I*J, R)
    """
    R = A.shape[1]
    return (A[:, None, :] * B[None, :, :]).reshape(-1, R)

def cp_als(T, R, max_iter=300, tol=1e-9, init=None):
    """
    Alternating Least Squares (ALS) algorithm for CP decomposition of a 3-way tensor T.
    T: (I, J, K) tensor
    R: target rank
    """
    I, J, K = T.shape
    
    if init is None:
        A = np.random.normal(size=(I, R))
        B = np.random.normal(size=(J, R))
        C = np.random.normal(size=(K, R))
    else:
        A, B, C = init
        
    T_1 = np.transpose(T, (0, 2, 1)).reshape(I, -1)
    T_2 = np.transpose(T, (1, 2, 0)).reshape(J, -1)
    T_3 = np.transpose(T, (2, 1, 0)).reshape(K, -1)
    
    norm_T = np.linalg.norm(T)
    if norm_T == 0:
        return np.zeros((I, R)), np.zeros((J, R)), np.zeros((K, R)), [0.0]
        
    rel_errors = []
    
    for iteration in range(max_iter):
        # Update A
        C_kr_B = khatri_rao(C, B)
        V_A = (C.T @ C) * (B.T @ B)
        A = (T_1 @ C_kr_B) @ np.linalg.pinv(V_A)
        # Normalize columns of A to avoid scaling issues
        lambda_A = np.linalg.norm(A, axis=0)
        lambda_A[lambda_A < 1e-12] = 1.0
        A = A / lambda_A
        
        # Update B
        C_kr_A = khatri_rao(C, A)
        V_B = (C.T @ C) * (A.T @ A)
        B = (T_2 @ C_kr_A) @ np.linalg.pinv(V_B)
        # Normalize columns of B
        lambda_B = np.linalg.norm(B, axis=0)
        lambda_B[lambda_B < 1e-12] = 1.0
        B = B / lambda_B
        
        # Update C (C absorbs the scale factors)
        B_kr_A = khatri_rao(B, A)
        V_C = (B.T @ B) * (A.T @ A)
        C = (T_3 @ B_kr_A) @ np.linalg.pinv(V_C)
        
        # Reconstruct and compute error
        T_hat = np.einsum('ir,jr,kr->ijk', A, B, C)
        err = np.linalg.norm(T - T_hat) / norm_T
        rel_errors.append(err)
        
        if iteration > 0 and abs(rel_errors[-2] - rel_errors[-1]) < tol:
            break
            
    return A, B, C, rel_errors

def fit_cp(T, R, num_restarts=15, max_iter=300, tol=1e-9):
    """
    Fits a CP decomposition of rank R with multiple random restarts.
    """
    best_err = float('inf')
    best_decomp = None
    
    for _ in range(num_restarts):
        A, B, C, errors = cp_als(T, R, max_iter=max_iter, tol=tol)
        if errors[-1] < best_err:
            best_err = errors[-1]
            best_decomp = (A, B, C)
            
    return best_decomp, best_err

def estimate_rank(T, max_rank=7, tolerance=1e-5, num_restarts=15):
    """
    Estimates the CP rank of tensor T by finding the smallest rank r
    for which the relative error is below the tolerance.
    """
    for r in range(1, max_rank + 1):
        _, err = fit_cp(T, r, num_restarts=num_restarts)
        if err < tolerance:
            return r
    return max_rank + 1

def _eval_single(args):
    dist_name, shape, max_rank, seed = args
    np.random.seed(seed)
    if dist_name == "Normal":
        T = np.random.normal(size=shape)
    elif dist_name == "Uniform":
        T = np.random.uniform(-1, 1, size=shape)
    else:
        raise ValueError(f"Unknown distribution {dist_name}")
    return estimate_rank(T, max_rank=max_rank, tolerance=1e-5, num_restarts=15)

def run_experiment():
    base_seed = 42
    
    distributions = [
        {"name": "Normal", "label": r"Normal $\mathcal{N}(0, 1)$"},
        {"name": "Uniform", "label": r"Uniform $\mathcal{U}(-1, 1)$"}
    ]
    
    formats = [
        {"shape": (2, 2, 2), "num_samples": 200, "max_rank": 4, "title": r"2 \times 2 \times 2"},
        {"shape": (3, 3, 2), "num_samples": 200, "max_rank": 5, "title": r"3 \times 3 \times 2"},
        {"shape": (3, 3, 3), "num_samples": 100, "max_rank": 6, "title": r"3 \times 3 \times 3"},
        {"shape": (3, 3, 5), "num_samples": 100, "max_rank": 7, "title": r"3 \times 3 \times 5"}
    ]
    
    output_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(output_dir, "experiment_results.json")
    
    if os.path.exists(json_path):
        print(f"Loading cached results from {json_path}...")
        with open(json_path, "r") as f:
            results = json.load(f)
    else:
        print("Starting typical rank estimation experiment (2x4 grid)...")
        start_all = time.time()
        
        with ProcessPoolExecutor() as executor:
            for dist_idx, dist in enumerate(distributions):
                dist_name = dist["name"]
                results[dist_name] = {}
                for fmt_idx, fmt in enumerate(formats):
                    shape = fmt["shape"]
                    shape_str = f"{shape[0]}x{shape[1]}x{shape[2]}"
                    num_samples = fmt["num_samples"]
                    max_rank = fmt["max_rank"]
                    print(f"\nEvaluating {dist_name} distribution for format {shape} ({num_samples} samples)...")
                    
                    tasks = [
                        (dist_name, shape, max_rank, base_seed + dist_idx * 10000 + fmt_idx * 1000 + i)
                        for i in range(num_samples)
                    ]
                    
                    t0 = time.time()
                    ranks = list(executor.map(_eval_single, tasks))
                    t1 = time.time()
                    print(f"Finished {dist_name} format {shape} in {t1 - t0:.2f} seconds.")
                    results[dist_name][shape_str] = ranks

        total_time = time.time() - start_all
        print(f"\nAll evaluations finished in {total_time:.2f} seconds.")

        with open(json_path, "w") as f:
            json.dump(results, f, indent=2)

    plot_from_results(results, distributions, formats, output_dir)

from matplotlib.patches import Patch

def plot_from_results(results, distributions, formats, output_dir):
    # Publication quality matplotlib setup
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
    
    # 1x4 grid (Single row layout)
    fig, axes = plt.subplots(1, 4, figsize=(9.6, 2.9), sharey=True)
    
    colors = {
        "Normal": "#2B5C8F",   # Deep Slate Blue
        "Uniform": "#D96B27"   # Warm Burnt Amber
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
        
        # Get rank frequencies for both distributions
        normal_ranks = results["Normal"][shape_str]
        uniform_ranks = results["Uniform"][shape_str]
        
        u_norm, c_norm = np.unique(normal_ranks, return_counts=True)
        freq_norm = dict(zip(u_norm, c_norm / len(normal_ranks) * 100))
        
        u_unif, c_unif = np.unique(uniform_ranks, return_counts=True)
        freq_unif = dict(zip(u_unif, c_unif / len(uniform_ranks) * 100))
        
        all_ranks = sorted(list(set(u_norm) | set(u_unif)))
        
        # Clean horizontal grid lines
        ax.grid(False, axis='x')
        ax.grid(True, axis='y', linestyle='--', alpha=0.35, color='#CBD5E1', linewidth=0.7)
        ax.set_axisbelow(True)
        
        # Draw side-by-side bars for each rank
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
                
            # Smart percentage annotation placement to prevent overlap
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
                
        # Column title
        ax.set_title(rf"Format ${fmt['title']}$", fontsize=10.5, pad=8)
        
        # X tick configuration
        ax.set_xticks(all_ranks)
        if len(all_ranks) == 1:
            ax.set_xlim(all_ranks[0] - 0.75, all_ranks[0] + 0.75)
        else:
            ax.set_xlim(min(all_ranks) - 0.6, max(all_ranks) + 0.6)
            
        ax.set_ylim(0, 118)
        
        # Spine & tick formatting
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

    # Shared Y-axis label on left
    axes[0].set_ylabel(r"Empirical Frequency (%)", fontsize=10.5, labelpad=6)

    # Shared X-axis label centered at bottom
    fig.text(0.5, 0.01, r"Tensor Rank ($r$)", ha='center', va='center', fontsize=10.5)

    # Global legend at the top
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
    
    thesis_fig_dir = os.path.abspath(os.path.join(output_dir, "../../Sources/Chapter1/figures"))
    os.makedirs(thesis_fig_dir, exist_ok=True)
    thesis_pdf = os.path.join(thesis_fig_dir, "typical_rank_distribution.pdf")
    
    plt.savefig(thesis_pdf, bbox_inches='tight', dpi=300)
    print(f"\nSuccess! Publication quality plot saved directly to {thesis_pdf}")





if __name__ == "__main__":
    run_experiment()
