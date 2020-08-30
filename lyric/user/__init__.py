"""Lyric: User"""


class LyricUser(object):
    """Class definition for User object."""

    def __init__(
        self, client: "LyricClient", location: "LyricLocation", user: "LyricUser"
    ):
        """Configure User object."""
        self._client = client
        self._location = location
        self._user = user

    @property
    def id(self):
        """Return ID."""
        return self._userId

    @property
    def name(self):
        """Return name."""
        return self.username

    @property
    def user(self):
        """Return user."""
        return self._user

    @property
    def user_id(self):
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
    def connected_home_account_exists(self):
        """Return connected home account exists."""
        return self.user.get("connectedHomeAccountExists")
