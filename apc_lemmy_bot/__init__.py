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
"""apc_lemmy_bot __init__ module."""

from dataclasses import dataclass

__app__: str = "apc_lemmy_bot"
__version__: str = "0.5.6"

LEMMY_MAX_TITLE_LENGTH: int = 199


@dataclass
class ApcLemmyBotSupabaseConf:
    """A data class for Supabase data conf."""

    url: str = ""  # Not initialized
    key: str = ""  # Not initialized
    base_event_url: str = ""  # Not initialized
    base_event_img_url: str = ""  # Not initialized


@dataclass
class ApcLemmyBotLemmyConf:
    """A data class for Lemmy instances conf."""

    instance: str = "https://lemmy.world"
    user: str = "roig"
    password: str = ""  # Not initialized
    community: str = "workingclasscalendar@lemmy.world"


@dataclass
class ApcLemmyBotConf:
    """A data class for apc_lemmy_conf."""

    supabase: ApcLemmyBotSupabaseConf
    lemmy: ApcLemmyBotLemmyConf
    database: str = "sqlite:///apc_database.db"
    delay: int = 5400  # seconds


# The configuration and shared data structure:
apc_lb_conf: ApcLemmyBotConf = ApcLemmyBotConf(
    ApcLemmyBotSupabaseConf(),
    ApcLemmyBotLemmyConf(),
)
