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

"""apc_lemmy_bot.cli common module."""

import datetime
import typer
from typing_extensions import Annotated

from apc_lemmy_bot import apc_lb_conf
from . import callbacks

val_date: str = datetime.datetime.today().strftime("%Y-%m-%d")
arg_date = Annotated[
    str,
    typer.Argument(
        help="The date to look for ephemerides [Format: YYYY-MM-DD].",
        callback=callbacks.date,
        show_default=True,
    ),
]


val_supabase_url: str = apc_lb_conf.supabase.url
opt_supabase_url = Annotated[
    str,
    typer.Option(
        "--sb-url",
        "-u",
        rich_help_panel="Supabase options",
        help="Url of the supabase database.",
        callback=callbacks.url,
        show_default=True,
        envvar="APC_SUPABASE_URL",
        # prompt="Please we need the URL for the supabase database",
    ),
]

val_supabase_key: str = apc_lb_conf.supabase.key
opt_supabase_key = Annotated[
    str,
    typer.Option(
        "--sb-key",
        "-k",
        rich_help_panel="Supabase options",
        help="Key used to access to the database.",
        callback=callbacks.supabase_key,
        show_default=False,
        envvar="APC_SUPABASE_KEY",
        # prompt="Please we need the KEY for the supabase database",
    ),
]

val_base_event_url: str = apc_lb_conf.supabase.base_event_url
opt_base_event_url = Annotated[
    str,
    typer.Option(
        "--ev-url",
        rich_help_panel="Supabase options",
        help="Base URL where where the events are shown.",
        callback=callbacks.url,
        show_default=True,
        envvar="APC_BASE_EVENT_URL",
    ),
]

val_base_event_img_url: str = apc_lb_conf.supabase.base_event_img_url
opt_base_event_img_url = Annotated[
    str,
    typer.Option(
        "--ev-img-url",
        rich_help_panel="Supabase options",
        help="Base URL where the images of the events are shown.",
        callback=callbacks.url,
        show_default=True,
        envvar="APC_BASE_EVENT_IMG_URL",
    ),
]

opt_langcode = Annotated[
    str,
    typer.Option(
        "--langcode",
        help="The language code of the event in ISO 639 format",
        callback=callbacks.langcode,
        show_default=True,
        envvar="APC_LANGCODE",
    ),
]

val_silence: bool = False
opt_silence = Annotated[
    bool,
    typer.Option(
        "--silence",
        "-s",
        help="Don't print extra information.",
        callback=callbacks.silence,
        is_eager=True,
    ),
]

val_version: bool = False
opt_version = Annotated[
    bool,
    typer.Option(
        "--version",
        help="Show program version and exit.",
        callback=callbacks.version,
        is_eager=True,
    ),
]
