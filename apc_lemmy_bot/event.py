# -*- coding: utf-8 -*-
#    Copyright (C) 2023-2025 Carles Muñoz Gorriz <carlesmu@internautas.org>
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
from typing import Optional
from urllib.parse import urlsplit

# https://github.com/supabase-community/supabase-py
from supabase import Client, create_client

from apc_lemmy_bot import apc_lb_conf

TODAY: datetime.date = datetime.datetime.now(tz=datetime.UTC).date()


class Event:
    """A class to store events."""

    def __init__(
        self,
        event: dict,
        base_event_url: Optional[str] = None,
        base_event_img_url: Optional[str] = None,
        force_langcode: Optional[str] = None,
    ) -> None:
        """
        Initialize a Event object.

        Parameters
        ----------
        event : dict
            A dictionary with de event data.
        base_event_url : Optional[str], optional
            The base/common URL shared for the events. The default is None.
        base_event_img_url : Optional[str], optional
            The base/common URLs shared for the images. The default is None.
        force_langcode : Optional[str], optional
            The ISO 639-2 language code in which the event has been written.
            The default is None.
         : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        self.id: Optional[str] = None
        self.title: Optional[str] = None
        self.slugTitle: Optional[str] = None
        self.otd: Optional[str] = None
        self.description: Optional[str] = None
        self.imgAltText: Optional[str] = None
        self.NSFW: Optional[bool] = None
        self.imgSrc: Optional[str] = None
        self.date: Optional[datetime.date] = None
        self.links: list[Optional[str]] = []
        self.tags: list[Optional[str]] = []
        self.day: Optional[int] = None
        self.month: Optional[int] = None

        if force_langcode:
            self.langcode = force_langcode
        else:
            self.langcode = ""

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
                if missed_dict not in [
                    "base_event_url",
                    "base_event_img_url",
                    "langcode",
                ]:
                    warnings.warn(
                        (
                            f"Key '{missed_dict}' missed in event "
                            f"'{event['slugTitle']}'."
                        ),
                        stacklevel=2,
                    )

            for missed_key in [x for x in event if x not in self.__dict__]:
                warnings.warn(
                    (
                        f"Unexpected key '{missed_key}' in event "
                        f"'{event['slugTitle']}'."
                    ),
                    stacklevel=2,
                )

        for e_key, e_value in event.items():
            match e_key:
                case "date":
                    dstr = e_value.split("-")
                    setattr(
                        self,
                        e_key,
                        datetime.date(
                            int(dstr[0]),
                            int(dstr[1]),
                            int(dstr[2]),
                        ),
                    )
                case "month" | "day":
                    setattr(self, e_key, int(e_value))
                case _:
                    setattr(self, e_key, e_value)

    def json(self) -> str:
        """
        Get a serialization of the event.

        Returns
        -------
        str
            The serialized str of the event.

        """
        return json.dumps(self.__dict__, indent=4, default=str)

    def get_event_url(self) -> str:
        """
        Return the original URL of the event.

        Returns
        -------
        str
            The URL of the event.

        """
        return f"{self.base_event_url}{self.slugTitle}"

    def get_image_url(self) -> Optional[str]:
        """
        Return the original image URL.

        Returns
        -------
        Optional[str]
            The original URL of the image, or `None` if there were not image.

        """
        if self.imgSrc:
            return f"{self.base_event_img_url}{self.imgSrc}"
        return None

    def nice_title(self, max_length: Optional[int] = None) -> str:
        """
        Return a title with part of the short description `self.otd`.

        Parameters
        ----------
        max_length : Optional[int], optional
            The max length of the string to return. When not informed, it
            return the `self.title` + `self.otd`. The default is None.

        Returns
        -------
        str
            A nice title.

        """
        if max_length:
            return textwrap.shorten(
                f"{self.title} {self.otd}",
                width=max_length,
                placeholder="...",
            )
        return f"{self.title} {self.otd}"

    def nice_description(self) -> str:
        """
        Improved description to be added in a Lemmy post.

        Returns
        -------
        str
            The description to be posted.

        """
        if not self.description:
            return ""
        # Replace asterisks * with heavy asterisk ✱
        nice_desc = self.description.replace("*", "✱")
        # Replace underscore _ with full-with low line ＿
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
        """
        Return a formatted message content of the event.

        It contains markdown formatted text.

        Returns
        -------
        str
            The event content.

        """
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
                ret += (
                    f"[#{tag}](/search?q=%23{tag}&type=Posts"
                    "&listingType=All&page=1&sort=New)"
                )
                i += 1
                if i < len(self.tags):
                    ret += ", "
                else:
                    ret += "."
            ret += "\n"

        ret += (
            f"- Source: [{urlsplit(self.get_event_url()).netloc}]"
            f"({self.get_event_url()})"
        )

        return ret

    def __eq__(self, other: object) -> bool:
        """
        Compare 2 event objects.

        Parameters
        ----------
        other : Event
            DESCRIPTION.

        Returns
        -------
        bool
            True if they share the same content.

        """
        if not isinstance(other, Event):
            return NotImplemented
        return self.__dict__ == other.__dict__


def get_dated_events(
    date: datetime.date = TODAY,
    url: Optional[str] = apc_lb_conf.supabase.url,
    key: Optional[str] = apc_lb_conf.supabase.key,
    base_event_url: Optional[str] = apc_lb_conf.supabase.base_event_url,
    base_event_img_url: Optional[
        str
    ] = apc_lb_conf.supabase.base_event_img_url,
    force_langcode: Optional[str] = None,
) -> list[Event]:
    """
    Get the dated events of a day looking for them in a *Supabase* database.

    Parameters
    ----------
    date : datetime.date, optional
        The date to use to look for events. The default is
        `datetime.datetime.now(tz=datetime.UTC).date()`.
    url : Optional[str], optional
        The URL of the database. The default is apc_lb_conf.supabase.url.
    key : Optional[str], optional
        The access key to the database. The default is
        apc_lb_conf.supabase.key.
    base_event_url : Optional[str], optional
        The base/common URL where the event can be shown. The default is
        apc_lb_conf.supabase.base_event_url.
    base_event_img_url : Optional[str], optional
        The base/common URL where the event image can be shown. The default is
        apc_lb_conf.supabase.base_event_img_url.
    force_langcode : Optional[str], optional
        The ISO 639-2 `langcode` in which the event has been written. The
        default is None.

    Returns
    -------
    list[Event]
        A list of events.

    """
    apc_lb_conf.supabase.url = url if url else ""
    apc_lb_conf.supabase.key = key if key else ""
    apc_lb_conf.supabase.base_event_url = (
        base_event_url if base_event_url else ""
    )
    apc_lb_conf.supabase.base_event_img_url = (
        base_event_img_url if base_event_img_url else ""
    )

    supabase: Client = create_client(
        apc_lb_conf.supabase.url,
        apc_lb_conf.supabase.key,
    )
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
        events.append(
            Event(event, base_event_url, base_event_img_url, force_langcode),
        )
    return events
