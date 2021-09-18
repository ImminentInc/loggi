import psutil
import logging

from debug_details.dataclasses_ import SystemInfo
from platform import uname

from typing import Any


def get_sys_info() -> list:
    logging.debug('Getting system info')
    return list(uname())[:5]


def get_cpu_usage() -> Any:
    logging.debug('Getting cpu usage')
    return psutil.cpu_percent()


def get_ram_usage():
    logging.debug('Getting ram usage')
    return psutil.virtual_memory().percent
 

def get_used_memory() -> int:
    logging.debug('Getting used memory')
    hdd = psutil.disk_usage('/')
    return (hdd.used // (1024**3))


def get_total_memory() -> int:
    logging.debug('Getting total memory')
    hdd = psutil.disk_usage('/')
    return (hdd.total // (1024**3))


def system_details() -> SystemInfo:
    logging.debug('Getting system details')
    return SystemInfo(
        *get_sys_info(),
        cpu_usage=get_cpu_usage(),
        ram_usage=get_ram_usage(),
        memory_total=get_total_memory(),
        memory_used=get_used_memory()
    )
