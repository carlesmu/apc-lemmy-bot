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
import os
from typing import Annotated

import typer

from apc_lemmy_bot import apc_lb_conf

from . import callbacks

val_date: str = (
    datetime.datetime.now(tz=datetime.UTC)
    .astimezone(None)
    .strftime("%Y-%m-%d")
)
arg_date = Annotated[
    str,
    typer.Argument(
        help="The date to look for ephemerides [Format: YYYY-MM-DD].",
        callback=callbacks.date,
        show_default=True,
    ),
]

_val_supabase_url: str | None = (
    os.environ.get("APC_SUPABASE_URL")
    if os.environ.get("APC_SUPABASE_URL") is not None
    else apc_lb_conf.supabase.url
)
val_supabase_url: str = (
    _val_supabase_url if _val_supabase_url is not None else ""
)
del _val_supabase_url
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

_val_supabase_key: str | None = (
    os.environ.get("APC_SUPABASE_KEY")
    if os.environ.get("APC_SUPABASE_KEY")
    else apc_lb_conf.supabase.key
)
val_supabase_key: str = (
    _val_supabase_key if _val_supabase_key is not None else ""
)
del _val_supabase_key
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

_val_base_event_url: str | None = (
    os.environ.get("APC_BASE_EVENT_URL")
    if os.environ.get("APC_BASE_EVENT_URL")
    else apc_lb_conf.supabase.base_event_url
)
val_base_event_url: str = (
    _val_base_event_url if _val_base_event_url is not None else ""
)
del _val_base_event_url
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

_val_base_event_img_url: str | None = (
    os.environ.get("APC_BASE_EVENT_IMG_URL")
    if os.environ.get("APC_BASE_EVENT_IMG_URL")
    else apc_lb_conf.supabase.base_event_img_url
)
val_base_event_img_url: str = (
    _val_base_event_img_url if _val_base_event_img_url is not None else ""
)
del _val_base_event_img_url
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

_val_local_database: str | None = (
    os.environ.get("APC_LOCAL_DATABASE")
    if os.environ.get("APC_LOCAL_DATABASE") is not None
    else apc_lb_conf.database
)
val_local_database: str = (
    _val_local_database if _val_local_database is not None else ""
)
del _val_local_database

_val_lemmy_user: str | None = (
    os.environ.get("APC_LEMMY_USER")
    if os.environ.get("APC_LEMMY_USER") is not None
    else apc_lb_conf.lemmy.user
)
val_lemmy_user: str = _val_lemmy_user if _val_lemmy_user is not None else ""
del _val_lemmy_user

_val_lemmy_password: str | None = (
    os.environ.get("APC_LEMMY_PASSWORD")
    if os.environ.get("APC_LEMMY_PASSWORD") is not None
    else apc_lb_conf.lemmy.password
)
val_lemmy_password: str = (
    _val_lemmy_password if _val_lemmy_password is not None else ""
)
del _val_lemmy_password

_val_lemmy_community: str | None = (
    os.environ.get("APC_LEMMY_COMMUNITY")
    if os.environ.get("APC_LEMMY_COMMUNITY") is not None
    else apc_lb_conf.lemmy.community
)
val_lemmy_community: str = (
    _val_lemmy_community if _val_lemmy_community is not None else ""
)
del _val_lemmy_community

_val_lemmy_instance: str | None = (
    os.environ.get("APC_LEMMY_INSTANCE")
    if os.environ.get("APC_LEMMY_INSTANCE") is not None
    else apc_lb_conf.lemmy.instance
)
val_lemmy_instance: str = (
    _val_lemmy_instance if _val_lemmy_instance is not None else ""
)
del _val_lemmy_instance

_val_langcode: str | None = os.environ.get("APC_LANGCODE")
val_langcode: str = _val_langcode if _val_langcode else ""
del _val_langcode
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
