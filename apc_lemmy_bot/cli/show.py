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

"""apc_lemmy_bot.cli show module."""

import typer
from typing_extensions import Annotated

from apc_lemmy_bot import apc_lb_conf
from apc_lemmy_bot.event import get_dated_events

from . import app
from .callbacks import callback_output_format
from .common import (
    arg_date,
    val_date,
    opt_supabase_url,
    val_supabase_url,
    opt_supabase_key,
    val_supabase_key,
    opt_base_event_url,
    val_base_event_url,
    opt_base_event_img_url,
    val_base_event_img_url,
    opt_silence,
    val_silence,
    opt_version,
    val_version,
)


@app.command()
def show(
    date: arg_date = val_date,
    supabase_url: opt_supabase_url = val_supabase_url,
    supabase_key: opt_supabase_key = val_supabase_key,
    base_event_url: opt_base_event_url = val_base_event_url,
    base_event_img_url: opt_base_event_img_url = val_base_event_img_url,
    output_format: Annotated[
        str,
        typer.Option(
            "--format",
            "-f",
            help="Output format [json | txt | none].",
            show_default=True,
            callback=callback_output_format,
        ),
    ] = "txt",
    silence: opt_silence = val_silence,
    version: opt_version = val_silence,
):
    """Show a day's events stored in a supabase database."""
    apc_lb_conf.supabase.url = supabase_url
    apc_lb_conf.supabase.key = supabase_key
    apc_lb_conf.supabase.base_event_url = base_event_url
    apc_lb_conf.supabase.base_event_img_url = base_event_img_url

    if not silence:
        print(f"Fetching events for date {date.strftime('%d %B')}:")

    events = get_dated_events(
        date=date,
        url=supabase_url,
        key=supabase_key,
        base_event_url=base_event_url,
        base_event_img_url=base_event_img_url,
    )

    for event in events:
        match output_format:
            case "json":
                print(event.json())
            case "txt":
                print(event.get_content())
            case "none":
                pass
            case _:
                raise typer.BadParameter("Non recognized -f {output_format}")

    if not silence:
        print(f"{len(events)} fetched.")
