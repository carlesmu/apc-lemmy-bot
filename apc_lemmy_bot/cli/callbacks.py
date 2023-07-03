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

"""
apc_lemmy_bot cli.callbacks module."""

import datetime
from urllib.parse import urlparse

import typer

from pythorhead.types import LanguageType
from apc_lemmy_bot import __app__, __version__


def date(date: str) -> str:
    """Validate a date argument.

    It should have format YYYY-MM-DD
    """
    if not date:
        return datetime.datetime.today().strftime("%Y-%m-%d")
    try:
        return datetime.datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%m-%d")
    except ValueError as err:
        raise typer.BadParameter(f"{err}")


def langcode(value: str) -> str:
    """Validates a language code.

    It should have format XX.
    """
    if value is None:
        return
    try:
        return LanguageType[value.upper()].name
    except KeyError:
        raise typer.BadParameter(f"KeyError: Langcode '{value}' undefined in Pythorhead")

    raise typer.BadParameter(f"Langcode '{value}' undefined in Pythorhead")


def output_format(value: str) -> str:
    """Validate the --format option.

    It should be 'json', 'txt' or 'none'.
    """
    if not value.lower() in ["json", "txt", "none"]:
        raise typer.BadParameter(f"Not recognized '{value}'")
    return value.lower()


def supabase_key(value: str) -> str:
    """Validate the --sb-key option."""
    if value.strip() == "":
        raise typer.BadParameter(f"Cannot precess supabase empty key '{value}'")
    return value


def version(value: bool):
    """Validate the --version option."""
    if value:
        print(f"{__app__}-v{__version__}")
        raise typer.Exit()


def url(url: str) -> str:
    """Validate a valid URL.

    It should have protocols 'file', 'http' or 'https'.
    """
    result = urlparse(url)
    if all(
        [
            result.scheme in ["file", "http", "https"],
            result.scheme,
            result.netloc,
        ]
    ):
        return url
    raise typer.BadParameter(f"Not recognized URL '{url}'")


def silence(value: bool):
    """Validate the option --silence."""
    return value
