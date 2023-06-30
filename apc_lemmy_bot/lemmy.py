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
"""apc_lemmy_bot lemmy module."""

from typing import Optional
from pythorhead import Lemmy

from .__init__ import apc_lb_conf, LEMMY_MAX_TITLE_LENGTH
from .event import Event


class LemmyException(Exception):
    """Exception rised fot errors connection to the lemmy instance."""


def login(instance: str = None, user: str = None, password: str = None) -> Lemmy:
    """Login into a lemmy instance."""
    if instance is None:
        instance = apc_lb_conf.lemmy.instance
    if user is None:
        user = apc_lb_conf.lemmy.user
    if password is None:
        password = apc_lb_conf.lemmy.password

    lemmy = Lemmy(instance)

    if not lemmy.log_in(user, password):
        if not lemmy._requestor.nodeinfo:
            raise LemmyException(f"Sorry, cannot connect to lemmy instance {instance}.")
        raise LemmyException(
            f"Sorry, cannot login {user} into {instance}. Bad user or wrong password."
        )

    return lemmy


def create_post(
    lemmy: Lemmy,
    title: str,
    url: str,
    body: str,
    nsfw: bool,
    community: str = None,
    honeypot: Optional[str] = None,
    language_id: Optional[int] = None,
) -> Optional[dict]:
    """Create a lemy post."""
    if community is None:
        community = apc_lb_conf.lemmy.community

    community_id = lemmy.discover_community(community)
    if community_id is None:
        raise LemmyException(f"Sorry, cannot find community '{community}'")

    created: Optional[dict] = lemmy.post.create(
        community_id,
        name=title,
        url=url,
        body=body,
        nsfw=nsfw,
        honeypot=honeypot,
        language_id=language_id,
    )

    if not created:
        raise LemmyException(
            f"Sorry, cannot creat post {title} in community_id={community_id}"
        )

    return created


def create_event_post(
    event: Event,
    lemmy: Lemmy,
    community: Optional[str] = None,
    honeypot: Optional[str] = None,
    language_id: Optional[int] = None,
) -> Optional[dict]:
    """Create a lemmy post using an event."""
    if community is None:
        community = apc_lb_conf.lemmy.community

    # We post the image, if it not exists, the link to the event:
    url = event.get_image_url()
    if url is None:
        url = event.get_event_url()

    return create_post(
        lemmy,
        title=event.nice_title(LEMMY_MAX_TITLE_LENGTH),
        url=url,
        body=event.get_content(),
        nsfw=event.NSFW if event.NSFW else False,
        community=community,
        honeypot=honeypot,
        language_id=language_id,
    )
