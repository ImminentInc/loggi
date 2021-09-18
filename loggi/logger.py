import logging
import traceback
import sys

from types import FrameType
from typing import Optional

from api import LoggingAPI
from debug_details.all_info import debug_info

from inspect import currentframe  # For get details about exception/info
import asyncio


class Singleton(type):
	_instances = dict()

	def __call__(self, *args, **kwagrs):
		if self not in self._instances:
			self._instances[self] = super(
				Singleton, self
			).__call__(*args, **kwagrs)
		return self._instances[self]
		

class Loggi(metaclass=Singleton):
	def __init__(
		self,
		project_name: str, 
		api: LoggingAPI,
		additional_info: Optional[dict] = None
	):
		self.__project_name = project_name
		self.__api = api
		
		if isinstance(additional_info, type(None)) \
		or isinstance(additional_info, type(dict)):
			self.__additional_info = additional_info
		else:
			raise TypeError('additional_info must be type dict or None')

	async def __log(
		self, 
		message: str, 
		level: str, 
		caller: FrameType, 
	) -> None:
		from dataclasses import asdict

		logging.debug('Log message')
		
		details = debug_info(
			self.__project_name, 
			level, 
			message, 
			caller, 
			self.__additional_info
		)
		
		await self.__api.write(asdict(details))

	async def debug(self, message):
		caller = currentframe().f_back
		level = 'DEBUG'
		
		await self.__log(message, level, caller)

	async def info(self, message):
		caller = currentframe().f_back
		level = 'INFO'

		await self.__log(message, level, caller)

	async def warning(self, message):
		caller = currentframe().f_back
		level = 'WARNING'

		await self.__log(message, level, caller)

	async def error(self, message):
		caller = currentframe().f_back
		level = 'ERROR'

		await self.__log(message, level, caller)

	async def critical(self, message):
		caller = currentframe().f_back  
		level = 'CRITICAL'

		await self.__log(message, level, caller)

	def catch_exception(self, func):
		""" Wrapper for catch exception on functions/methods """
		def catch(*args, **kwargs):
			try:
				return func(*args, **kwargs)
			except Exception:
				caller = currentframe().f_back
				asyncio.run(self.__log('Exception', level='ERROR', caller=caller))
		return catch

	def set_additional_info(self, data: dict):
		logging.debug('Setting additional info')
		if isinstance(data, type(None)) \
		or isinstance(data, type(dict)):
			self.__additional_info = data
		else:
			raise TypeError('additional_info must be type dict or None')

	def get_project_name(self) -> str:
		return self.__project_name


def on_debug_mode():
	logging.basicConfig(level=logging.DEBUG)
