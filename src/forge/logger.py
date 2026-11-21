'''
This script handles logging.
'''

import logging

# Init logger and default settings
log = logging.getLogger("logger")
logging.basicConfig(level=logging.DEBUG)


def set_level(level: str):
    logging.basicConfig(level=getattr(logging, level.upper()))

def debug(msg : str):
    log.debug(msg)

def info(msg : str):
    log.info(msg)

def warning(msg : str):
    log.warning(msg)

def error(msg : str):
    log.error(msg)

