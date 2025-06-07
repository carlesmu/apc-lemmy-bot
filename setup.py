#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
`Setup.py` file used to build with cx_Freeze.

It's executed with `.venv/bin/poetry build`
See: https://cx-freeze.readthedocs.io/en/latest/setup_script.html
"""

import sys
from cx_Freeze import setup, Executable

sys.setrecursionlimit(2000)  # make cz_freeze don't fail with recursion limit

# Dependencies are automatically detected, but it might need
# fine tuning.
build_options: dict[str, list[str]] = {"packages": [], "excludes": []}

base: str = "console"

setup(
    executables=[
        Executable(
            "apc_lemmy_bot/__main__.py",
            base=base,
            target_name="apc-lemmy-bot",
        )
    ]
)
