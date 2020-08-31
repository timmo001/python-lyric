"""Lyric: Location"""
from datetime import datetime, timedelta

from ..exceptions import LyricException, LyricAuthenticationException
from ..const import AUTH_URL, BASE_URL, TOKEN_URL
from ..device import LyricDevice
from ..thermostat import LyricThermostat
from ..waterleakdetector import LyricWaterLeakDetector
from ..user import LyricUser


class LyricLocation(object):
    """Store Location Information."""

    def __init__(self, client: "LyricClient", location_id: int):
        """Initialize and setup Location class."""
        self._client = client
        self._location_id = location_id

    @property
    def id(self):
        """Return id."""
        return self._location_id

    @property
    def locationId(self) -> int:
        """Return Location ID."""
        return self._location_id

    @property
    def location(self):
        """Return Location."""
        return self._location(self._location_id)

    @property
    def locationID(self):
        """Return Location ID."""
        return self.location.get("locationID")

    @property
    def name(self):
        """Return name."""
        return self.location.get("name")

    @property
    def streetAddress(self):
        """Return street address."""
        return self.location.get("streetAddress")

    @property
    def city(self):
        """Return city."""
        return self.location.get("city")

    @property
    def state(self):
        """Return state."""
        return self.location.get("state")

    @property
    def country(self):
        """Return country."""
        return self.location.get("country")

    @property
    def zipcode(self):
        """Return zipcode."""
        return self.location.get("zipcode")

    @property
    def timeZone(self):
        """Return timezone."""
        return self.location.get("timeZone")

    @property
    def daylightSavingTimeEnabled(self):
        """Return daylight savings time enabled."""
        return self.location.get("daylightSavingTimeEnabled")

    @property
    def geoFenceEnabled(self):
        """Return geofencing enabled."""
        return self.location.get("geoFenceEnabled")

    @property
    def geoFences(self):
        """Return geofences."""
        return self.location.get("geoFences")

    @property
    def geoFence(self, index=0):
        """Return specific geofence."""
        if self.geoFences and len(self.geoFences) >= index + 1:
            return self.geoFences[index]

    @property
    def geoOccupancy(self):
        """Return geo Occupancy."""
        if "geoOccupancy" in self.geoFence:
            return self.geoFence.get("geoOccupancy")

    @property
    def withInFence(self):
        """Return user in fence."""
        if "withinFence" in self.geoOccupancy:
            return self.geoOccupancy.get("withinFence")

    @property
    def outsideFence(self):
        """Return user out of fence."""
        if "outsideFence" in self.geoOccupancy:
            return self.geoOccupancy.get("outsideFence")

    @property
    def _users(self):
        """Return Users."""
        return self._users(self._location_id)

    @property
    def _devices(self, forceGet=False):
        """Return devices."""
        return self._devices(self._location_id, forceGet)

    @property
    def _thermostats(self):
        """Return thermostats."""
        return self._devices_type("thermostats", self._location_id)

    @property
    def _water_leak_detectors(self):
        """Return water leak dectectors."""
        return self._devices_type("water_leak_detectors", self._location_id)

    @property
    def users(self):
        """Return Users."""
        return [
            LyricUser(user.get("userID"), self, self._lyric_api, self._local_time)
            for user in self._users
        ]

    @property
    def devices(self):
        """Return devices."""
        devices = []
        for device in self._devices:
            if device["deviceType"] == "Thermostat":
                devices.append(
                    LyricThermostat(
                        device["deviceID"], self, self._lyric_api, self._local_time
                    )
                )
            elif device["deviceType"] == "Water Leak Detector":
                devices.append(
                    LyricWaterLeakDetector(
                        device["deviceID"], self, self._lyric_api, self._local_time
                    )
                )
            else:
                devices.append(
                    LyricDevice(
                        device["deviceID"], self, self._lyric_api, self._local_time
                    )
                )
        return devices

    @property
    def thermostats(self):
        """Return thermostats."""
        thermostats = []
        for device in self._devices:
            if device["deviceType"] == "Thermostat":
                thermostats.append(
                    LyricThermostat(
                        device["deviceID"], self, self._lyric_api, self._local_time
                    )
                )
        return thermostats

    @property
    def water_leak_detectors(self):
        """Return water leak detectors."""
        water_leak_detectors = []
        for device in self._devices:
            if device["deviceType"] == "Water Leak Detector":
                water_leak_detectors.append(
                    LyricWaterLeakDetector(
                        device["deviceID"], self, self._lyric_api, self._local_time
                    )
                )
        return water_leak_detectors
