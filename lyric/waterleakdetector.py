"""Water Leak Detector"""
from lyric import lyricDevice


class WaterLeakDetector(lyricDevice):
    """Water Leak Detector Class."""

    @property
    def waterPresent(self):
        """Return water present."""

        return self.device.get("waterPresent")

    @property
    def currentSensorReadings(self):
        """Return current sensor reading."""

        return self.device.get("currentSensorReadings")

    @property
    def currentAlarms(self):
        """Return current alarms."""

        return self.device.get("currentAlarms")

    @property
    def lastCheckin(self):
        """Return last checkin."""

        return self.device.get("lastCheckin")

    @property
    def lastDeviceSettingUpdatedOn(self):
        """Return last device setting update on."""

        return self.device.get("lastDeviceSettingUpdatedOn")

    @property
    def batteryRemaining(self):
        """Return battery remaining."""

        return self.device.get("batteryRemaining")

    @property
    def isRegistered(self):
        """Return is registered."""

        return self.device.get("isRegistered")

    @property
    def hasDeviceCheckedIn(self):
        """Return has device checked in."""

        return self.device.get("hasDeviceCheckedIn")

    @property
    def isDeviceOffline(self):
        """Return is device offline."""

        return self.device.get("isDeviceOffline")

    @property
    def firstFailedAttemptTime(self):
        """Return first failed attempt time."""

        return self.device.get("firstFailedAttemptTime")

    @property
    def failedConnectionAttempts(self):
        """Return failed connection attempts."""

        return self.device.get("failedConnectionAttempts")

    @property
    def wifiSignalStrength(self):
        """Return wifi signal strength."""

        return self.device.get("wifiSignalStrength")

    @property
    def isFirmwareUpdateRequired(self):
        """Return is firmware update required."""

        return self.device.get("isFirmwareUpdateRequired")

    @property
    def time(self):
        """Return time."""

        return self.device.get("time")

    @property
    def deviceSettings(self):
        """Return device settings."""

        return self.device.get("deviceSettings")
