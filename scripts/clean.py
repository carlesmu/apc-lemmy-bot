#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/build.py utility.

See: https://github.com/python-poetry/poetry/issues/5539
"""

import shutil
import os

POETRY_EXE = ".venv/bin/poetry"
if not os.path.isfile(POETRY_EXE):
    POETRY_EXE = ".venv/Scripts/poetry.exe"


def make_clean(setup_kwargs):
    """Cleanup."""
    print("- Cleaning environment: ")
    for directory in [
        "build",
        ".mypy_cache",
        "apc_lemmy_bot/__pycache__",
        "apc_lemmy_bot/cli/__pycache__",
    ]:
        try:
            print(f"  - deleting '{directory}'", end=" ... ")
            shutil.rmtree(directory)
            print("Done.")
        except FileNotFoundError:
            print("Not found.")
    return setup_kwargs


if __name__ == "__main__":
    make_clean({})
