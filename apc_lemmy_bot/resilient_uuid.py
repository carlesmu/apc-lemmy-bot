#    Copyright (C) 2025 Carles Muñoz Gorriz <carlesmu@internautas.org>
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
apc_lemmy_bot resilient_uid module.

@author: Carles Muñoz Gorriz <carlesmu@internautas.org>
"""

import uuid

UUID_MAX_LENGTH = 32


class UUID(uuid.UUID):
    """
    A extended class of uuid.UUID.

    This is a proxy class for uuid.UUID that let us process malformed
    uuids with length greath than 32.

    """

    def __init__(
        self,
        hex: str | None = None,
        bytes: bytes | None = None,
        bytes_le: bytes | None = None,
        fields: tuple[int, int, int, int, int, int] | None = None,
        int: int | None = None,
        version: int | None = None,
        *,
        is_safe: uuid.SafeUUID = uuid.SafeUUID.unknown,
    ) -> None:
        """Initialize a UUID object."""
        if hex is not None:
            hex = hex.replace("urn:", "").replace("uuid:", "")
            hex = hex.strip("{}").replace("-", "")
            if len(hex) > UUID_MAX_LENGTH:
                hex = hex[(-1 * UUID_MAX_LENGTH) :]
        super().__init__(
            hex, bytes, bytes_le, fields, int, version, is_safe=is_safe
        )
