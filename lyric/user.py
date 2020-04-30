"""User"""


class User(object):
    """Class definition for User object."""

    def __init__(self, userId, location, lyric_api, local_time=False):
        """Configure User object."""

        self._location = location
        self._locationId = self._location.locationId
        self._userId = userId
        self._lyric_api = lyric_api
        self._local_time = local_time

    def __repr__(self):
        """Print out helpful debug."""

        return "<%s: %s>" % (self.__class__.__name__, self._repr_name)

    @property
    def id(self):
        """Return ID."""

        return self._userId

    @property
    def name(self):
        """Return name."""

        return self.username

    @property
    def _repr_name(self):
        """Return name."""

        return self.username

    @property
    def user(self):
        """Return user."""

        return self._lyric_api._user(self._locationId, self._userId)

    @property
    def userID(self):
        """Return userID."""

        return self.user.get("userID")

    @property
    def username(self):
        """Return username."""

        return self.user.get("username")

    @property
    def firstname(self):
        """Return firstname."""

        return self.user.get("firstname")

    @property
    def lastname(self):
        """Return lastname."""

        return self.user.get("lastname")

    @property
    def created(self):
        """Return created."""

        return self.user.get("created")

    @property
    def deleted(self):
        """Return deleted."""

        return self.user.get("deleted")

    @property
    def activated(self):
        """Return activated."""

        return self.user.get("activated")

    @property
    def connectedHomeAccountExists(self):
        """Return connected home account exists."""

        return self.user.get("connectedHomeAccountExists")
