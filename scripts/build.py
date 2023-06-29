#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""scripts/build.py utility.

See: https://github.com/python-poetry/poetry/issues/5539
"""
import subprocess
import shutil
import os

POETRY_EXE = ".venv/bin/poetry"
if not os.path.isfile(POETRY_EXE):
    POETRY_EXE = ".venv/Scripts/poetry.exe"


def make_clean(setup_kwargs):
    """Cleanup."""
    print("- Cleaning environment: ")
    for d in ["build", "dist"]:
        try:
            print(f"  - deleting {d}.")
        except FileNotFoundError:
            print(f"  - {d} not found.")
    return setup_kwargs


def make_cx_Freeze_build(setup_kwargs):
    """Build a cx_Freeze executable."""
    print("- Creating cx_Freeze build")
    foo = subprocess.run([POETRY_EXE, "run", "python", "setup.py", "build"])
    print(f"  - {foo}")
    return setup_kwargs


if __name__ == "__main__":
    make_clean({})
    make_cx_Freeze_build({})
