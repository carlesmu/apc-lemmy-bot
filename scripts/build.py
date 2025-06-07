#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/build.py utility.

See: https://github.com/python-poetry/poetry/issues/5539
"""

import subprocess
from pathlib import Path
from typing import Any

POETRY_EXE = ".venv/bin/poetry"
if not Path(POETRY_EXE).is_file():
    POETRY_EXE = ".venv/bin/poetry.exe"


def make_cx_freeze_build(setup_kwargs: dict[Any, Any]) -> dict[Any, Any]:
    """Build a cx_Freeze executable."""
    print("- Creating cx_Freeze build")
    foo = subprocess.run([POETRY_EXE, "run", "python", "setup.py", "build"])
    print(f"  - {foo}")
    return setup_kwargs


if __name__ == "__main__":
    make_cx_freeze_build({})
