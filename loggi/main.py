# from loggi import logger, api


# auth = api.Auth('illya', 'illya')
# api = api.LoggingAPI(auth)

# logging = logger.Logger(api)
# logging.debug('hello')




# from api import Auth
# import asyncio
# import time

# auth = Auth(username='string', password='string')

# asyncio.run(auth.login())
# print(auth.get_token())

# print('___')
# time.sleep(5)
# asyncio.run(auth.refresh_token())
# print(auth.get_token())



from logger import Loggi

logger = Loggi('aa')
logger.getLogger('aa')
print(logger.info('debug'))