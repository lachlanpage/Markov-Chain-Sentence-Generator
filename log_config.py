import logging
import coloredlogs


def configure_logger(name, verbose=False, quiet=False):
    logger = logging.getLogger(name)
    fmt = "[%(levelname)s] %(message)s"

    if verbose:
        # coloredlogs.install(level='DEBUG', logger=logger, fmt=fmt)
        log_level = 'DEBUG'
    elif quiet:
        # coloredlogs.install(level='CRITICAL +1', logger=logger, fmt=fmt)
        log_level = logging.CRITICAL + 1
    else:
        # coloredlogs.install(level='INFO', logger=logger, fmt=fmt)
        log_level = 'INFO'

    coloredlogs.install(level=log_level, logger=logger, fmt=fmt)

    return logger

    # logger = logging.getLogger(name)
    # fmt = "[%(levelname)s] %(message)s"
    #
    # if verbose:
    #     coloredlogs.install(level='DEBUG', logger=logger, fmt=fmt)
    # else:
    #     coloredlogs.install(level='INFO', logger=logger, fmt=fmt)
    #
    # return logger
    # logger = logging.getLogger(name)
    # fmt = "[%(levelname)s] %(message)s"
    #
    # # coloredlogs.DEFAULT_FIELD_STYLES["levelname"]["info"] = {"color": "white"}
    # # coloredlogs.DEFAULT_LEVEL_STYLES["info"] = {"color": "white"}
    # coloredlogs.install(level='DEBUG', logger=logger, fmt=fmt)

    # return logger
