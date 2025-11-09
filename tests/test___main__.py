#  This file is part of apc-lemmy-bot.
#
#  Copyright 2025 Carles Muñoz Gorriz <carlesmu@internautas.org>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.

"""Test cases for __main__ module."""

import sys

import pytest

from apc_lemmy_bot import __main__


def test_args_ok() -> None:
    """Test ok args."""
    # Remove pytest options:
    orig_args = sys.argv[:]

    # Parse command line (it should work):
    for gr_op in (
        ("--help",),
        ("-h",),
        ("--version",),
        ("db", "--help"),
        ("post", "--help"),
        ("show", "--help"),
    ):
        del sys.argv[1:]
        for op in gr_op:
            sys.argv.append(op)
        with pytest.raises(SystemExit, match="0") as ex_info:
            __main__.main()
        assert ex_info.value.code == 0

    # Restore pytest args
    sys.argv = orig_args


def test_args_wrong() -> None:
    """Test wrong args."""
    # Remove pytest options:
    orig_args = sys.argv[:]

    # Parse command line (it should work):
    for gr_op in (
        ("--foo",),
        ("db",),
        ("post",),
        ("show",),
    ):
        del sys.argv[1:]
        for op in gr_op:
            sys.argv.append(op)
        with pytest.raises(SystemExit, match="2") as ex_info:
            __main__.main()
        assert ex_info.value.code == 2  # noqa: PLR2004

    # Restore pytest args
    sys.argv = orig_args
