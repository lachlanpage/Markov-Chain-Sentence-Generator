import logging
import coloredlogs
from config import Config


def configure_logger(name):
    logger = logging.getLogger(name)
    fmt = "[%(levelname)s] %(message)s"

    # Use the VERBOSE and QUIET flags from the Config class
    if Config.VERBOSE:

        log_level = 'DEBUG'

    elif Config.QUIET:

        #  Set log level to CRITICAL if QUIET is set
        log_level = logging.CRITICAL

    else:

        # Default to INFO if no flags are set
        log_level = 'INFO'

    coloredlogs.install(level=log_level, logger=logger, fmt=fmt)

    return logger

