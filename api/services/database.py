from pymongo import MongoClient
from api.utils.logging import logger
from api.config import Config


if Config.MONGO_URI:
    logger.info(f"Using Database based on connection URI")
    client = MongoClient(Config.MONGO_URI, connect=False)
else:
    logger.info(f"Using Database based on username and password")
    client = MongoClient("db", username=Config.MONGO_USERNAME, password=Config.MONGO_PASSWORD)
    
dmt_database = client[Config.MONGO_DB]
