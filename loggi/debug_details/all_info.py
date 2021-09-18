import logging

from typing import Optional
from debug_details.dataclasses_ import AllLogInfo

from debug_details.log_info import log_details
from debug_details.system_info import system_details


def debug_info(
    project_name: str,
    level: str, 
    message: str, 
    frame_caller, 
    additional_info: Optional[dict] = None
) -> AllLogInfo:
    logging.debug('Getting all debug info')
    
    log_details_ = log_details(
        level, 
        message, 
        frame_caller, 
        additional_info
    )
    
    system_details_ = system_details()

    logging.debug('Generating all log info')
    return AllLogInfo(
        project_name=project_name,
        log=log_details_,
        system_info=system_details_
    )
