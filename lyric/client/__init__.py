"""Lyric: Client"""
import async_timeout
import logging

from abc import abstractmethod
from asyncio import CancelledError, TimeoutError, get_event_loop
from aiohttp import ClientError, ClientSession, ClientResponse

from ..base import LyricBase
from ..exceptions import LyricException, LyricAuthenticationException
from .token_manager import LyricTokenManager


class LyricClient(LyricBase):
    """Client to handle API calls."""

    def __init__(self, session: ClientSession) -> None:
        """Initialize the client."""
        self.session = session
        self.token_manager = LyricTokenManager(self.session)

    @abstractmethod
    async def async_get_access_token(self) -> str:
        """Return a valid access token."""

    async def get(self, url: str, **kwargs) -> ClientResponse:
        """Make a GET request."""
        async with async_timeout.timeout(20, loop=get_event_loop()):
            response = await self.request(
                "GET",
                url,
                headers=f"Authorization: Basic {self._client.token_manager.access_token}",
                **kwargs,
            )
        if response.status != 200:
            if response.status == 401 or response.status == 403:
                raise LyricAuthenticationException(response.status)
            else:
                raise LyricException(response.status)
        return response

    async def post(self, url: str, **kwargs) -> ClientResponse:
        """Make a POST request."""
        async with async_timeout.timeout(20, loop=get_event_loop()):
            response = await self.request("POST", url, **kwargs)
        if response.status != 200:
            if response.status == 401 or response.status == 403:
                raise LyricAuthenticationException(response.status)
            else:
                raise LyricException(response.status)
        return response

    async def request(
        self, method: str in ["GET", "POST"], url: str, **kwargs
    ) -> ClientResponse:
        """Make a request."""
        headers = kwargs.get("headers")

        if headers is None:
            headers = {}
        else:
            headers = dict(headers)

        access_token = await self.async_get_access_token()
        headers["authorization"] = f"Bearer {access_token}"

        async with async_timeout.timeout(20, loop=get_event_loop()):
            return await self.session.request(
                method,
                url,
                **kwargs,
                headers=headers,
            )
