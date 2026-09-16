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


def compile_tikz_file(
    tikz_path: Path,
    preamble_path: Path,
    out_dir: Optional[Path],
    engine: str = "pdflatex",
    presentation: bool = False,
) -> Tuple[Path, bool, str]:
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

    # Build document string
    border_str = "0pt" if presentation else "2pt"
    tex = (
        f"\\documentclass[tikz,border={border_str}]{{standalone}}\n"
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

        # Destination determination
        if out_dir is not None:
            out_dir.mkdir(parents=True, exist_ok=True)
            dest = out_dir / f"{tikz_path.stem}.pdf"
        else:
            dest = tikz_path.with_suffix(".pdf")

        try:
            shutil.copyfile(pdf_src, dest)
        except Exception as e:
            return tikz_path, False, f"Failed to copy PDF to destination {dest}: {e}\n" + "\n".join(logs)

        return dest, True, "\n".join(logs)


def main(argv: Optional[list[str]] = None) -> int:
    p = argparse.ArgumentParser(description="Compile .tikz files recursively or by target figure name/path using a tikz preamble")
    p.add_argument("target", nargs="?", default=".", help="Target figure name, file path to .tikz file, or directory (default: current directory)")
    p.add_argument("--preamble", "-p", default="tikz_preamble.tex", help="Path to tikz preamble tex file (default: tikz_preamble.tex in CWD)")
    p.add_argument("--engine", "-e", choices=["pdflatex", "xelatex", "lualatex"], default="pdflatex", help="TeX engine to use (default: pdflatex)")
    p.add_argument("--jobs", "-j", type=int, default=4, help="Number of parallel jobs (default: 4)")
    p.add_argument("--presentation", "--slides", action="store_true", help="Compile in 4:3 presentation slide format and output to slides/figures/")
    p.add_argument("--format", "-f", choices=["standalone", "presentation"], default=None, help="Output format (default: presentation if --presentation/--slides is set, otherwise standalone)")
    p.add_argument("--out-dir", "-o", type=Path, default=None, help="Output directory for compiled PDFs")
    args = p.parse_args(argv)

    repo_root = Path(__file__).parent.resolve()
    target_str = args.target
    target_path = Path(target_str)

    preamble = Path(args.preamble)
    if not preamble.is_absolute():
        preamble = repo_root / preamble

    if not preamble.exists():
        print(f"Preamble file not found: {preamble}")
        print("Create a tikz_preamble.tex file or pass its path via --preamble.")
        return 3

    is_presentation = args.presentation or (args.format == "presentation")

    if args.out_dir is not None:
        out_dir = args.out_dir
    elif is_presentation:
        out_dir = repo_root / "slides" / "figures"
    else:
        out_dir = None

    tikz_files: list[Path] = []

    if target_path.is_file():
        tikz_files = [target_path]
    elif target_path.is_dir():
        tikz_files = find_tikz_files(target_path)
    else:
        # Search for matching .tikz file by stem or filename across repo
        all_tikz = find_tikz_files(repo_root)
        stem_target = target_str.removesuffix(".tikz")
        matches = [
            f for f in all_tikz
            if f.stem == stem_target or f.name == target_str or str(f).endswith(target_str)
        ]
        if matches:
            tikz_files = matches
        else:
            print(f"Error: Target '{target_str}' does not exist as a file/directory and no matching .tikz files were found under {repo_root}")
            return 2

    if not tikz_files:
        print(f"No .tikz files found for target: {target_str}")
        return 0

    mode_desc = "presentation (4:3 ratio)" if is_presentation else "standalone"
    out_desc = str(out_dir) if out_dir else "alongside .tikz files"
    print(f"Found {len(tikz_files)} .tikz file(s). Format: {mode_desc}. Output dir: {out_desc}. Preamble: {preamble}")

    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as ex:
        futures = {
            ex.submit(compile_tikz_file, tf, preamble, out_dir, args.engine, is_presentation): tf
            for tf in tikz_files
        }
        for fut in concurrent.futures.as_completed(futures):
            tikz_path = futures[fut]
            try:
                dest_path, ok, log = fut.result()
            except Exception as e:
                print(f"{tikz_path}: exception during compilation: {e}")
                results.append((tikz_path, False, str(e)))
                continue
            if ok:
                print(f"OK: {dest_path}")
            else:
                print(f"FAILED: {tikz_path}\nLog:\n{log}")
            results.append((tikz_path, ok, log))

    failed = [r for r in results if not r[1]]
    print(f"\nSummary: {len(results)-len(failed)} succeeded, {len(failed)} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())

