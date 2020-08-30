"""Lyric: Device"""


class Device(lyricDevice):
    """Device class."""

    @property
    def unknownType(self):
        """Return unknown type."""
        return True

    def properties(self):
        """Return properties."""
        return self.device
