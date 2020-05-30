"""Library to restfully handle Honeywell Home Assistant API calls."""

import logging
import os
import time

import asyncio
from abc import ABC, abstractmethod
from aiohttp import ClientSession, ClientResponse
import urllib.parse

from lyric.location import Location

_LOGGER = logging.getLogger(__name__)

BASE_URL = "https://api.honeywell.com/v2/"
AUTHORIZATION_BASE_URL = "https://api.honeywell.com/oauth2/authorize"
TOKEN_URL = "https://api.honeywell.com/oauth2/token"


class Lyric(object):
    """Lyric Class."""

    async def __init__(
        self, client_id, client_secret, token, local_time=False,
    ):
        """Intializes and configures the Lyric class."""

        self._session = await self.aiohttp_get_session()
        self._client_id = client_id
        self._client_secret = client_secret
        self._token = token
        self._local_time = local_time

        async with ClientSession() as session:
            self._auth = Auth(session, TOKEN_URL, token)

    def __enter__(self):
        """Return Self."""

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Return exit."""

        return False

    @property
    def token(self):
        """Return token."""

        return self._token

    async def _get(self, endpoint, **params):
        """Lyric get request method."""

        params["apikey"] = self._client_id
        query_string = urllib.parse.urlencode(params)
        url = BASE_URL + endpoint + "?" + query_string
        # try:
        response = await self._auth.request(
            "GET", url, client_id=self._client_id, client_secret=self._client_secret,
        )
        return response.json()
        # except requests.HTTPError as e:
        #     _LOGGER.error("HTTP Error Lyric API: %s" % e)
        #     if e.response.status_code == 401:
        #         self._lyricReauth()
        # except requests.exceptions.RequestException as e:
        #     # print("Error Lyric API: %s with data: %s" % (e, data))
        #     _LOGGER.error("Error Lyric API: %s" % e)

    async def _post(self, endpoint, json, **params):
        """Lyric post request method."""

        params["apikey"] = self._client_id
        query_string = urllib.parse.urlencode(params)
        url = BASE_URL + endpoint + "?" + query_string
        # try:
        response = await self.aiohttp_post(
            "POST", url, self._client_id, self._client_secret, json=json,
        )
        return response.status_code
        # except requests.HTTPError as e:
        #     _LOGGER.error("HTTP Error Lyric API: %s" % e)
        #     if e.response.status_code == 401:
        #         self._lyricReauth()
        # except requests.exceptions.RequestException as e:
        #     # print("Error Lyric API: %s with data: %s" % (e, data))
        #     _LOGGER.error("Error Lyric API: %s with data: %s" % (e, data))

    async def _location(self, locationId):
        """Return location."""

        for location in await self._get_locations():
            if location.get("locationID") == locationId:
                return location

    async def _get_locations(self):
        """Return locations."""

        return await self._get("locations")

    def _user(self, locationId, userId):
        """Return user."""

        for user in self._users(locationId):
            if user.get("userID") == userId:
                return user

    def _users(self, locationId):
        """Return users."""

        value = self._location(locationId).get("users")
        return value

    def _device(self, locationId, deviceId):
        """Return device."""

        for device in self._devices(locationId):
            if device.get("deviceID") == deviceId:
                return device

    def _devices(self, locationId, forceGet=False):
        """Return devices."""

        return self._location(locationId).get("devices")

    async def _device_type(self, locationId, deviceType, deviceId):
        """Return devices of a specific type."""

        for device in await self._devices_type(deviceType, locationId):
            if device.get("deviceID") == deviceId:
                return device

    async def _devices_type(self, deviceType, locationId):
        """Return device type."""

        return await self._get("devices/" + deviceType, locationId=locationId)

    async def get_locations(self):
        """Return locations."""

        return [
            Location(location["locationID"], self, self._local_time)
            for location in await self._get_locations()
        ]


class lyricDevice(object):
    """Class definition for Lyric devices."""

    def __init__(self, deviceId, location, lyric_api, local_time=False):
        """Intializes and configures lyricDevice class."""

        self._deviceId = deviceId
        self._location = location
        self._locationId = location.locationId
        self._lyric_api = lyric_api
        self._local_time = local_time

    def __repr__(self):
        """Debug string representation."""

        return "<%s: %s>" % (self.__class__.__name__, self._repr_name)

    def _set(self, endpoint, data, **params):
        """Setter Magic Method."""

        params["locationId"] = self._location.locationId
        print(self._lyric_api._post(endpoint, data, **params))

    @property
    def id(self):
        """Return id."""

        return self._deviceId

    @property
    def device(self):
        """Return device."""

        return self._lyric_api._device(self._locationId, self._deviceId)

    @property
    def name(self):
        """Return Name."""

        if "name" in self.device:
            return self.device.get("name")
        else:
            return self.userDefinedDeviceName

    @property
    def _repr_name(self):
        """Return User Defined Name."""

        return self.userDefinedDeviceName

    @property
    def deviceClass(self):
        """Return class."""

        return self.device.get("deviceClass")

    @property
    def deviceType(self):
        """Return Device Type."""

        return self.device.get("deviceType")

    @property
    def deviceID(self):
        """Return Device ID."""

        return self.device.get("deviceID")

    @property
    def userDefinedDeviceName(self):
        """Return User Defined Name."""

        return self.device.get("userDefinedDeviceName")


class Auth(AbstractAuth):
    def __init__(self, websession: ClientSession, host: str, token_manager):
        """Initialize the auth."""
        super().__init__(websession, host)
        self.token_manager = token_manager

    async def async_get_access_token(self) -> str:
        """Return a valid access token."""
        if self.token_manager.is_token_valid():
            return self.token_manager.access_token

        await self.token_manager.fetch_access_token()
        await self.token_manager.save_access_token()

        return self.token_manager.access_token


class AbstractAuth(ABC):
    """Abstract class to make authenticated requests."""

    def __init__(self, websession: ClientSession, host: str):
        """Initialize the auth."""
        self.websession = websession
        self.host = host

    @abstractmethod
    async def async_get_access_token(self) -> str:
        """Return a valid access token."""

    async def request(self, method, url, **kwargs) -> ClientResponse:
        """Make a request."""
        headers = kwargs.get("headers")

        if headers is None:
            headers = {}
        else:
            headers = dict(headers)

        access_token = await self.async_get_access_token()
        headers["authorization"] = f"Bearer {access_token}"

        return await self.websession.request(
            method, f"{self.host}/{url}", **kwargs, headers=headers,
        )
