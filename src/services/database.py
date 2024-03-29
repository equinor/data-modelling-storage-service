from pymongo import MongoClient

from config import config

mongo_client = None
if config.MONGO_URI:
    mongo_client = MongoClient(config.MONGO_URI, connect=False)
elif config.MONGO_USERNAME and config.MONGO_PASSWORD:
    mongo_client = MongoClient(
        "db",
        username=config.MONGO_USERNAME,
        password=config.MONGO_PASSWORD,
        connectTimeoutMS=5000,
        serverSelectionTimeoutMS=5000,
    )

else:
    raise ValueError("Missing credentials for the DataSource database")

internal_db = mongo_client["dmss-internal"]
data_source_collection = internal_db["data_sources"]
personal_access_token_collection = internal_db["personal_access_tokens"]
lookup_table_collection = internal_db["lookup_tables"]
