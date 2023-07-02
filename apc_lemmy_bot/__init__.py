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
apc_lemmy_bot __init__ module.

@author: Carles Muñoz Gorriz <carlesmu@internautas.org>
"""

from dataclasses import dataclass

from typing import Optional

__all__ = ["event", "lemmy"]

__app__: str = "apc_lemmy_bot"
__version__: str = "0.1.1"

LEMMY_MAX_TITLE_LENGTH: int = 199


@dataclass
class ApcLemmyBotSupabaseConf:
    """Dataclass for supabase data conf."""

    url: Optional[str] = None
    key: Optional[str] = None
    base_event_url: Optional[str] = None
    base_event_img_url: Optional[str] = None


@dataclass
class ApcLemmyBotLemmyConf:
    """Dataclass for Lemmy instances conf."""

    instance: Optional[str] = None
    user: Optional[str] = None
    password: Optional[str] = None
    community: Optional[str] = None


@dataclass
class ApcLemmyBotDatabaseConf:
    """Dataclass for  the database conf."""

    url: Optional[str] = None


@dataclass
class ApcLemmyBotConf:
    """Dataclass for apc_lemmy_conf."""

    supabase: ApcLemmyBotSupabaseConf
    lemmy: ApcLemmyBotLemmyConf
    database: ApcLemmyBotDatabaseConf
    delay: int = 5400  # seconds


apc_lb_conf = ApcLemmyBotConf(
    ApcLemmyBotSupabaseConf(), ApcLemmyBotLemmyConf(), ApcLemmyBotDatabaseConf()
)
