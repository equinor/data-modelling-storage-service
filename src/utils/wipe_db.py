from services.database import dmt_database
from utils.logging import logger


def wipe_db():
    logger.info("Dropping all collections")
    for name in dmt_database.list_collection_names():
        logger.debug(f"Dropping collection '{name}'")
        dmt_database.drop_collection(name)
