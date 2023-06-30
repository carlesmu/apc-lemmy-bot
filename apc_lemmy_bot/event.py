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
apc_lemmy_bot event module.

@author: Carles Muñoz Gorriz <carlesmu@internautas.org>
"""

import datetime
import json
import textwrap
import warnings

from typing import List, Optional
from urllib.parse import urlsplit

# https://github.com/supabase-community/supabase-py
from supabase import create_client, Client

from .__init__ import apc_lb_conf


class Event:
    """The Event class represents a event."""

    def __init__(
        self,
        event: dict,
        base_event_url: Optional[str] = None,
        base_event_img_url: Optional[str] = None,
    ):
        self.id: Optional[str] = None
        self.title: Optional[str] = None
        self.slugTitle: Optional[str] = None
        self.otd: Optional[str] = None
        self.description: Optional[str] = None
        self.imgAltText: Optional[str] = None
        self.NSFW: Optional[bool] = None
        self.imgSrc: Optional[str] = None
        self.date: Optional[datetime.date] = None
        self.links: List[Optional[str]] = []
        self.tags: List[Optional[str]] = []
        self.day: Optional[int] = None
        self.month: Optional[int] = None
        self.base_event_url: str = (
            base_event_url
            if base_event_url is not None
            else apc_lb_conf.supabase.base_event_url
        )
        self.base_event_img_url: str = (
            base_event_img_url
            if base_event_img_url is not None
            else apc_lb_conf.supabase.base_event_img_url
        )

        if event.keys() != self.__dict__.keys():
            for missed_dict in [x for x in self.__dict__ if x not in event]:
                if missed_dict not in ["base_event_url", "base_event_img_url"]:
                    warnings.warn(
                        f"Key '{missed_dict}' missed in event '{event['slugTitle']}'."
                    )

            for missed_key in [x for x in event if x not in self.__dict__]:
                warnings.warn(
                    f"Unexpected key '{missed_key}' in event '{event['slugTitle']}'."
                )

        for e_key, e_value in event.items():
            match e_key:
                case "date":
                    dstr = e_value.split("-")
                    setattr(
                        self,
                        e_key,
                        datetime.date(int(dstr[0]), int(dstr[1]), int(dstr[2])),
                    )
                case "month" | "day":
                    setattr(self, e_key, int(e_value))
                case _:
                    setattr(self, e_key, e_value)

    def json(self) -> str:
        """Return a json serialized dict."""
        return json.dumps(self.__dict__, indent=4, default=str)

    def get_event_url(self) -> str:
        """Return the original url of the event."""
        return f"{self.base_event_url}{self.slugTitle}"

    def get_image_url(self) -> Optional[str]:
        """Return the original image url."""
        if self.imgSrc:
            return f"{self.base_event_img_url}{self.imgSrc}"
        return None

    def nice_title(self, max_length: Optional[int] = None) -> str:
        """@TODO: improved description."""
        if max_length:
            return textwrap.shorten(
                f"{self.title} {self.otd}", width=max_length, placeholder="..."
            )
        return f"{self.title} {self.otd}"

    def nice_description(self) -> str:
        """Improved description."""
        if not self.description:
            return ""
        # Replace asterisks * with heavy asterisk ✱
        nice_desc = self.description.replace("*", "✱")
        # Replace underscore _ with fullwith low line ＿
        nice_desc = nice_desc.replace("_", "＿")
        # Replace grave accent ` with apostrophe '
        nice_desc = nice_desc.replace("`", "'")

        # Improve quotation text at end of the description:
        text = nice_desc.split("\n\n")
        if (
            len(text) > 1
            and text[-1].startswith("- ")
            and text[-2].startswith('"')
            and text[-2].endswith('"')
        ):
            text[-2] = f"> *{text[-2]}*"
            text[-1] = f"> `{text[-1]}`"
            nice_desc = "\n\n".join(text[:-1])
            nice_desc = f"{nice_desc}\n> \n{text[-1]}"
        return nice_desc

    def get_content(self) -> str:
        """Return a formated missage content of the event."""

        ret = f"## {self.title}\n\n"

        if self.date:
            ret += f"### {self.date.strftime('%a %b %d, %Y')}\n"

        if self.get_image_url() is not None:
            if self.NSFW:
                ret += "::: spoiler Image (NSFW):\n"
            ret += f"![Image]({self.get_image_url()})\n"
            if self.NSFW:
                ret += ":::\n"
            if self.imgAltText is not None:
                ret += f"\nImage: *{self.imgAltText}*\n"
            ret += "\n---\n"

        ret += self.nice_description() + "\n\n---\n"

        if self.date is not None:
            ret += f"- Date: {self.date}\n"

        if len(self.links) > 0:
            ret += "- Learn More: "
            i = 0
            for link in self.links:
                ret += f"[{str(urlsplit(link).netloc)}]({link})"
                i += 1
                if i < len(self.links):
                    ret += ", "
                else:
                    ret += "."
            ret += "\n"

        if len(self.tags) > 0:
            ret += "- Tags: "
            i = 0
            for tag in self.tags:
                ret += f"#{tag}"
                i += 1
                if i < len(self.tags):
                    ret += ", "
                else:
                    ret += "."
            ret += "\n"

        ret += f"- Source: [{urlsplit(self.get_event_url()).netloc}]({self.get_event_url()})"

        return ret


def get_dated_events(
    date: datetime.date = datetime.datetime.today().date(),
    url: Optional[str] = None,
    key: Optional[str] = None,
    base_event_url: Optional[str] = None,
    base_event_img_url: Optional[str] = None,
) -> List[Event]:
    """Get the events of a day."""
    if not url:
        url = apc_lb_conf.supabase.url
    if not key:
        key = apc_lb_conf.supabase.key
    if not base_event_url:
        base_event_url = apc_lb_conf.supabase.base_event_url
    if not base_event_img_url:
        base_event_img_url = apc_lb_conf.supabase.base_event_img_url

    supabase: Client = create_client(url, key)
    response = (
        supabase.table("events")
        .select("*")
        .eq("month", str(date.month))
        .eq("day", str(date.day))
        .execute()
    )
    # Assert we pulled real data.
    assert len(response.data) > 0

    events = []
    for event in response.data:
        events.append(Event(event, base_event_url, base_event_img_url))
    return events
