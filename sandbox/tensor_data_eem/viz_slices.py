#!/usr/bin/env python3
"""
Wrapper for EEM Slices visualization (textbook style, 18 compressed rows).
Generates PDF and PNG figures in both sandbox and thesis figures directory.
"""

import sys
import shutil
from pathlib import Path

# Add src folder to python path
script_dir = Path(__file__).parent
sys.path.append(str(script_dir / "src"))

from plots.viz_slices import visualize_eem_slices

if __name__ == '__main__':
    mat_path = script_dir / "EEM18.mat"
    output_pdf = script_dir / "X-slices.pdf"
    output_png = script_dir / "X-slices.png"
    
    # Generate 18 compressed rows matching eem slices.png figure exactly
    visualize_eem_slices(
        mat_path=mat_path,
        output_pdf=output_pdf,
        output_png=output_png,
        var_name="X",
        n_rows=18
    )

    # Copy generated PDF/PNG to thesis figures directory
    thesis_fig_dir = script_dir.parent.parent / "Sources" / "Chapter4" / "figures"
    if thesis_fig_dir.exists():
        shutil.copy(output_pdf, thesis_fig_dir / "X-slices.pdf")
        shutil.copy(output_png, thesis_fig_dir / "X-slices.png")
        print(f"Copied figure to thesis directory: {thesis_fig_dir / 'X-slices.pdf'}")
