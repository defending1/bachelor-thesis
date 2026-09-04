#!/usr/bin/env python3
"""
Wrapper for EEM Slices visualization.
"""

from pathlib import Path
from experiments.tensor_data_eem.plots.viz_slices import visualize_eem_slices

script_dir = Path(__file__).parent

if __name__ == '__main__':
    mat_path = script_dir / "EEM18.mat"
    output_dir = script_dir.parent.parent.parent / "Sources" / "Chapter4" / "figures"
    output_pdf = output_dir / "X-slices.pdf"
    output_png = output_dir / "X-slices.png"

    visualize_eem_slices(
        mat_path=mat_path,
        output_pdf=output_pdf,
        output_png=output_png
    )
