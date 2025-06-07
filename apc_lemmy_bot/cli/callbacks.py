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

"""apc_lemmy_bot cli.callbacks module."""

import datetime
from urllib.parse import urlparse

import typer

from pythorhead.types import LanguageType
from apc_lemmy_bot import __app__, __version__


def date(input_date: str) -> str:
    """Validate a date argument.

    It should have format YYYY-MM-DD

    Parameters
    ----------
    input_date : str
        The date to validate.

    Raises
    ------
    typer.BadParameter
        raises a BadParameter exception when it's a unexpected date format.

    Returns
    -------
    str
        The date.

    """
    if not input_date:
        return datetime.datetime.today().strftime("%Y-%m-%d")
    try:
        return datetime.datetime.strptime(input_date, "%Y-%m-%d").strftime("%Y-%m-%d")
    except ValueError as err:
        raise typer.BadParameter(f"{err}")


def from_(value: str) -> str:
    """Validate the FROM argument.

    Parameters
    ----------
    value : str
        the source of the events. Right values are: **SUPABASE** and **DATABASE**.

    Raises
    ------
    typer.BadParameter
        When we cannot validate the input.

    Returns
    -------
    str
        The FROM argument in upper case.
    """
    if (val := value.upper()) in {"SUPABASE", "DATABASE"}:
        return val
    raise typer.BadParameter(f"It sould be 'SUPABASE' or 'DATABASE', not '{value}'")


def langcode(value: str | None) -> str | None:
    """Validate the --langcode option.

    It should have format XX or None.

    Parameters
    ----------
    value : str | None
        The language code in ISO 639 format or None for no language code.

    Raises
    ------
    typer.BadParameter
        When we cannot validate the language code.

    Returns
    -------
    str | None
        The validated language code or None if that was the input.

    """
    if value is None:
        return None
    try:
        return str(LanguageType[value.upper()].name)
    except KeyError as exc:
        raise typer.BadParameter(
            f"KeyError: Langcode '{value}' undefined in Pythorhead"
        ) from exc

    raise typer.BadParameter(f"Langcode '{value}' undefined in Pythorhead")


def output_format(value: str) -> str:
    """Validate the --format option.

    It should be 'json', 'txt' or 'none'.

    Parameters
    ----------
    value : str
        the format option.

    Raises
    ------
    typer.BadParameter
        When we cannot validate the option.

    Returns
    -------
    str
        the output format in lower case.

    """
    if value.lower() not in {"json", "txt", "none"}:
        raise typer.BadParameter(f"Not recognized '{value}'")
    return value.lower()


def supabase_key(ctx: typer.Context, value: str) -> str:
    """Validate the --sb-key option.

    Parameters
    ----------
    ctx : typer.Context
        The context of the command.
    value : str
        The SUPABASE key.

    Raises
    ------
    typer.BadParameter
        When we cannot validate the option.

    Returns
    -------
    str
        The SUPABASE key.

    """
    # In the db option not originated from SUPABASE the SUPABASE parameters are optional:
    if (
        ctx.info_name == "db"  # pylint: disable=R2004  # magic-value-comparison
        and ctx.params["from_"]  # pylint: disable=R2004  # magic-value-comparison
        != "SUPABASE"  # pylint: disable=R2004  # magic-value-comparison
        and not value
    ):
        return value

    if not value.strip():
        raise typer.BadParameter(f"Cannot precess supabase empty key '{value}'")
    return value


def to_(value: str) -> str:
    """Validate the TO argument.

    Parameters
    ----------
    value : str
        the destination of the events. Right values are: **DATABASE**, **LEMMY** or
        **SHOW**

    Raises
    ------
    typer.BadParameter
        When we cannot validate the option.

    Returns
    -------
    str
        The TO argument in upper case.
    """
    if (val := value.upper()) in {"DATABASE", "LEMMY", "SHOW"}:
        return val
    raise typer.BadParameter(f"It sould be 'DATABASE', 'LEMMY' or 'SHOW', not '{value}'")


def version(value: bool) -> None:
    """Validate the --version option and if it's true it shows the version and exit.

    Parameters
    ----------
    value : bool
        If the version should be shown.

    Raises
    ------
    typer.Exit
        After the version is shown.

    Returns
    -------
    None.

    """
    if value:
        print(f"{__app__}-v{__version__}")
        raise typer.Exit()


def url(ctx: typer.Context, input_url: str) -> str:
    """Validate a valid URL.

    It should have protocols 'file', 'http' or 'https'.

    Parameters
    ----------
    ctx : typer.Context
        The option value.
    input_url: str
        The input url.

    Raises
    ------
    typer.BadParameter
        When we cannot validate the option.

    Returns
    -------
    value : str
        The url.
    """
    # In the db option not originated from SUPABASE the SUPABASE parameters are optional:
    if (
        ctx.info_name == "db"  # pylint: disable=R2004  # magic-value-comparison
        and ctx.params["from_"]  # pylint: disable=R2004  # magic-value-comparison
        != "SUPABASE"  # pylint: disable=R2004  # magic-value-comparison
        and not input_url
    ):
        return input_url

    result = urlparse(input_url)
    if all(
        [
            result.scheme in {"file", "http", "https"},
            result.scheme,
            result.netloc,
        ]
    ):
        return input_url
    raise typer.BadParameter(f"Not recognized URL '{input_url}'")


def silence(value: bool) -> bool:
    """Validate the option --silence.

    Parameters
    ----------
    value : bool
        the option value.

    Returns
    -------
    value : bool
        The option value.

    """
    return value
