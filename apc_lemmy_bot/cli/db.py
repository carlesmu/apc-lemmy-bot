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

"""apc_lemmy_bot.cli db module."""

import datetime
import tempfile
from pathlib import Path
from uuid import UUID

import typer
from typing_extensions import Annotated

import apc_lemmy_bot.database
from apc_lemmy_bot import apc_lb_conf
from apc_lemmy_bot.event import Event, get_dated_events
from apc_lemmy_bot.lemmy import (
    LemmyException,
    create_event_post,
    login,
    upload_img,
)

from . import app, callbacks, common


def _create_event_post(
    event: Event,
    silence: bool,
    lemmy_instance: str,
    lemmy_user: str,
    lemmy_password: str,
    lemmy_community: str,
    database_obj: apc_lemmy_bot.database.Database,
) -> dict | None:
    """
    Create a post in a lemmy instance.

    Parameters
    ----------
    event : Event
        The event to be posted.
    silence : bool
        Don't show information.
    lemmy_instance : str
        The lemmy instance to connect (e.g.: `https:enterprise.lemmy.ml`).
    lemmy_user : str
        The lemmy user.
    lemmy_password : str
        The lemmy user password.
    lemmy_community : str
        The community where it will be posted.
    database_obj : apc_lemmy_bot.database.Database
        The database object where the events are stored


    Raises
    ------
    typer.Exit
        If the Event cannot be posted.

    Returns
    -------
    Optional[dict]
        post data if successful.

    """
    if not silence:
        print(
            f"Logging to lemmy instance {apc_lb_conf.lemmy.instance}",
            end=" ... ",
        )
    try:
        lemmy = login(lemmy_instance, lemmy_user, lemmy_password)
    except LemmyException as err:
        print(f"\nLemmyException: {err}")
        raise typer.Exit(1) from err

    if not silence:
        print("Logued.")

    if not silence:
        print(f"Posting {event.id}: {event.slugTitle}", end=" ... ")

    # We check if we must upload the image to the lemmy instance
    view = database_obj.get_view_by_id(UUID(event.id))
    if (
        view is not None
        and "extended" in view.__dict__
        and "images" in view.__dict__
        and "imgSrc" in event.__dict__
        and event.imgSrc is not None
        and (view.extended.img_url is None or not view.extended.img_url)
        and view.images[0]
        and view.images[0].img
    ):
        # We upload the img from the database to the instance and we
        # update the url of the image in the event.
        if not silence:
            print("Uploading image", end=" ... ")

        _suffix: str = (
            event.imgSrc.replace("/", "_").replace("\\", "_")
            if event.imgSrc is not None
            else ""
        )
        with tempfile.NamedTemporaryFile(
            suffix=_suffix,
            delete=False,
        ) as tmp_file:
            tmp_file.write(
                apc_lemmy_bot.database.large_binary_to_bytes(
                    view.images[0].img,
                ),
            )
        tmp_file.close()
        img_url = ""
        try:
            img_url = upload_img(lemmy, tmp_file.name)
        except LemmyException as err:
            Path(tmp_file.name).unlink()  # the tmp file should be removed
            print(f"\nLemmyException: {err}")
            raise typer.Exit(1) from err

        Path(tmp_file.name).unlink()  # the tmp file should be removed

        event.base_event_img_url = ""
        event.imgSrc = img_url

    try:
        ret = create_event_post(
            event,
            lemmy,
            lemmy_community,
            langcode=event.langcode,
        )
    except LemmyException as err:
        print(f"\nLemmyException: {err}")
        raise typer.Exit(1) from err

    if not silence:
        if ret:
            print(f"Posted: {ret['post_view']['post']['ap_id']}")
        else:
            print("Posted.")

    return ret


@app.command()
def db(
    from_: Annotated[
        str,
        typer.Argument(
            callback=callbacks.from_,
            metavar="FROM",
            help="Where we get the events ['SUPABASE'|'DATABASE']",
        ),
    ],
    to_: Annotated[
        str,
        typer.Argument(
            callback=callbacks.to_,
            metavar="TO",
            help="Where we store the events ['DATABASE'|'LEMMY'|'SHOW']",
        ),
    ] = "SHOW",
    date: common.arg_date = common.val_date,
    database: Annotated[
        str,
        typer.Option(
            help=(
                "Local database url (Note: use a extra '/' if you want "
                "to use an absolute path)"
            ),
            envvar="APC_LOCAL_DATABASE",
        ),
    ] = common.val_local_database,
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
    ] = common.val_lemmy_user,
    lemmy_password: Annotated[
        str,
        typer.Option(
            "--lm-password",
            rich_help_panel="Lemmy",
            help="Password of the user of the lemmy instance",
            envvar="APC_LEMMY_PASSWORD",
        ),
    ] = common.val_lemmy_password,
    lemmy_community: Annotated[
        str,
        typer.Option(
            "--lm-community",
            rich_help_panel="Lemmy",
            help="Lemmy comumunity of the instance where the events be posted",
            envvar="APC_LEMMY_COMMUNITY",
        ),
    ] = common.val_lemmy_community,
    lemmy_instance: Annotated[
        str,
        typer.Option(
            "--lm-instance",
            rich_help_panel="Lemmy",
            help=(
                "Base URL of the lemmy instance where the events will be posted"
            ),
            callback=callbacks.url,
            show_default=True,
            envvar="APC_LEMMY_INSTANCE",
        ),
    ] = common.val_lemmy_instance,
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
    langcode: common.opt_langcode = common.val_langcode,
    silence: common.opt_silence = common.val_silence,
    version: common.opt_version = common.val_version,
) -> None:
    """Store events in the database or post or show them."""
    _ = version  # unused variable required fot the command line

    # Some validations
    if from_ == to_:
        msg = f"Error: FROM '{from_}' and TO '{to_}' cannot be equals"
        raise typer.BadParameter(msg)

    # The configuration:
    apc_lb_conf.supabase.url = supabase_url
    apc_lb_conf.supabase.key = supabase_key
    apc_lb_conf.supabase.base_event_url = base_event_url
    apc_lb_conf.supabase.base_event_img_url = base_event_img_url
    apc_lb_conf.lemmy.instance = lemmy_instance
    apc_lb_conf.lemmy.user = lemmy_user
    apc_lb_conf.lemmy.password = lemmy_password
    apc_lb_conf.lemmy.community = lemmy_community
    apc_lb_conf.database = database

    database_obj = apc_lemmy_bot.database.Database(
        database_url=apc_lb_conf.database,
        echo=False,
    )

    date_dt = datetime.datetime.strptime(date, "%Y-%m-%d").astimezone(None)

    match from_:
        case "SUPABASE":
            # Get the data from supabase and we store it to the database:
            if not silence:
                d_str = date_dt.strftime("%d %B")
                print(f"Fetching events for date {d_str}:")
            events = get_dated_events(
                date=date_dt,
                url=supabase_url,
                key=supabase_key,
                base_event_url=base_event_url,
                base_event_img_url=base_event_img_url,
                force_langcode=langcode if langcode else None,
            )
            if not silence:
                print(f"{len(events)} fetched.")
            for event in events:
                if not silence:
                    print(
                        (
                            f"- {apc_lb_conf.database} {event.id}: "
                            f"{event.slugTitle}"
                        ),
                        end="... ",
                    )
                database_obj.add_event(event, silence)

        case "DATABASE":
            pass

        case _:
            msg = f"Error: unexpected FROM '{from_}'"
            raise typer.BadParameter(msg)

    match to_:
        case "DATABASE":
            pass

        case "LEMMY":
            views = database_obj.get_views_by_month_day(
                date_dt.month,
                date_dt.day,
            )
            if not silence:
                print(
                    f"{0 if not views else len(views)} found in the database.",
                )
            random_event = None
            if views:
                random_event = database_obj.get_random_dated_event(
                    views,
                    date_dt,
                )
            if not random_event:
                print("There are not events for today or all has been posted.")
            else:
                post = _create_event_post(
                    random_event,
                    silence,
                    lemmy_instance,
                    lemmy_user,
                    lemmy_password,
                    lemmy_community,
                    database_obj,
                )
                url_ = (
                    f"{post['post_view']['post']['ap_id']}"
                    if post
                    else f"url:{random_event.id}"
                )
                database_obj.update_posted_event(UUID(random_event.id), url_)

        case "SHOW":
            views = database_obj.get_views_by_month_day(
                date_dt.month,
                date_dt.day,
            )
            if not silence:
                print(
                    f"{0 if not views else len(views)} found in the database.",
                )
            random_event = None
            if views:
                random_event = database_obj.get_random_dated_event(
                    views,
                    date_dt,
                )
            if not random_event:
                print("There are not events for today or all has been posted.")
            else:
                match output_format:
                    case "json":
                        print(random_event.json())
                    case "txt":
                        print(random_event.get_content())
                    case "none":
                        pass
                    case _:
                        msg = "Non recognized -f {output_format}"
                        raise typer.BadParameter(msg)

        case _:
            msg = f"Error: unexpected TO '{to_}'"
            raise typer.BadParameter(msg)
