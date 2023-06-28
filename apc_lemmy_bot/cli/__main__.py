#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#    Copyright (C) 2023  Carles Muñoz Gorriz <carlesmu@internautas.org>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""apc_lemmy_bot.cli __main__ module."""

import typer
from typing_extensions import Annotated

from . import app, post, show
from .callbacks import callback_version


@app.callback()
def main(
    ctx: typer.Context,
    version: Annotated[
        bool,
        typer.Option(
            "--version",
            help="Show program version and exit.",
            callback=callback_version,
            is_eager=True,
        ),
    ] = False,
):
    """
    Post supabase events to a Lemmy instance or show them.

    You can show additional command help information running, by exemple,
    'apc_lemmy_bot post --help'
    """


def run():
    """Run apc_lemmy_bot CLI."""
    app()
