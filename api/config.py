import json
import os
from pathlib import Path


class Config:
    MONGO_USERNAME = os.getenv("MONGO_INITDB_ROOT_USERNAME", "maf")
    MONGO_PASSWORD = os.getenv("MONGO_INITDB_ROOT_PASSWORD", "maf")
    MONGO_URI = os.getenv("MONGO_AZURE_URI", "")
    default_db = os.getenv("ENVIRONMENT", os.getenv("RADIX_ENVIRONMENT", "local"))
    MONGO_DB = os.getenv("MONGO_DB", default_db)
    LOGGER_LEVEL = os.getenv("LOGGING_LEVEL", "INFO")
    MAX_ENTITY_RECURSION_DEPTH = os.getenv("MAX_ENTITY_RECURSION_DEPTH", 50)
    FLASK_DEBUG = os.getenv("FLASK_DEBUG", 0)
    ENVIRONMENT = os.getenv("ENVIRONMENT", "local")
    BLUEPRINT_COLLECTION = "SSR-DataSource"
    ENTITY_COLLECTION = "entities"
    DATA_SOURCES_COLLECTION = "data_sources"
    SYSTEM_COLLECTION = "system"
    CACHE_MAX_SIZE = 200
    APPLICATION_HOME = os.getenv("APPLICATION_HOME", f"{Path(__file__).parent.absolute()}/home")
    DMT_SETTINGS_FILE = f"{APPLICATION_HOME}/dmt_settings.json"
    ENTITY_SETTINGS_FILE = f"{APPLICATION_HOME}/settings.json"
    SYSTEM_FOLDERS = ["SIMOS"]
    IMPORT_BLOBS = []
    with open(DMT_SETTINGS_FILE) as json_file:
        DMT_APPLICATION_SETTINGS = json.load(json_file)
    with open(ENTITY_SETTINGS_FILE) as json_file:
        ENTITY_APPLICATION_SETTINGS = json.load(json_file)
