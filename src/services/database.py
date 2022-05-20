from pymongo import MongoClient
from config import config

tls_args = {
    "tls": True if config.MONGO_SELF_SIGN_CA_PEM else False,
    "tlsCAFile": config.MONGO_SELF_SIGN_CA_PATH if config.MONGO_SELF_SIGN_CA_PEM else None,
}

mongo_client = None
if config.MONGO_URI:
    mongo_client = MongoClient(config.MONGO_URI, connect=False, **tls_args)
elif config.MONGO_USERNAME and config.MONGO_PASSWORD:
    mongo_client = MongoClient("db", username=config.MONGO_USERNAME, password=config.MONGO_PASSWORD, **tls_args)

else:
    raise ValueError("Missing credentials for the DataSource database")

internal_db = mongo_client["dmss-internal"]
data_source_collection = mongo_client["dmss-internal"]["data_sources"]
personal_access_token_collection = mongo_client["dmss-internal"]["personal_access_tokens"]
