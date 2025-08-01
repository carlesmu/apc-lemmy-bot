#!/usr/bin/env python3
"""
scripts/build.py utility.

See: https://github.com/python-poetry/poetry/issues/5539
"""

import shutil
from pathlib import Path
from typing import Any

POETRY_EXE = ".venv/bin/poetry"
if not Path(POETRY_EXE).is_file():
    POETRY_EXE = ".venv/Scripts/poetry.exe"


def make_clean(setup_kwargs: dict[Any, Any]) -> dict[Any, Any]:
    """Cleanup."""
    print("- Cleaning environment: ")
    for directory in [
        ".mypy_cache",
        ".ruff_cache",
        "apc_lemmy_bot/__pycache__",
        "apc_lemmy_bot/cli/__pycache__",
        "build",
        "dist",
        "docs/build",
    ]:
        print(f"  - deleting '{directory}'", end=" ... ")
        if Path(directory).exists():
            shutil.rmtree(directory)
            print("Done.")
        else:
            print("Not found.")
    return setup_kwargs


if __name__ == "__main__":
    make_clean({})
