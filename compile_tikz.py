#!/usr/bin/env python3
"""
Recursively find .tikz files and compile them to PDF using a provided tikz_preamble.tex.

Usage examples:
  python compile_tikz.py                # looks for tikz_preamble.tex in CWD, writes PDFs next to .tikz files
  python compile_tikz.py --preamble my_preamble.tex --out-dir out

The script creates a temporary build directory per file, writes a minimal standalone
LaTeX document that includes the preamble and the contents of the .tikz file, runs
pdflatex (twice) and copies the resulting PDF to the destination.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Optional, Tuple


def find_tikz_files(root: Path) -> list[Path]:
    return sorted(root.rglob("*.tikz"))


def compile_tikz_file(tikz_path: Path, preamble_path: Path, out_dir: Optional[Path], engine: str = "pdflatex") -> Tuple[Path, bool, str]:
    """Compile a single .tikz file. Returns (tikz_path, success, log).

    The PDF is written either next to the .tikz file or under out_dir preserving filename.
    """
    tikz_path = tikz_path.resolve()
    preamble_path = preamble_path.resolve()

    try:
        tikz_text = tikz_path.read_text()
    except Exception as e:
        return tikz_path, False, f"Failed to read .tikz file: {e}"

    try:
        preamble_text = preamble_path.read_text()
    except Exception as e:
        return tikz_path, False, f"Failed to read preamble ({preamble_path}): {e}"

    # Build a standalone document
    tex = (
        "\\documentclass[tikz,border=2pt]{standalone}\n"
        f"% Preamble from: {preamble_path}\n"
        f"{preamble_text}\n"
        "\\begin{document}\n"
        f"{tikz_text}\n"
        "\\end{document}\n"
    )

    with tempfile.TemporaryDirectory(prefix="compile_tikz_") as td:
        td_path = Path(td)
        tex_file = td_path / "main.tex"
        tex_file.write_text(tex)

        # Copy local .sty files from the repository root (where this script lives)
        # and from the .tikz file directory into the build dir so \input and \usepackage
        # that reference local style files will work.
        try:
            repo_root = Path(__file__).parent.resolve()
            for sty in repo_root.glob("*.sty"):
                shutil.copy(sty, td_path / sty.name)
        except Exception:
            # Ignore copy errors; compilation will fail later if files are required
            pass

        try:
            for sty in tikz_path.parent.glob("*.sty"):
                shutil.copy(sty, td_path / sty.name)
        except Exception:
            pass

        # Run the chosen TeX engine (two passes)
        cmd = [engine, "-interaction=nonstopmode", "-halt-on-error", "main.tex"]
        logs = []
        success = True
        for i in range(2):
            proc = subprocess.run(cmd, cwd=td, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            out = proc.stdout.decode(errors="ignore")
            logs.append(f"--- {engine} pass {i+1} ---\n{out}\n")
            if proc.returncode != 0:
                success = False
                break

        if not success:
            return tikz_path, False, "\n".join(logs)

        pdf_src = td_path / "main.pdf"
        if not pdf_src.exists():
            return tikz_path, False, f"{engine} finished but main.pdf not found\n" + "\n".join(logs)

        # Destination must be the same directory as the .tikz file
        dest = tikz_path.with_suffix(".pdf")

        try:
            shutil.copyfile(pdf_src, dest)
        except Exception as e:
            return tikz_path, False, f"Failed to copy PDF to destination {dest}: {e}\n" + "\n".join(logs)

        return tikz_path, True, "\n".join(logs)


def main(argv: Optional[list[str]] = None) -> int:
    p = argparse.ArgumentParser(description="Compile .tikz files recursively using a tikz preamble")
    p.add_argument("root", nargs="?", default='.', help="Root directory to search (default: current directory)")
    p.add_argument("--preamble", "-p", default="tikz_preamble.tex", help="Path to tikz preamble tex file (default: tikz_preamble.tex in CWD)")
    p.add_argument("--engine", "-e", choices=["pdflatex", "xelatex", "lualatex"], default="pdflatex", help="TeX engine to use (default: pdflatex)")
    p.add_argument("--jobs", "-j", type=int, default=4, help="Number of parallel jobs (default: 4)")
    args = p.parse_args(argv)

    root = Path(args.root)
    preamble = Path(args.preamble)
    out_dir = None

    if not root.exists():
        print(f"Root directory does not exist: {root}")
        return 2

    if not preamble.exists():
        print(f"Preamble file not found: {preamble}")
        print("Create a tikz_preamble.tex file or pass its path via --preamble.")
        return 3

    tikz_files = find_tikz_files(root)
    if not tikz_files:
        print(f"No .tikz files found under {root}")
        return 0

    print(f"Found {len(tikz_files)} .tikz files. Compiling with preamble: {preamble}")

    results = []
    engine = args.engine
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as ex:
        futures = {ex.submit(compile_tikz_file, tf, preamble, None, args.engine): tf for tf in tikz_files}
        for fut in concurrent.futures.as_completed(futures):
            tikz_path = futures[fut]
            try:
                path, ok, log = fut.result()
            except Exception as e:
                print(f"{tikz_path}: exception during compilation: {e}")
                results.append((tikz_path, False, str(e)))
                continue
            if ok:
                print(f"OK: {path}")
            else:
                print(f"FAILED: {path}\nLog:\n{log}")
            results.append((path, ok, log))

    failed = [r for r in results if not r[1]]
    print(f"\nSummary: {len(results)-len(failed)} succeeded, {len(failed)} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
