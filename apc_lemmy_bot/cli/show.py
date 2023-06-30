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

import datetime
import typer
from typing_extensions import Annotated

from apc_lemmy_bot import apc_lb_conf
from apc_lemmy_bot.event import get_dated_events

from . import app
from .cli import callbacks, common


@app.command()
def show(
    date: common.arg_date = common.val_date,
    supabase_url: common.opt_supabase_url = common.val_supabase_url,
    supabase_key: common.opt_supabase_key = common.val_supabase_key,
    base_event_url: common.opt_base_event_url = common.val_base_event_url,
    base_event_img_url: common.opt_base_event_img_url = common.val_base_event_img_url,
    output_format: Annotated[
        str,
        typer.Option(
            "--format",
            "-f",
            help="Output format [json | txt | none].",
            show_default=True,
            callback=callbacks.output_format,
        ),
    ] = "txt",
    silence: common.opt_silence = common.val_silence,
    version: common.opt_version = common.val_version,
):
    """Show a day's events stored in a supabase database."""
    apc_lb_conf.supabase.url = supabase_url
    apc_lb_conf.supabase.key = supabase_key
    apc_lb_conf.supabase.base_event_url = base_event_url
    apc_lb_conf.supabase.base_event_img_url = base_event_img_url

    if not silence:
        print(
            f"Fetching events for date {datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%d %B')}:"
        )

    events = get_dated_events(
        date=datetime.datetime.strptime(date, "%Y-%m-%d"),
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
