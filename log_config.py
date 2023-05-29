import logging
import coloredlogs


def configure_logger(name):
    logger = logging.getLogger(name)
    fmt = "[%(levelname)s] %(message)s"

    # coloredlogs.DEFAULT_FIELD_STYLES["levelname"]["info"] = {"color": "white"}
    # coloredlogs.DEFAULT_LEVEL_STYLES["info"] = {"color": "white"}
    coloredlogs.install(level='DEBUG', logger=logger, fmt=fmt)

    return logger
