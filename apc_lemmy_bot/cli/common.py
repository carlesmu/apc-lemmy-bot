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
from typing import Optional, Union
from typing_extensions import Annotated

from .callbacks import callback_date, callback_url, callback_silence, callback_version

# val_date: date = datetime.datetime.today().strftime("%Y-%m-%d")
val_date: str = datetime.datetime.today().strftime("%Y-%m-%d")
arg_date = Annotated[
    str,
    typer.Argument(
        help="The date to look for ephemerides [Format: YYYY-MM-DD].",
        callback=callback_date,
        show_default=True,
    ),
]


val_supabase_url: str = "https://stahmaxffcqankienulh.supabase.co"
opt_supabase_url = Annotated[
    str,
    typer.Option(
        "--sb-url",
        "-u",
        rich_help_panel="Supabase options",
        help="Url of the supabase database.",
        callback=callback_url,
        show_default=True,
        envvar="APC_SUPABASE_URL",
        # prompt="Please we need the URL for the supabase database",
    ),
]

val_supabase_key: str = ""  # not initialized
opt_supabase_key = Annotated[
    str,
    typer.Option(
        "--sb-key",
        "-k",
        rich_help_panel="Supabase options",
        help="Key used to access to the database.",
        show_default=False,
        envvar="APC_SUPABASE_KEY",
        # prompt="Please we need the KEY for the supabase database",
    ),
]

val_base_event_url: str = "https://www.apeoplescalendar.org/calendar/events/"
opt_base_event_url = Annotated[
    str,
    typer.Option(
        "--ev-url",
        rich_help_panel="Supabase options",
        help="Base URL where where the events are shown.",
        callback=callback_url,
        show_default=True,
        envvar="APC_BASE_EVENT_URL",
    ),
]

val_base_event_img_url: str = (
    "https://stahmaxffcqankienulh.supabase.co/storage/v1/object/public/event-photos/"
)
opt_base_event_img_url = Annotated[
    str,
    typer.Option(
        "--ev-img-url",
        rich_help_panel="Supabase options",
        help="Base URL where the images of the events are shown.",
        callback=callback_url,
        show_default=True,
        envvar="APC_BASE_EVENT_IMG_URL",
    ),
]

val_silence: bool = False
opt_silence = Annotated[
    bool,
    typer.Option(
        "--silence",
        "-s",
        help="Don't print extra information.",
        callback=callback_silence,
        is_eager=True,
    ),
]

val_version: bool = False
opt_version = Annotated[
    bool,
    typer.Option(
        "--version",
        help="Show program version and exit.",
        callback=callback_version,
        is_eager=True,
    ),
]
