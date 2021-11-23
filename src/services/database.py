from pymongo import MongoClient
from config import config

mongo_client = None
if config.MONGO_USERNAME and config.MONGO_PASSWORD:
    mongo_client = MongoClient("db", username=config.MONGO_USERNAME, password=config.MONGO_PASSWORD)
elif config.MONGO_URI:
    mongo_client = MongoClient(config.MONGO_URI, connect=False)
else:
    raise ValueError("Missing credentials for the DataSource database")

data_source_db = mongo_client["data-source-database"]
data_source_collection = mongo_client["data-source-database"]["data_sources"]
