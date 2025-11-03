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
from typing import Any


class UUID(uuid.UUID):
    """
    A extended class of uuid.UUID.

    This is a proxy class for uuid.UUID that let us process malformed
    uuids with length greath than 32.

    """

    _append_hex = ""

    def __init__(
        self,
        hex=None,
        bytes=None,
        bytes_le=None,
        fields=None,
        int=None,
        version=None,
        *,
        is_safe=uuid.SafeUUID.unknown,
    ) -> None:
        """Initialize a UUID object."""
        if hex is not None:
            hex = hex.replace("urn:", "").replace("uuid:", "")
            hex = hex.strip("{}").replace("-", "")
            if len(hex) > 32:  # noqa: PLR2004
                self._append_hex = hex[:-32]
                hex = hex[-32:]
        super().__init__(
            hex, bytes, bytes_le, fields, int, version, is_safe=is_safe
        )

    def __str__(self) -> str:
        """UUID string representation."""
        hex = f"{self.int:032x}"
        return f"{self._append_hex}{hex[:8]}-{hex[8:12]}-{hex[12:16]}-{hex[16:20]}-{hex[20:]}"

    def __getattribute__(self, name) -> Any:
        """Get an attribute."""
        if name == "hex":
            return "{}{}".format(
                object.__getattribute__(self, "_append_hex"),
                super().__getattribute__("hex"),
            )
        return object.__getattribute__(self, name)

    def __setattr__(self, name, value) -> None:
        """Set an attribute."""
        if name == "_append_hex":
            # we need object because super is inmutable
            object.__setattr__(self, name, value)
        else:
            super().__setattr__(name, value)
