"""Library to restfully handle Honeywell Home Assistant API calls."""

import logging
import os
import time

import asyncio
from aiohttp import ClientSession, ClientResponse
import urllib.parse

from . import Auth, Location

_LOGGER = logging.getLogger(__name__)

BASE_URL = "https://api.honeywell.com/v2/"
AUTHORIZATION_BASE_URL = "https://api.honeywell.com/oauth2/authorize"
TOKEN_URL = "https://api.honeywell.com/oauth2/token"
REFRESH_URL = TOKEN_URL


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

    def __enter__(self):
        """Return Self."""

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Return exit."""

        return False

    async def aiohttp_get_session(self) -> ClientSession:
        """Setup session."""
        async with ClientSession() as session:
            return await session

    async def aiohttp_get(
        self, session: ClientSession, url: str, client_id: str, client_secret: str,
    ) -> ClientResponse:
        """Get request."""
        async with session.get(url, client_id, client_secret) as response:
            return await response

    async def aiohttp_post(
        self,
        session: ClientSession,
        url: str,
        client_id: str,
        client_secret: str,
        json: dict,
    ) -> ClientResponse:
        """Get request."""
        async with session.get(url, client_id, client_secret, json) as response:
            return await response

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
        response = await self.aiohttp_get(
            self._session, url, self._client_id, self._client_secret,
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
            self._session, url, self._client_id, self._client_secret, json,
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
