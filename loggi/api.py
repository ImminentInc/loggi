import asyncio
import aiohttp

from config import AUTH_API_URL, LOGGING_API_URL
from exceptions import UnauthorizedException


class Auth:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

        self.__token = None

    async def login(self) -> None:
        async with aiohttp.ClientSession() as session:
            url = f'{AUTH_API_URL}/login'

            async with session.post(
                url, 
                json={
                    'username': self.username, 
                    'password': self.password
                }
            ) as response:
                if response.status == 401:  # Unauthorized, user does not exists
                    error_detail = (await response.json())['detail']
                    raise UnauthorizedException(error_detail)
                self.__token = (await response.json())['token']

    def auth_credentials(self) -> dict[str, str]:
        return {'Authorization': f'Bearer {self.__token}'}

    async def refresh_token(self) -> str:
        if self.__token is None:
            raise UnauthorizedException('User is not logined.')

        async with aiohttp.ClientSession(headers=self.auth_credentials()) as session:
            url = f'{AUTH_API_URL}/refresh_token'

            async with session.get(url) as response:
                new_token = (await response.json())['token']
                self.__token = new_token
        return new_token

    def get_token(self) -> str:
        if self.__token is None:
            raise UnauthorizedException('User is not logined')
        return self.__token


# class LoggingAPI:
