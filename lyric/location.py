"""Location"""

from lyric.device import Device
from lyric.thermostat import Thermostat
from lyric.user import User
from lyric.waterleakdetector import WaterLeakDetector

class Location(object):
    """Store Location Information."""

    def __init__(self, locationId, lyric_api, local_time=False):
        """Initialize and setup Location class."""

        self._locationId = locationId
        self._lyric_api = lyric_api
        self._local_time = local_time

    def __repr__(self):
        """Print helpful debug information."""

        return "<%s: %s>" % (self.__class__.__name__, self._repr_name)

    @property
    def id(self):
        """Return id."""

        return self._locationId

    @property
    def locationId(self):
        """Return Location ID."""

        return self._locationId

    @property
    def location(self):
        """Return Location."""

        return self._lyric_api._location(self._locationId)

    @property
    def locationID(self):
        """Return Location ID."""

        return self.location.get("locationID")

    @property
    def name(self):
        """Return name."""

        return self.location.get("name")

    @property
    def _repr_name(self):
        """Return name."""

        return self.name

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

        return self._lyric_api._users(self._locationId)

    @property
    def _devices(self, forceGet=False):
        """Return devices."""

        return self._lyric_api._devices(self._locationId, forceGet)

    @property
    def _thermostats(self):
        """Return thermostats."""

        return self._lyric_api._devices_type("thermostats", self._locationId)

    @property
    def _waterLeakDetectors(self):
        """Return water leak dectectors."""

        return self._lyric_api._devices_type("waterLeakDetectors", self._locationId)

    @property
    def users(self):
        """Return Users."""

        return [
            User(user.get("userID"), self, self._lyric_api, self._local_time)
            for user in self._users
        ]

    @property
    def devices(self):
        """Return devices."""

        devices = []
        for device in self._devices:
            if device["deviceType"] == "Thermostat":
                devices.append(
                    Thermostat(
                        device["deviceID"], self, self._lyric_api, self._local_time
                    )
                )
            elif device["deviceType"] == "Water Leak Detector":
                devices.append(
                    WaterLeakDetector(
                        device["deviceID"], self, self._lyric_api, self._local_time
                    )
                )
            else:
                devices.append(
                    Device(device["deviceID"], self, self._lyric_api, self._local_time)
                )
        return devices

    @property
    def thermostats(self):
        """Return thermostats."""

        thermostats = []
        for device in self._devices:
            if device["deviceType"] == "Thermostat":
                thermostats.append(
                    Thermostat(
                        device["deviceID"], self, self._lyric_api, self._local_time
                    )
                )
        return thermostats

    @property
    def waterLeakDetectors(self):
        """Return water leak detectors."""

        waterLeakDetectors = []
        for device in self._devices:
            if device["deviceType"] == "Water Leak Detector":
                waterLeakDetectors.append(
                    WaterLeakDetector(
                        device["deviceID"], self, self._lyric_api, self._local_time
                    )
                )
        return waterLeakDetectors
