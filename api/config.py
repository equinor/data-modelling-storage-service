import json
import os
from pathlib import Path


class Config:
    AUTH_ENABLED = os.getenv("AUTH_ENABLED", "0") in ("1", "True", "true")
    AUTH_SECRET = os.getenv("AUTH_SECRET")
    AUTH_JWT_AUDIENCE = os.getenv("AUTH_JWT_AUDIENCE", "97a6b5bd-63fb-42c6-bb75-7e5de2394ba0")
    AUTH_JWK_URL = os.getenv("AUTH_JWK_URL", "https://login.microsoftonline.com/common/discovery/v2.0/keys")
    MONGO_USERNAME = os.getenv("MONGO_INITDB_ROOT_USERNAME", "maf")
    MONGO_PASSWORD = os.getenv("MONGO_INITDB_ROOT_PASSWORD", "maf")
    MONGO_URI = os.getenv("MONGO_AZURE_URI", "")
    MONGO_DB = os.getenv("ENVIRONMENT", os.getenv("RADIX_ENVIRONMENT", "local"))
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
    with open(DMT_SETTINGS_FILE) as json_file:
        DMT_APPLICATION_SETTINGS = json.load(json_file)
    with open(ENTITY_SETTINGS_FILE) as json_file:
        ENTITY_APPLICATION_SETTINGS = json.load(json_file)
