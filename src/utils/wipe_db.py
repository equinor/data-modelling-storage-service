from services.database import mongo_client
from utils.logging import logger


def wipe_db():
    databases = mongo_client.list_database_names()
    databases = [
        databasename for databasename in databases if databasename not in ("admin", "local")
    ]  # Don't delete the mongo admin or local database
    logger.warning(f"Dropping all databases {tuple(databases)}")
    for db_name in databases:
        logger.debug(f"Dropping database '{db_name}' from the DMSS system MongoDB server")
        mongo_client.drop_database(db_name)
