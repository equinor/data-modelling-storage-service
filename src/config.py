from pathlib import Path
from typing import List

from pydantic import BaseSettings, Field


class Config(BaseSettings):
    MONGO_USERNAME: str = Field("maf", env="MONGO_INITDB_ROOT_USERNAME")
    MONGO_PASSWORD: str = Field("maf", env="MONGO_INITDB_ROOT_PASSWORD")
    MONGO_URI: str = Field(None, env="MONGO_AZURE_URI")
    ENVIRONMENT: str = Field("local", env="ENVIRONMENT")
    SECRET_KEY: str = Field(None, env="SECRET_KEY")
    LOGGER_LEVEL: str = Field("INFO", env="LOGGING_LEVEL", to_lower=True)
    MAX_ENTITY_RECURSION_DEPTH: int = Field(50, env="MAX_ENTITY_RECURSION_DEPTH")
    DATA_SOURCES_COLLECTION: str = "data_sources"
    CORE_DATA_SOURCE: str = "system"
    CORE_PACKAGES: List[str] = ["SIMOS"]
    CACHE_MAX_SIZE: int = 200
    APPLICATION_HOME: str = Field(f"{str(Path(__file__).parent)}/home", env="APPLICATION_HOME")
    # Access Control
    DMSS_ADMIN = Field("dmss-admin", env="DMSS_ADMIN")
    DMSS_ADMIN_ROLE = Field("dmss-admin", env="DMSS_ADMIN_ROLE")
    # Authentication
    AUTH_ENABLED: bool = Field(False, env="AUTH_ENABLED")
    OAUTH_WELL_KNOWN: str = Field(None, env="OAUTH_WELL_KNOWN")
    OAUTH_TOKEN_ENDPOINT: str = Field("", env="OAUTH_TOKEN_ENDPOINT")
    OAUTH_AUTH_ENDPOINT: str = Field("", env="OAUTH_AUTH_ENDPOINT")
    OAUTH_CLIENT_ID = Field("dmss", env="OAUTH_CLIENT_ID")


config = Config()
if config.AUTH_ENABLED:
    print("Authentication is enabled")
    if not config.OAUTH_WELL_KNOWN or not config.OAUTH_TOKEN_ENDPOINT or not config.OAUTH_AUTH_ENDPOINT:
        raise ValueError(
            "Environment variable 'OAUTH_WELL_KNOWN', 'OAUTH_AUTH_ENDPOINT',"
            "and 'OAUTH_TOKEN_ENDPOINT' must be set when 'AUTH_ENABLED' is 'True'"
        )
