from pymongo import MongoClient

from services.database import acl_lookup_db, data_source_db, lookup_table_db, personal_access_token_db

mongo_client = MongoClient(
    "db",
    username="maf",
    password="maf",  # noqa S105
    connectTimeoutMS=5000,
    serverSelectionTimeoutMS=5000,
)


# Should only be called on local test databases.
# As databases in test and production environments have some configuration we would like to persist
def wipe_db():
    databases = mongo_client.list_database_names()
    databases = [
        databasename for databasename in databases if databasename not in ("admin", "local", "config")
    ]  # Don't delete the mongo admin or local database
    for db_name in databases:
        mongo_client.drop_database(db_name)

    data_source_db.client.flushdb()
    personal_access_token_db.client.flushdb()
    lookup_table_db.client.flushdb()
    acl_lookup_db.client.flushdb()
