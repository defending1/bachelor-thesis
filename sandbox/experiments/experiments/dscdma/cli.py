"""
Command-line interface helpers and reusable entry points for DS-CDMA tasks.
Reads configuration parameters directly from a .toml config file.
"""

import sys
from pathlib import Path
from typing import Optional, Dict, Any, Union

from experiments.dscdma.config import SimConfig
from experiments.dscdma.utils.generator import DSCDMADatasetGenerator
from experiments.dscdma.solver import align_factors
from experiments.utils.cp import CP
from experiments.dscdma.utils.exporter import save_dataset, load_dataset
from experiments.dscdma.plot import (
    plot_antenna_and_radii,
    plot_antenna_localization_multi,
    generate_multi_plot_pdf,
    generate_dscdma_noise_experiment_pdf,
    generate_dscdma_noise_multi_experiment_pdf,
)


def print_sim_banner(
    title: str, config: SimConfig, extra_info: Optional[Dict[str, Any]] = None
) -> None:
    """
    Prints a formatted summary banner for DS-CDMA simulation runs.
    """
    print("=" * 70)
    print(title.upper())
    print("=" * 70)
    print(f"  R (Sources/Users): {config.num_sources}")
    print(f"  I (Antennas):      {config.num_antennas}")
    print(f"  J (Chips):         {config.spreading_gain}")
    print(f"  K (Signals):       {config.num_symbols}")
    print(f"  2D Area Side:      {config.area_side}")
    print(f"  Seed:              {config.seed}")
    if extra_info:
        for key, val in extra_info.items():
            print(f"  {key:<18}: {val}")
    print("-" * 70)


def resolve_config_path(
    config_arg: Optional[Union[str, Path, list]] = None
) -> Optional[Union[str, Path]]:
    """
    Resolves config path from direct argument or command line args.
    """
    if isinstance(config_arg, (str, Path)):
        return config_arg
    if isinstance(config_arg, list) and len(config_arg) > 0:
        return config_arg[0]
    if len(sys.argv) > 1 and not sys.argv[1].startswith("-"):
        return sys.argv[1]
    return None


def run_generator_cli(config_arg: Optional[Union[str, Path, list]] = None) -> None:
    """
    CLI runner logic for generating synthetic DS-CDMA datasets using config.toml.
    """
    config_path = resolve_config_path(config_arg)
    config = SimConfig.from_toml(config_path)

    out_file = config.dataset_output

    print_sim_banner(
        "DS-CDMA Spatial Real Dataset Generator", config, {"Output File": out_file}
    )

    generator = DSCDMADatasetGenerator(config)
    data = generator.generate()

    out_path = save_dataset(data, out_file)
    print(f"\nDataset successfully saved to: {out_path.resolve()}")
    print(f"Tensor shape: {data['tensor'].shape}, dtype: {data['tensor'].dtype}")

    reloaded = load_dataset(out_path)
    print(f"Reload check passed: Rank R = {reloaded['rank_R']}")


def run_plot_cli(config_arg: Optional[Union[str, Path, list]] = None) -> None:
    """
    CLI runner logic for antenna localization scatter plotting using config.toml.
    """
    config_path = resolve_config_path(config_arg)
    config = SimConfig.from_toml(config_path)

    output_path = Path(config.plot_output)
    if output_path.suffix.lower() != ".pdf":
        output_path = output_path.with_suffix(".pdf")

    print_sim_banner(
        "DS-CDMA Antenna Recovery and Distance Circle Plotting",
        config,
        {
            "Output Plot": str(output_path),
        },
    )

    generator = DSCDMADatasetGenerator(config)
    data = generator.generate()

    T_true = data["tensor"]
    user_pos = data["user_pos"]
    antenna_pos_true = data["antenna_pos"]

    print(">>> Solving CP-ALS decomposition...")
    cp = CP(T_true, config.num_sources).compute(
        n_iter_max=2000,
        tol=1e-9,
        random_state=config.seed,
    )
    print(f"  Relative Tensor Reconstruction Error: {cp.rec_error:.6e}")

    print(">>> Aligning recovered factors with ground-truth channel...")
    align_factors(cp, data["A_true"])

    title = None
    plot_antenna_and_radii(
        user_pos=user_pos,
        antenna_pos_true=antenna_pos_true,
        A_est=cp.A,
        S_est=cp.S,
        title=title,
        save_path=str(output_path),
        show=False,
        area_side=config.area_side,
    )

    print("\n" + "=" * 70)
    print(f"SUCCESS: Plot generated and saved to '{output_path}'")
    print("=" * 70)


def run_multi_plot_cli(
    config_arg: Optional[Union[str, Path, list]] = None, num_plots: int = 6
) -> None:
    """
    CLI runner logic for 6-subfigure (3x2 grid) DS-CDMA experiment plotting.
    Generates 6 independent runs in 3 rows of 2 with equal area boxes in a single A4-friendly PDF figure.
    """
    config_path = resolve_config_path(config_arg)
    config = SimConfig.from_toml(config_path)

    output_path = Path("dscdma_6_experiments.pdf")

    print_sim_banner(
        f"DS-CDMA Multi-Subfigure Experiment Generator ({num_plots} Runs)",
        config,
        {
            "Output PDF": str(output_path),
            "Number of Subfigures": num_plots,
        },
    )

    fig, _ = plot_antenna_localization_multi(
        config=config,
        num_runs=num_plots,
        save_path=str(output_path),
        show=False,
    )

    print("\n" + "=" * 70)
    print(f"SUCCESS: {num_plots} subfigures generated and saved to '{output_path.resolve()}'")
    print("=" * 70)


def run_noise_experiment_cli(
    config_arg: Optional[Union[str, Path, list]] = None,
) -> None:
    """
    CLI runner logic for single-run DS-CDMA Gaussian noise degradation experiment.
    Generates a single overlaid trajectory plot.
    """
    config_path = resolve_config_path(config_arg)
    config = SimConfig.from_toml(config_path)

    output_path = Path("dscdma_noise_experiment.pdf")

    print_sim_banner(
        "DS-CDMA Gaussian Noise Experiment Generator (Single Run Trajectory)",
        config,
        {
            "Output PDF": str(output_path),
            "Noise Levels": "6 steps (0.0 to 0.25 * RMS)",
        },
    )

    out_file = generate_dscdma_noise_experiment_pdf(
        config=config,
        noise_stds=None,
        output_path=str(output_path),
    )

    print("\n" + "=" * 70)
    print(f"SUCCESS: Single noise experiment PDF generated and saved to '{out_file.resolve()}'")
    print("=" * 70)


def run_noise_multi_experiment_cli(
    config_arg: Optional[Union[str, Path, list]] = None, num_plots: int = 6
) -> None:
    """
    CLI runner logic for 6-subfigure (3x2 grid) DS-CDMA Gaussian noise degradation experiment.
    Generates 6 independent noise trajectory runs in a single A4-friendly PDF figure.
    """
    config_path = resolve_config_path(config_arg)
    config = SimConfig.from_toml(config_path)

    output_path = Path("dscdma_noise_experiment_multi.pdf")

    print_sim_banner(
        f"DS-CDMA Gaussian Noise Multi-Subfigure Experiment Generator ({num_plots} Runs)",
        config,
        {
            "Output PDF": str(output_path),
            "Number of Subfigures": num_plots,
            "Noise Levels per Subfigure": "6 steps (0.0 to 0.25 * RMS)",
        },
    )

    out_file = generate_dscdma_noise_multi_experiment_pdf(
        config=config,
        num_runs=num_plots,
        noise_stds=None,
        output_path=str(output_path),
    )

    print("\n" + "=" * 70)
    print(f"SUCCESS: Multi noise experiment PDF generated and saved to '{out_file.resolve()}'")
    print("=" * 70)


def run_all_plots_cli(
    config_arg: Optional[Union[str, Path, list]] = None,
    output_dir: Optional[Union[str, Path]] = None,
    presentation: bool = False,
) -> None:
    """
    CLI runner logic to generate all 4 DS-CDMA experiment plots at once:
      1. antenna_localization_plot.pdf
      2. dscdma_6_experiments.pdf
      3. dscdma_noise_experiment.pdf
      4. dscdma_noise_experiment_multi.pdf
    """
    config_path = resolve_config_path(config_arg)
    config = SimConfig.from_toml(config_path)

    import numpy as np

    if output_dir is None:
        thesis_root = Path(__file__).resolve().parents[4]
        if presentation:
            out_dir = thesis_root / "slides" / "figures"
        else:
            out_dir = thesis_root / "Sources" / "Chapter4" / "figures"
        if not thesis_root.exists():
            out_dir = Path.cwd() / "slides" / "figures" if presentation else Path.cwd()
    else:
        out_dir = Path(output_dir)

    out_dir.mkdir(parents=True, exist_ok=True)

    mode_str = "PRESENTATION (4:3, Sans-Serif)" if presentation else "PAPER (A4 / LaTeX)"
    print("=" * 70)
    print(f"DS-CDMA GENERATING ALL 4 EXPERIMENT PLOTS AT ONCE [{mode_str}]")
    print("=" * 70)
    print(f"Target Directory: {out_dir.resolve()}")
    print("-" * 70)

    # Generate single dataset instance once so plot 1 and plot 3 share the exact same antennas and users (even when unseeded/random)
    generator = DSCDMADatasetGenerator(config)
    single_data = generator.generate()

    # Determine seeds once for multi-plot runs so plot 2 and plot 4 share the exact same subfigure runs
    if config.seed is None:
        rng_seeds = np.random.default_rng()
        multi_seeds = [int(s) for s in rng_seeds.integers(1, 1_000_000, size=6)]
    else:
        multi_seeds = [config.seed + 10 * i for i in range(6)]

    # 1. Single antenna localization plot (zero noise baseline of noise_experiment)
    print("1/4 Generating antenna_localization_plot.pdf ...")
    generate_dscdma_noise_experiment_pdf(
        config=config,
        noise_stds=[0.0],
        output_path=str(out_dir / "antenna_localization_plot.pdf"),
        presentation=presentation,
        data=single_data,
    )

    # 2. 6-experiment multi plot (zero noise baseline of multi noise experiment)
    print("2/4 Generating dscdma_6_experiments.pdf ...")
    generate_dscdma_noise_multi_experiment_pdf(
        config=config,
        num_runs=6,
        noise_stds=[0.0],
        output_path=str(out_dir / "dscdma_6_experiments.pdf"),
        presentation=presentation,
        seeds=multi_seeds,
    )

    # 3. Single noise experiment plot (reusing single_data)
    print("3/4 Generating dscdma_noise_experiment.pdf ...")
    generate_dscdma_noise_experiment_pdf(
        config=config,
        output_path=str(out_dir / "dscdma_noise_experiment.pdf"),
        presentation=presentation,
        data=single_data,
    )

    # 4. Multi noise experiment plot (reusing multi_seeds)
    print("4/4 Generating dscdma_noise_experiment_multi.pdf ...")
    generate_dscdma_noise_multi_experiment_pdf(
        config=config,
        num_runs=6,
        output_path=str(out_dir / "dscdma_noise_experiment_multi.pdf"),
        presentation=presentation,
        seeds=multi_seeds,
    )

    print("\n" + "=" * 70)
    print(f"SUCCESS: All 4 {mode_str} plots successfully generated in:")
    print(f"  {out_dir.resolve()}")
    print("=" * 70)


def run_all_plots_pres_cli(
    config_arg: Optional[Union[str, Path, list]] = None,
    output_dir: Optional[Union[str, Path]] = None,
) -> None:
    """
    CLI runner logic to generate presentation-friendly (16:9 aspect ratio, sans-serif fonts, Typst/slide ready) versions of all 4 DS-CDMA plots.
    """
    run_all_plots_cli(config_arg=config_arg, output_dir=output_dir, presentation=True)





