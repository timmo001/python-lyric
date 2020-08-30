"""Lyric: Token"""
from aiohttp import ClientError, ClientSession, ClientResponse
from asyncio import CancelledError, TimeoutError, get_event_loop
from datetime import datetime, timedelta

from ..base import LyricBase
from ..exceptions import LyricException, LyricAuthenticationException
from ..const import AUTH_URL, BASE_URL, TOKEN_URL


class LyricTokenManager(LyricBase):
    """Handles authentication refresh tokens."""

    def __init__(self, client: "LyricClient") -> None:
        """Initialize the token manager class."""
        self._client = client
        self._access_token = None
        self._refresh_token = None
        self._expires_in = datetime.now()

    @property
    def access_token(self) -> str:
        """Return the current token."""
        return self._access_token

    @property
    def refresh_token(self) -> str:
        """Return the current token."""
        return self._refresh_token

    @property
    def expires_in(self) -> datetime:
        """Return the current token expiration."""
        return self._expires_in

    @property
    def valid(self) -> bool:
        """Is the current token valid?"""
        return self._token_expires > datetime.now()

    async def async_update_token(
        self, client_id: str, code: str, redirect_url: str
    ) -> None:
        """Update the current token."""
        auth_response: ClientResponse = await self._client.post(
            TOKEN_URL,
            headers={
                "Authorization": f"Basic {self.access_token}",
                "Content-Type": "application/x-www-form-urlencoded",
            },
            data=f"grant_type=authorization_code&code={code}&redirect_uri={redirect_url}",
        )
        if auth_response.status != 200:
            raise LyricAuthenticationException(auth_response.status)
        json = await auth_response.json()

        self.logger.debug(f"Auth - JSON: {json}")

        self._access_token = json["access_token"]
        self._refresh_token = json["refresh_token"]
        self._expires_in = timedelta(seconds=json["expires_in"])
