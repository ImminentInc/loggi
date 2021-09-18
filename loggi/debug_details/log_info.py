import sys
import logging
import traceback

from types import FrameType

from typing import Union, Optional
from enum import Enum

from datetime import datetime
from inspect import Traceback, getframeinfo

from debug_details.dataclasses_ import Log


class LevelNumbers(Enum):
    DEBUG = 20
    INFO = 30
    WARNING = 40
    ERROR = 50
    CRITICAL = 60

    @staticmethod
    def get_level_number(level_: str) -> int:
        logging.debug('Getting level number by name level')
        for level in LevelNumbers:
            if level.name == level_:
                level_number = level.value
        return level_number


def convert_global_vars_value_to_str(
    frame_caller: FrameType
) -> dict[str, Union[str, int, type]]:
    """
        Convert objects to str sample:
        <api.LoggingAPI object at 0x7fb4e8fae550> 
        to '<api.LoggingAPI object at 0x7fb4e8fae550>'
    """
    logging.debug('Converting objects to str')
    global_vars = frame_caller.f_globals
    for var in global_vars:
        global_vars[var] = str(global_vars[var])
    return global_vars


def get_line_exception(exception_info) -> int:
    logging.debug('Getting line exception')
    return exception_info[2].tb_lineno 


def get_exception_message(exception_info) -> str:
    logging.debug('Getting exception message')
    type_, value, *some = exception_info  
    exc_type = str(type_).removeprefix("<class '").removesuffix("'>")
    return f'{exc_type}: {value}'


def get_line_log_called(caller: Traceback) -> int:
    logging.debug('Getting log call line')
    return caller.lineno


def is_exception(exception_info) -> bool:
    if any(exception_info):
        return True
    return False


def get_traceback(exception_info: tuple) -> list:
    return traceback.format_exception(*exception_info)


def log_details(
    level: str, 
    message: str, 
    frame_caller, 
    additional_info: Optional[dict] = None
) -> dict[str, Union[str, int]]:

    caller = getframeinfo(frame_caller)
    exception_info = sys.exc_info()

    global_vars = convert_global_vars_value_to_str(frame_caller)

    if is_exception(exception_info):
        logging.debug('Message is exception')
        line = get_line_exception(exception_info)
        message = get_exception_message(exception_info)
        traceback_ = get_traceback(exception_info)
    else:
        logging.debug('Message is simple log')
        line = get_line_log_called(caller)
        traceback_ = None
    
    logging.debug('Generating log info')
    return Log(
        level=level,
        level_number=LevelNumbers.get_level_number(level),

        func_name=caller.function, 
        path_to_file=caller.filename,
        filename=caller.filename.split('/')[-1],  
        line=line,

        global_vars=global_vars,
        
        traceback=traceback_,
        message=str(message),
        created=datetime.now().strftime('%D:%H %M'),

        additional_info=additional_info
    )
