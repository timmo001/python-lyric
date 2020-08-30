"""Lyric: Token"""
import async_timeout
import datetime
import logging

from asyncio import CancelledError, TimeoutError, get_event_loop
from aiohttp import ClientError, ClientSession

from .common.exceptions import LyricException, LyricAuthenticationException

_LOGGER = logging.getLogger(__name__)


class LyricToken(LyricBase):
    """Handles authentication refresh tokens."""

    def __init__(self) -> None:
        """Initialize the client."""
        self._token = None
        self._token_expires = None

    @property
    def token(self) -> str:
        """Return the current token."""
        return self._token

    @property
    def token_expires(self) -> DateTime:
        """Return the current token expiration."""
        return self._token_expires

    @property
    def token_valid(self) -> bool:
        """Is the current token valid?"""
        return self.token_expires < datetime.utcnow() - datetime.timedelta(seconds=30)

    async def async_update_token(self) -> bool:
        """Update the current token."""
        return True
