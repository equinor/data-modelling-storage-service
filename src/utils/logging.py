import logging
from config import Config

uvicorn_logger = logging.getLogger("uvicorn")

logger = logging.getLogger("DMSS-API")
logger.setLevel(Config.LOGGER_LEVEL)
formatter = logging.Formatter("%(levelname)s:%(asctime)s %(message)s")
channel = logging.StreamHandler()
channel.setFormatter(formatter)
channel.setLevel(Config.LOGGER_LEVEL)
logger.addHandler(channel)
