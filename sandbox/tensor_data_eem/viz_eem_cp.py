#!/usr/bin/env python3
"""
Thin wrapper for EEM CP model visualization, importing from src package.
"""

import sys
from pathlib import Path

# Add src folder to python path
script_dir = Path(__file__).parent
sys.path.append(str(script_dir / "src"))

from plots.viz_eem_cp import visualize_eem_cp

if __name__ == '__main__':
    mat_path = script_dir / "EEM18.mat"
    
    # Save directly to Chapter4/figures for LaTeX inclusion
    output_dir = script_dir.parent.parent / "Sources" / "Chapter4" / "figures"
    output_pdf = output_dir / "eem_model.pdf"
    output_png = output_dir / "eem_model.png"
    
    visualize_eem_cp(
        mat_path=mat_path,
        output_pdf=output_pdf,
        output_png=output_png
    )
