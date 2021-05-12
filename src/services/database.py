from pymongo import MongoClient
from config import Config


if Config.ENVIRONMENT == "local":
    client = MongoClient("db", username=Config.MONGO_USERNAME, password=Config.MONGO_PASSWORD)
else:
    client = MongoClient(Config.MONGO_URI, connect=False)

dmt_database = client[Config.MONGO_DB]
