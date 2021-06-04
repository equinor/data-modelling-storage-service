from pymongo import MongoClient
from config import Config

mongo_client = None
if Config.ENVIRONMENT == "local":
    mongo_client = MongoClient("db", username=Config.MONGO_USERNAME, password=Config.MONGO_PASSWORD)
else:
    mongo_client = MongoClient(Config.MONGO_URI, connect=False)

data_source_db = mongo_client["data-source-database"]
data_source_collection = mongo_client["data-source-database"]["data_sources"]
