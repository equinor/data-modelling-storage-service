from pymongo import MongoClient
from config import config
from functools import lru_cache
from storage.repositories.azure_blob import AzureBlobStorageClient
from storage.repositories.mongo import MongoDBClient
from enums import RepositoryType, StorageDataTypes
from utils.encryption import decrypt

tls_args = {
    "tls": True if config.MONGO_SELF_SIGN_CA_CRT else False,
    "tlsCAFile": config.MONGO_SELF_SIGN_CA_PATH if config.MONGO_SELF_SIGN_CA_CRT else None,
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


@lru_cache(maxsize=config.CACHE_MAX_SIZE)
def get_client(**kwargs):
    if kwargs["type"] == RepositoryType.MONGO.value:
        handler = MongoClient(
            host=kwargs["host"],
            port=kwargs["port"],
            username=kwargs["username"],
            password=decrypt(kwargs["password"]),
            tls=True if config.MONGO_SELF_SIGN_CA_CRT else False,
            tlsCAFile=config.MONGO_SELF_SIGN_CA_PATH if config.MONGO_SELF_SIGN_CA_CRT else None,
            connectTimeoutMS=15000,
            serverSelectionTimeoutMS=15000,
            retryWrites=True,
            connect=True
        )
        return MongoDBClient(handler=handler, database=kwargs["database"], collection=kwargs["collection"])

    if kwargs["type"] == RepositoryType.AZURE_BLOB_STORAGE.value:
        return AzureBlobStorageClient(**kwargs)
