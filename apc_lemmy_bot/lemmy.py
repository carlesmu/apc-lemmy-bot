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
"""apc_lemmy_bot Lemmy module."""

import warnings

from pythorhead import Lemmy
from pythorhead.types import LanguageType

from apc_lemmy_bot import LEMMY_MAX_TITLE_LENGTH, apc_lb_conf
from apc_lemmy_bot.event import Event


class LemmyError(Exception):
    """Exception raised for errors connecting to the Lemmy instance."""


def login(
    instance: str = apc_lb_conf.lemmy.user,
    user: str = apc_lb_conf.lemmy.user,
    password: str = apc_lb_conf.lemmy.password,
) -> Lemmy:
    """Login into a Lemmy instance."""
    apc_lb_conf.lemmy.instance = instance
    apc_lb_conf.lemmy.user = user
    apc_lb_conf.lemmy.password = password

    lemmy = Lemmy(instance, raise_exceptions=True, request_timeout=10)
    if not lemmy.nodeinfo:
        msg = f"Sorry, cannot connect to the Lemmy instance {instance}."
        raise LemmyError(msg)

    if not lemmy.log_in(user, password):
        msg = (
            f"Sorry, cannot login {user} into {instance}. Bad user "
            "or wrong password."
        )
        raise LemmyError(msg)

    return lemmy


def upload_img(lemmy: Lemmy, file_name: str) -> str:
    """
    Upload a image to a Lemmy instance.

    Parameters
    ----------
    lemmy : Lemmy
        The Lemmy instance that we get after login to it.
    file_name : str
        The image path to upload to the Lemmy instance.

    Raises
    ------
    LemmyError
        If the upload has failed.

    Returns
    -------
    str
        The url of the uploaded image.

    """
    uploaded = lemmy.image.upload(file_name)
    if not uploaded:
        msg = f"Sorry, cannot upload {file_name}."
        raise LemmyError(msg)

    if (
        len(uploaded) != 1
        or "image_url" not in uploaded[0]
        or "delete_url" not in uploaded[0]
    ):
        msg = f"Sorry, cannot upload {file_name}: {uploaded}"
        raise LemmyError(msg)
    print(uploaded)
    return f"{uploaded[0]['image_url']}"


def _create_post(
    lemmy: Lemmy,
    title: str,
    url: str,
    body: str,
    nsfw: bool,
    community: str,
    honeypot: str | None = None,
    langcode: str | None = None,
) -> dict | None:
    """Create a Lemmy post."""
    # Look for the language_id
    language_id = 0  # any
    if langcode is not None:
        try:
            language_id = LanguageType[langcode].value
        except KeyError:
            warnings.warn(
                f"Key 'Langcode '{langcode}' not defined in pythorhead.",
                stacklevel=2,
            )

    community_id = lemmy.discover_community(community)
    if community_id is None:
        msg = f"Sorry, cannot find community '{community}'"
        raise LemmyError(msg)

    created: dict | None = lemmy.post.create(
        community_id,
        name=title,
        url=url,
        body=body,
        nsfw=nsfw,
        honeypot=honeypot,
        language_id=language_id,
    )

    if not created:
        msg = (
            f"Sorry, cannot create post {title} in community_id={community_id}"
        )
        raise LemmyError(msg)

    return created


def create_event_post(
    event: Event,
    lemmy: Lemmy,
    community: str = apc_lb_conf.lemmy.community,
    honeypot: str | None = None,
    langcode: str | None = None,
    retries: int = 3,
) -> dict | None:
    """
    Create a Lemmy post using an event.

    When we don't have a link to the event, we upload the image to the Lemmy
    instance.
    """
    apc_lb_conf.lemmy.community = community

    # We post the image, if it not exists, the link to the event:
    _url = event.get_image_url()
    if _url is None:
        _url = event.get_event_url()
    for try_num in range(retries):
        try:
            return _create_post(
                lemmy,
                title=event.nice_title(LEMMY_MAX_TITLE_LENGTH),
                url=_url,
                body=event.get_content(),
                nsfw=event.NSFW if event.NSFW else False,
                community=community,
                honeypot=honeypot,
                langcode=langcode,
            )
        except Exception as err:
            warnings.warn(
                f"[{try_num}/{retries}] Error '{err=}/{type(err)=}' \
                creating post '{event}'.",
                stacklevel=2,
            )
            if try_num == retries:
                raise err
    msg = "This code cannot be executed. Contacts devs."
    raise LemmyError(msg)
