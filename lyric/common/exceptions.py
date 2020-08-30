"""Lyric: Exceptions"""


class LyricException(BaseException):
    """Raise this when something is off."""


class LyricAuthenticationException(AIOGitHubAPIException):
    """Raise this when there is an authentication issue."""
