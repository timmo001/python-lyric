"""Thermostat"""


class Thermostat(lyricDevice):
    """Thermostat Class."""

    def updateThermostat(
        self,
        mode=None,
        heatSetpoint=None,
        coolSetpoint=None,
        AutoChangeover=None,
        thermostatSetpointStatus=None,
        nextPeriodTime=None,
    ):
        """Update Themostate."""

        if mode is None:
            mode = self.operationMode
        if heatSetpoint is None:
            heatSetpoint = self.heatSetpoint
        if coolSetpoint is None:
            coolSetpoint = self.coolSetpoint

        if "thermostatSetpointStatus" in self.changeableValues:
            if thermostatSetpointStatus is None:
                thermostatSetpointStatus = self.thermostatSetpointStatus

        if "autoChangeoverActive" in self.changeableValues:
            if AutoChangeover is None:
                AutoChangeover = self.changeableValues.get("autoChangeoverActive")

        data = {
            "mode": mode,
            "heatSetpoint": heatSetpoint,
            "coolSetpoint": coolSetpoint,
        }

        if "thermostatSetpointStatus" in self.changeableValues:
            data["thermostatSetpointStatus"] = thermostatSetpointStatus
        if "autoChangeoverActive" in self.changeableValues:
            data["autoChangeoverActive"] = AutoChangeover
        if nextPeriodTime is not None:
            data["nextPeriodTime"] = nextPeriodTime

        self._set("devices/thermostats/" + self._deviceId, data=data)

    def updateFan(self, mode):
        """Update Fan."""

        if mode is None:
            mode = self.fanMode

        self._set("devices/thermostats/" + self._deviceId + "/fan", data={"mode": mode})

    @property
    def away(self):
        """Get away status."""

        if self.scheduleType == "Geofence":
            if self._location.geoFenceEnabled:
                return self._location.withInFence == 0
        elif self.scheduleType == "Timed" and self.scheduleSubType == "NA":
            # North America
            return self.currentSchedulePeriod.get("period") == "Away"
        elif self.scheduleType == "Timed" and self.scheduleSubType == "EMEA":
            # Europe, Middle-East, Africa
            return self.currentSchedulePeriod.get("period") == "P3"

    @property
    def vacationHold(self):
        """Return vacation hold."""

        return self.device.get("vacationHold").get("enabled")

    @property
    def where(self):
        """Return location."""

        return self._location.name

    @property
    def units(self):
        """Return units."""

        return self.device.get("units")

    @property
    def indoorTemperature(self):
        """Return indoor temperature."""

        return self.device.get("indoorTemperature")

    @property
    def heatSetpoint(self):
        """Return Heat Setpoint."""

        return self.changeableValues.get("heatSetpoint")

    @property
    def coolSetpoint(self):
        """Return Cool Setpoint."""

        return self.changeableValues.get("coolSetpoint")

    @property
    def thermostatSetpointStatus(self):
        """Return thermostat Set Point."""

        return self.changeableValues.get("thermostatSetpointStatus")

    def set_thermostatSetpointStatus(self, thermostatSetpointStatus):
        """Set Thermostat."""

        self.updateThermostat(thermostatSetpointStatus=thermostatSetpointStatus)

    def thermostatSetpointHoldUntil(
        self, nextPeriodTime, heatSetpoint=None, coolSetpoint=None
    ):
        """Set thermostat hold until point."""

        if nextPeriodTime is None:
            raise ValueError("nextPeriodTime is required")
        self.updateThermostat(
            heatSetpoint=heatSetpoint,
            coolSetpoint=coolSetpoint,
            thermostatSetpointStatus="HoldUntil",
            nextPeriodTime=nextPeriodTime,
        )

    @property
    def nextPeriodTime(self):
        """Return next period time."""

        return self.changeableValues.get("nextPeriodTime")

    @property
    def auto_changeover(self):
        """Return auto change over."""

        return self.changeableValues.get("AutoChangeover")

    @property
    def operationMode(self):
        """Return operation mode."""

        return self.changeableValues.get("mode")

    def set_operationMode(self, mode):
        """Set operation mode."""

        self.updateThermostat(mode=mode)

    @property
    def temperatureSetpoint(self):
        """Return temperature set point."""

        if self.operationMode == "Heat":
            return self.changeableValues.get("heatSetpoint")
        else:
            return self.changeableValues.get("coolSetpoint")

    def set_temperatureSetpoint(self, setpoint):
        """Set temperature set point."""

        if self.thermostatSetpointStatus in ["NoHold", "HoldUntil"]:
            thermostatSetpointStatus = "TemporaryHold"
        else:
            thermostatSetpointStatus = self.thermostatSetpointStatus

        if isinstance(setpoint, tuple):
            self.updateThermostat(
                coolSetpoint=setpoint[0],
                heatSetpoint=setpoint[1],
                thermostatSetpointStatus=thermostatSetpointStatus,
            )
        elif self.operationMode == "Cool":
            self.updateThermostat(
                coolSetpoint=setpoint, thermostatSetpointStatus=thermostatSetpointStatus
            )
        elif self.operationMode == "Heat":
            self.updateThermostat(
                heatSetpoint=setpoint, thermostatSetpointStatus=thermostatSetpointStatus
            )

    @property
    def can_heat(self):
        """Return can heat."""

        return "Heat" in self.allowedModes

    @property
    def can_cool(self):
        """Return can cool."""

        return "Cool" in self.allowedModes

    @property
    def has_fan(self):
        """Return has fan."""

        return True

    @property
    def outdoorTemperature(self):
        """Return outdoor temperature."""

        return self.device.get("outdoorTemperature")

    @property
    def allowedModes(self):
        """Return allowed modes."""

        return self.device.get("allowedModes")

    @property
    def deadband(self):
        """Return deadband."""

        return self.device.get("deadband")

    @property
    def hasDualSetpointStatus(self):
        """Return has dual set points."""

        return self.device.get("hasDualSetpointStatus")

    @property
    def minHeatSetpoint(self):
        """Return min heat set point."""

        return self.device.get("minHeatSetpoint")

    @property
    def maxHeatSetpoint(self):
        """Return max heat setpoint."""

        return self.device.get("maxHeatSetpoint")

    @property
    def minCoolSetpoint(self):
        """Return min cool set point."""

        return self.device.get("minCoolSetpoint")

    @property
    def maxCoolSetpoint(self):
        """Return max cool setpoint."""

        return self.device.get("maxCoolSetpoint")

    @property
    def maxSetpoint(self):
        """Return max setpoint."""

        if self.can_heat:
            return self.maxHeatSetpoint
        else:
            return self.maxCoolSetpoint

    @property
    def minSetpoint(self):
        """Return min setpoint."""

        if self.can_cool:
            return self.minCoolSetpoint
        else:
            return self.minHeatSetpoint

    @property
    def changeableValues(self):
        """Return changeable values."""

        return self.device.get("changeableValues")

    @property
    def operationStatus(self):
        """Return operation status."""

        return self.device.get("operationStatus")

    @property
    def smartAway(self):
        """Return smart away."""

        return self.device.get("smartAway")

    @property
    def indoorHumidity(self):
        """Return indoor humidity."""

        return self.device.get("indoorHumidity")

    @property
    def indoorHumidityStatus(self):
        """Return indoor humidity status."""

        return self.device.get("indoorHumidityStatus")

    @property
    def isAlive(self):
        """Return is alive."""

        return self.device.get("isAlive")

    @property
    def isUpgrading(self):
        """Return is upgrading."""

        return self.device.get("isUpgrading")

    @property
    def isProvisioned(self):
        """Return is provisioned."""

        return self.device.get("isProvisioned")

    @property
    def settings(self):
        """Return settings."""

        return self.device.get("settings")

    @property
    def fanMode(self):
        """Return fan mode."""

        if (
            self.settings
            and "fan" in self.settings
            and "changeableValues" in self.settings.get("fan")
        ):
            return self.settings.get("fan").get("changeableValues").get("mode")

    def set_fanMode(self, mode):
        """Set fan mode."""

        self.updateFan(mode)

    @property
    def macID(self):
        """Return MAC id."""

        return self.device.get("macID")

    @property
    def scheduleStatus(self):
        """Return schedule status."""

        return self.device.get("scheduleStatus")

    @property
    def allowedTimeIncrements(self):
        """Return allowed time increment."""

        return self.device.get("allowedTimeIncrements")

    @property
    def thermostatVersion(self):
        """Return thermostat version."""

        return self.device.get("thermostatVersion")

    @property
    def isRegistered(self):
        """Return is registered."""

        return self.device.get("isRegistered")

    @property
    def devicesettings(self):
        """Return device settings."""

        return self.device.get("devicesettings")

    @property
    def displayedOutdoorHumidity(self):
        """Return outdoor humidity."""

        return self.device.get("displayedOutdoorHumidity")

    @property
    def currentSchedulePeriod(self):
        """Return scheduled period."""

        return self.device.get("currentSchedulePeriod")

    @property
    def scheduleCapabilities(self):
        """Return schedule capabilities."""

        return self.device.get("scheduleCapabilities")

    @property
    def scheduleType(self):
        """Return schedule type."""

        if (
            "scheduleType" in self.device
            and "scheduleType" in self.device["scheduleType"]
        ):
            return self.device.get("scheduleType").get("scheduleType")
        elif "schedule" in self.device and "scheduleType" in self.device["schedule"]:
            return self.device.get("schedule").get("scheduleType")

    @property
    def scheduleSubType(self):
        """Return schedule subtype."""

        return self.device.get("scheduleType").get("scheduleSubType")
