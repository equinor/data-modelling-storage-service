import os
from pathlib import Path


class Config:
    MONGO_USERNAME = os.getenv("MONGO_INITDB_ROOT_USERNAME", "maf")
    MONGO_PASSWORD = os.getenv("MONGO_INITDB_ROOT_PASSWORD", "maf")
    MONGO_URI = os.getenv("MONGO_AZURE_URI", "")
    LOGGER_LEVEL = os.getenv("LOGGING_LEVEL", "INFO").upper()
    MAX_ENTITY_RECURSION_DEPTH = os.getenv("MAX_ENTITY_RECURSION_DEPTH", 50)
    ENVIRONMENT = os.getenv("ENVIRONMENT", "local")
    DATA_SOURCES_COLLECTION = "data_sources"
    CORE_DATA_SOURCE = "system"
    CORE_PACKAGES = ["SIMOS"]
    CACHE_MAX_SIZE = 200
    APPLICATION_HOME = os.getenv("APPLICATION_HOME", f"{str(Path(__file__).parent)}/home")
