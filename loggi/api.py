import asyncio
import logging
import aiohttp

from defaults import AUTH_API_URL, LOGGING_API_URL
from exceptions import UnauthorizedException


class Auth:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

        self.__token = None

    async def login(self) -> None:
        logging.debug('Starting user login')
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

                logging.debug('User logined')

    def auth_credentials(self) -> dict[str, str]:
        logging.debug('Set auth credentials')
        return {'Authorization': f'Bearer {self.__token}'}

    async def refresh_token(self) -> str:
        logging.debug('Creating new token')
        if self.__token is None:
            raise UnauthorizedException('User is not logined.')

        async with aiohttp.ClientSession(headers=self.auth_credentials()) as session:
            url = f'{AUTH_API_URL}/refresh_token'

            async with session.get(url) as response:
                new_token = (await response.json())['token']
                logging.debug('Successful created new token')
                self.__token = new_token

    def get_token(self) -> str:
        if self.__token is None:
            raise UnauthorizedException('User is not logined')
        return self.__token


class LoggingAPI:
    def __init__(self, auth: Auth):
        self.auth = auth
        asyncio.run(auth.login())

    async def write(self, log: dict) -> None:
        """ Write log to remote server(Loggi) """
        
        logging.debug('Writing log to remote server')
        async with aiohttp.ClientSession(
            headers=self.auth.auth_credentials()
        ) as session:
            url = f'{LOGGING_API_URL}/write'
            print(self.auth.auth_credentials())

            async with session.post(url, json=log) as response:
                if (await response.json())['detail'] == 'Token expired':
                    logging.debug('Token expired')
                    await self.auth.refresh_token()
                    logging.debug('Write log to remote server again')
                    await self.write(log)
                elif response.status == 201:
                    logging.debug('Log successful writed')
                elif response.status == 401:
                    raise UnauthorizedException('Failed to log in')
