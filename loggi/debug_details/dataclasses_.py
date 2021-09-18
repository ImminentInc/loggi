from dataclasses import dataclass
from typing import Optional, Union


@dataclass(frozen=True)
class SystemInfo:
    os: str
    nodename: str
    release: str
    version: str

    system_bits: str
    cpu_usage: int
    ram_usage: int

    memory_total: int
    memory_used: int


@dataclass
class Log:
    level: str
    level_number: int

    func_name: str
    path_to_file: str
    filename: str
    line: int

    global_vars: dict
    
    message: str
    created: str

    additional_info: Union[dict[Union[str, int], Union[str, int]], None]
    traceback: Optional[list] = None


@dataclass
class AllLogInfo:
    project_name: str
    log: Log
    system_info: SystemInfo
