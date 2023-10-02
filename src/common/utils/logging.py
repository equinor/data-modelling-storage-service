import logging

from config import config

logger = logging.getLogger("DMSS-API")
logger.setLevel(config.LOGGER_LEVEL.upper())
formatter = logging.Formatter("%(levelname)s:%(asctime)s %(message)s")
channel = logging.StreamHandler()
channel.setFormatter(formatter)
channel.setLevel(config.LOGGER_LEVEL.upper())
logger.addHandler(channel)
