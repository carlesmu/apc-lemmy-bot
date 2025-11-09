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
from typing import Annotated

import typer

from apc_lemmy_bot import apc_lb_conf
from apc_lemmy_bot.event import get_dated_events

from . import app, callbacks, common


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
            help="Output format [json | txt | none]. Only useful with SHOW",
            show_default=True,
            callback=callbacks.output_format,
        ),
    ] = "txt",
    langcode: common.opt_langcode = common.val_langcode,
    silence: common.opt_silence = common.val_silence,
    version: common.opt_version = common.val_version,
) -> None:
    """Show a day's events stored in a supabase database."""
    _ = version  # unused variable required for the command line

    apc_lb_conf.supabase.url = supabase_url
    apc_lb_conf.supabase.key = supabase_key
    apc_lb_conf.supabase.base_event_url = base_event_url
    apc_lb_conf.supabase.base_event_img_url = base_event_img_url

    if not silence:
        d_str = (
            datetime.datetime.strptime(date, "%Y-%m-%d")
            .astimezone(None)
            .strftime("%d %B")
        )
        print(f"Fetching events for date {d_str}:")

    events = get_dated_events(
        date=datetime.datetime.strptime(date, "%Y-%m-%d").astimezone(None),
        url=supabase_url,
        key=supabase_key,
        base_event_url=base_event_url,
        base_event_img_url=base_event_img_url,
        force_langcode=None if langcode == "" else langcode,
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
                msg = "Non recognized -f {output_format}"
                raise typer.BadParameter(msg)

    if not silence:
        print(f"{len(events)} fetched.")
