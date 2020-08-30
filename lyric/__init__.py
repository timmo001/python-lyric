"""Lyric: Init"""
from aiohttp import ClientError, ClientSession, ClientResponse
from asyncio import CancelledError, TimeoutError, get_event_loop
from datetime import datetime, timedelta
from typing import List

from .base import LyricBase
from .device import LyricDevice
from .location import LyricLocation
from .exceptions import LyricException, LyricAuthenticationException
from .const import BASE_URL


class Lyric(LyricBase):
    """Handles authentication refresh tokens."""

    def __init__(self, client: "LyricClient") -> None:
        """Initialize the token manager class."""
        self._client = client
        self._devices: List[LyricDevice] = None
        self._locations: List[LyricLocation] = None

    @property
    def devices(self) -> List[LyricDevice]:
        return self._devices

    @property
    def locations(self) -> List[LyricLocation]:
        return self._locations

    async def get_devices(self) -> None:
        """Get Devices."""
        response: ClientResponse = await self.client.get(
            f"{BASE_URL}/devices",
            headers={
                "Authorization": f"Basic {self.client.token_manager.access_token}",
            },
        )
        if response.status != 200:
            if response.status == 401 or response.status == 403:
                raise LyricAuthenticationException(response.status)
            else:
                raise LyricException(response.status)
        json = await response.json()

        self.logger.debug(json)

        self._devices = json

    async def get_locations(self) -> None:
        """Get Locations."""
        response: ClientResponse = await self.client.get(
            f"{BASE_URL}/locations",
            headers={
                "Authorization": f"Basic {self.access_token}",
            },
        )
        if response.status != 200:
            if response.status == 401 or response.status == 403:
                raise LyricAuthenticationException(response.status)
            else:
                raise LyricException(response.status)
        json = await response.json()

        self.logger.debug(json)

        self.locations = json
