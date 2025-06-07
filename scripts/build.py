#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/build.py utility.

See: https://github.com/python-poetry/poetry/issues/5539
"""

import subprocess
import os

from typing import Any

POETRY_EXE = ".venv/bin/poetry"
if not os.path.isfile(POETRY_EXE):
    POETRY_EXE = ".venv/bin/poetry.exe"


def make_cx_Freeze_build(setup_kwargs: dict[Any, Any]) -> dict[Any, Any]:
    """Build a cx_Freeze executable."""
    print("- Creating cx_Freeze build")
    foo = subprocess.run([POETRY_EXE, "run", "python", "setup.py", "build"])
    print(f"  - {foo}")
    return setup_kwargs


if __name__ == "__main__":
    make_cx_Freeze_build({})
