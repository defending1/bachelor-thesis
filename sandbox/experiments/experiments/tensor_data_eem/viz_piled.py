#!/usr/bin/env python3
"""
Wrapper for EEM Piled tensor visualization.
"""

from pathlib import Path
from experiments.tensor_data_eem.plots.viz_piled import visualize_eem_piled

script_dir = Path(__file__).parent

if __name__ == '__main__':
    mat_path = script_dir / "EEM18.mat"
    output_dir = script_dir.parent.parent.parent / "Sources" / "Chapter4" / "figures"
    output_pdf = output_dir / "piled_tensor.pdf"
    output_png = output_dir / "piled_tensor.png"

    visualize_eem_piled(
        mat_path=mat_path,
        output_pdf=output_pdf,
        output_png=output_png
    )
