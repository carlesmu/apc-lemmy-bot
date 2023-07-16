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

"""apc_lemmy_bot.cli post module."""

import datetime
import sched
import time

import typer
from typing_extensions import Annotated

from apc_lemmy_bot import apc_lb_conf
from apc_lemmy_bot.event import get_dated_events, Event
from apc_lemmy_bot.lemmy import LemmyException, login, create_event_post

from . import app
from . import callbacks, common


def _create_event_post(
    event: Event,
    schedule: sched.scheduler,
    silence: bool,
    lemmy_instance: str,
    lemmy_user: str,
    lemmy_password: str,
    lemmy_community: str,
) -> None:
    if not silence:
        print(
            f"Logging to lemmy instance {apc_lb_conf.lemmy.instance}",
            end=" ... ",
        )
    try:
        lemmy = login(lemmy_instance, lemmy_user, lemmy_password)
    except LemmyException as err:
        print(f"\nLemmyException: {err}")
        raise typer.Exit(1)

    if not silence:
        print("Logued.")

    if not silence:
        print(f"Posting {event.id}: {event.slugTitle}", end=" ... ")

    try:
        create_event_post(event, lemmy, lemmy_community, langcode=event.langcode)
    except LemmyException as err:
        print(f"\nLemmyException: {err}")
        raise typer.Exit(1)

    if not silence:
        print("Posted.")
        if not schedule.empty():
            minutes = float(apc_lb_conf.delay / 60)
            hours = float(apc_lb_conf.delay / 60 / 60)
            if hours > 1:
                time_txt = f"{hours:.2f} hours"
            elif minutes > 1:
                time_txt = f"{minutes:.2f} minutes"
            else:
                time_txt = f"{apc_lb_conf.delay} seconds"
            print(f"  ... Waiting {time_txt} for the next event to be posted.")


@app.command()
def post(
    date: common.arg_date = common.val_date,
    supabase_url: common.opt_supabase_url = common.val_supabase_url,
    supabase_key: common.opt_supabase_key = common.val_supabase_key,
    base_event_url: common.opt_base_event_url = common.val_base_event_url,
    base_event_img_url: common.opt_base_event_img_url = common.val_base_event_img_url,
    lemmy_user: Annotated[
        str,
        typer.Option(
            "--lm-user",
            rich_help_panel="Lemmy",
            help="User of the lemmy instance that will post the events",
            show_default=True,
            envvar="APC_LEMMY_USER",
        ),
    ] = apc_lb_conf.lemmy.user,
    lemmy_password: Annotated[
        str,
        typer.Option(
            "--lm-password",
            rich_help_panel="Lemmy",
            help="Password of the user of the lemmy instance",
            envvar="APC_LEMMY_PASSWORD",
        ),
    ] = apc_lb_conf.lemmy.password,
    lemmy_community: Annotated[
        str,
        typer.Option(
            "--lm-community",
            rich_help_panel="Lemmy",
            help="Lemmy comumunity of the instance where the events be posted",
            envvar="APC_LEMMY_COMMUNITY",
        ),
    ] = apc_lb_conf.lemmy.community,
    lemmy_instance: Annotated[
        str,
        typer.Option(
            "--lm-instance",
            rich_help_panel="Lemmy",
            help="Base URL of the lemmy instance where the events will be posted",
            callback=callbacks.url,
            show_default=True,
            envvar="APC_LEMMY_INSTANCE",
        ),
    ] = apc_lb_conf.lemmy.instance,
    delay: Annotated[
        int,
        typer.Option(
            "--delay",
            "-d",
            rich_help_panel="Lemmy",
            help="Delay in seconds between posts",
            envvar="APC_DELAY",
        ),
    ] = apc_lb_conf.delay,
    langcode: common.opt_langcode = common.val_langcode,
    silence: common.opt_silence = common.val_silence,
    version: common.opt_version = common.val_version,
):
    """Post a day's events in a lemmy community."""
    apc_lb_conf.supabase.url = supabase_url
    apc_lb_conf.supabase.key = supabase_key
    apc_lb_conf.supabase.base_event_url = base_event_url
    apc_lb_conf.supabase.base_event_img_url = base_event_img_url
    apc_lb_conf.lemmy.instance = lemmy_instance
    apc_lb_conf.lemmy.user = lemmy_user
    apc_lb_conf.lemmy.password = lemmy_password
    apc_lb_conf.lemmy.community = lemmy_community
    apc_lb_conf.delay = delay

    if not silence:
        d_str = datetime.datetime.strptime(date, "%Y-%m-%d").strftime("%d %B")
        print(
            f"Fetching events for date {d_str}",
            end=" ... ",
        )

    events = get_dated_events(
        date=datetime.datetime.strptime(date, "%Y-%m-%d"),
        url=supabase_url,
        key=supabase_key,
        base_event_url=base_event_url,
        base_event_img_url=base_event_img_url,
        force_langcode=None if langcode == "" else langcode,
    )

    if not silence:
        print(f"{len(events)} fetched.")

    schedule = sched.scheduler(time.monotonic, time.sleep)
    acum_delay: int = 0
    for event in events:
        schedule.enter(
            acum_delay,
            1,
            _create_event_post,
            argument=(
                event,
                schedule,
                silence,
                lemmy_instance,
                lemmy_user,
                lemmy_password,
                lemmy_community,
            ),
        )
        acum_delay += apc_lb_conf.delay

    schedule.run()
