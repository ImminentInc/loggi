import asyncio
from api import LoggingAPI, Auth
from logger import Loggi, on_debug_mode


on_debug_mode()
auth = Auth(username='string', password='string')
log_api = LoggingAPI(auth)

logger = Loggi(project_name='Bot1', api=log_api)


async def main():
    try:
        ee
    except Exception as e:
        await logger.error(e)

print(asyncio.run(main()))
