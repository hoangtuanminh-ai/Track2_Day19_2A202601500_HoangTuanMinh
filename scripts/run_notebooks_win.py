# -*- coding: utf-8 -*-
"""
Script to run and verify all notebooks on Windows (equivalent to `make notebooks`).
Converts Jupytext (.py) files to Jupyter Notebook (.ipynb), executes them, and saves the output.
"""

import os
import glob
import sys
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
notebooks_dir = ROOT / "notebooks"

# Locate the Scripts directory of the virtual environment on Windows
venv_bin = ROOT / ".venv" / "Scripts"
if not venv_bin.exists():
    venv_bin = ROOT / ".venv" / "bin"

def run_command(cmd, env=None):
    """Run command and return return code, stdout, and stderr."""
    res = subprocess.run(cmd, env=env, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return res.returncode, res.stdout, res.stderr

def main():
    print("=" * 60)
    print(" AUTOMATED NOTEBOOK RUNNER FOR WINDOWS")
    print("=" * 60)

    # 1. Convert Jupytext (.py) to Notebook (.ipynb)
    print("\n[Step 1] Converting Jupytext py files to ipynb...")
    jupytext_path = venv_bin / "jupytext.exe"
    if not jupytext_path.exists():
        jupytext_path = venv_bin / "jupytext"
    if not jupytext_path.exists():
        jupytext_path = Path("jupytext")  # fallback to system PATH

    py_files = sorted(glob.glob(str(notebooks_dir / "[0-9]*.py")))
    if not py_files:
        print("Error: No py source files found in notebooks/")
        return 1

    for py_file in py_files:
        py_name = Path(py_file).name
        print(f"  * Converting: {py_name} -> .ipynb")
        # Run jupytext --to notebook --update
        cmd = [str(jupytext_path), "--to", "notebook", "--update", py_file]
        code, out, err = run_command(cmd)
        if code != 0:
            # Fallback without --update if older version
            cmd = [str(jupytext_path), "--to", "notebook", py_file]
            code, out, err = run_command(cmd)
            if code != 0:
                print(f"    [Warning] Error converting {py_name}: {err.strip()}")

    # 2. Execute all notebooks
    print("\n[Step 2] Executing all notebooks (simulating grader)...")
    ipynb_files = sorted(glob.glob(str(notebooks_dir / "[0-9]*.ipynb")))
    if not ipynb_files:
        print("Error: No ipynb files found to run!")
        return 1

    # Prepare environment PATH for Feast CLI and other tools in venv
    env = os.environ.copy()
    env["PATH"] = f"{venv_bin}{os.pathsep}{env.get('PATH', '')}"

    jupyter_path = venv_bin / "jupyter.exe"
    if not jupyter_path.exists():
        jupyter_path = venv_bin / "jupyter"
    if not jupyter_path.exists():
        jupyter_path = Path("jupyter")

    success_count = 0
    total_count = len(ipynb_files)

    for nb in ipynb_files:
        nb_name = Path(nb).name
        print(f"  * {nb_name:<45} ... ", end="", flush=True)
        
        cmd = [
            str(jupyter_path), "nbconvert", "--to", "notebook",
            "--execute", "--inplace", nb,
            "--ExecutePreprocessor.timeout=900"
        ]
        
        code, out, err = run_command(cmd, env=env)
        if code == 0:
            print("PASS")
            success_count += 1
        else:
            print("FAIL")
            print("-" * 60)
            print("ERROR DETAILS:")
            print(err.strip() if err.strip() else out.strip())
            print("-" * 60)

    print("\n" + "=" * 60)
    print(f" RESULTS: Successfully executed {success_count}/{total_count} notebooks.")
    print("=" * 60)
    
    if success_count == total_count:
        return 0
    else:
        return 1

if __name__ == "__main__":
    sys.exit(main())
