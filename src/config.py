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
    AUTH_ENABLED = os.getenv("AUTH_ENABLED", "FALSE").upper() == "TRUE"
    OAUTH_WELL_KNOWN = os.getenv("OAUTH_WELL_KNOWN")
    OAUTH_TOKEN_ENDPOINT = os.getenv("OAUTH_TOKEN_ENDPOINT", "")
    OAUTH_AUTH_ENDPOINT = os.getenv("OAUTH_AUTH_ENDPOINT", "")
    OAUTH_CLIENT_ID = os.getenv("OAUTH_CLIENT_ID", "dmss")
    if AUTH_ENABLED:
        print("Authentication is enabled")
        if not OAUTH_WELL_KNOWN or not OAUTH_TOKEN_ENDPOINT or not OAUTH_AUTH_ENDPOINT:
            raise ValueError(
                "Environment variable 'OAUTH_WELL_KNOWN', 'OAUTH_AUTH_ENDPOINT',"
                "and 'OAUTH_TOKEN_ENDPOINT' must be set when 'AUTH_ENABLED' is 'True'"
            )

    DMSS_ADMIN = os.getenv("DMSS_ADMIN", "dmss-admin")
    DMSS_ADMIN_ROLE = os.getenv("DMSS_ADMIN_ROLE", "dmss-admin")


config = Config()
