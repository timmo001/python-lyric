"""Example usage of Lyric"""
import asyncio

from aiohttp import ClientSession

from lyric.client import LyricClient
from lyric.exceptions import LyricException, LyricAuthenticationException
from lyric.client.token_manager import LyricTokenManager

CLIENT_ID = "abc123"
CODE = "123456"
REDIRECT_URL = "http://192.168.1.123:8123/auth/lyric/callback"


async def example():
    """Example usage of Lyric."""
    async with ClientSession() as session:
        try:
            client = LyricClient(session)
            await client.token_manager.async_update_token(CLIENT_ID, CODE, REDIRECT_URL)
            print(client.token_manager.token)
            print(client.token_manager.token_expires)
            print(client.token_manager.token_valid)
        except LyricAuthenticationException as err:
            print(f"Lyric authentication error: {err}")
        except LyricException as err:
            print(f"Lyric error: {err}")


asyncio.get_event_loop().run_until_complete(example())
