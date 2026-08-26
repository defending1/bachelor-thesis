#!/usr/bin/env python3
"""
Thin wrapper for EEM Slices visualization, importing from src package.
"""

import sys
from pathlib import Path

# Add src folder to python path
script_dir = Path(__file__).parent
sys.path.append(str(script_dir / "src"))

from plots.viz_slices import visualize_eem_slices

if __name__ == '__main__':
    mat_path = script_dir / "EEM18.mat"
    output_pdf = script_dir / "X-slices.pdf"
    output_png = script_dir / "X-slices.png"
    
    visualize_eem_slices(
        mat_path=mat_path,
        output_pdf=output_pdf,
        output_png=output_png,
        var_name="X"
    )
