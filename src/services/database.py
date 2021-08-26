from pymongo import MongoClient
from config import config

mongo_client = None
if config.ENVIRONMENT == "local":
    mongo_client = MongoClient("db", username=config.MONGO_USERNAME, password=config.MONGO_PASSWORD)
else:
    mongo_client = MongoClient(config.MONGO_URI, connect=False)

data_source_db = mongo_client["data-source-database"]
data_source_collection = mongo_client["data-source-database"]["data_sources"]
