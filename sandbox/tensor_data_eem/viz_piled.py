#!/usr/bin/env python3
"""
Thin wrapper for EEM piled tensor visualization, importing from src package.
"""

import sys
from pathlib import Path

# Add src folder to python path
script_dir = Path(__file__).parent
sys.path.append(str(script_dir / "src"))

from plots.viz_piled import visualize_eem_piled

if __name__ == '__main__':
    mat_path = script_dir / "EEM18.mat"
    
    # 1. Save to Chapter 4 figures directory for LaTeX inclusion
    chapter_figures_dir = script_dir.parent.parent / "Sources" / "Chapter4" / "figures"
    output_pdf_chapter = chapter_figures_dir / "piled_tensor.pdf"
    output_png_chapter = chapter_figures_dir / "piled_tensor.png"
    
    visualize_eem_piled(
        mat_path=mat_path,
        output_pdf=output_pdf_chapter,
        output_png=output_png_chapter,
        step=14
    )
    
    # 2. Also save to the local sandbox directory
    output_pdf_local = script_dir / "piled_tensor.pdf"
    output_png_local = script_dir / "piled_tensor.png"
    
    visualize_eem_piled(
        mat_path=mat_path,
        output_pdf=output_pdf_local,
        output_png=output_png_local,
        step=14
    )
