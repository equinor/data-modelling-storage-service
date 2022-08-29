from pathlib import Path

from pydantic import BaseSettings, Field

from authentication.models import User
from enums import AuthProviderForRoleCheck


class Config(BaseSettings):
    MONGO_USERNAME: str = Field("maf", env="MONGO_INITDB_ROOT_USERNAME")
    MONGO_PASSWORD: str = Field("maf", env="MONGO_INITDB_ROOT_PASSWORD")
    MONGO_URI: str = Field(None, env="MONGO_URI")
    ENVIRONMENT: str = Field("local", env="ENVIRONMENT")
    SECRET_KEY: str = Field(None, env="SECRET_KEY")
    LOGGER_LEVEL: str = Field("INFO", env="LOGGING_LEVEL", to_lower=True)
    MAX_ENTITY_RECURSION_DEPTH: int = Field(50, env="MAX_ENTITY_RECURSION_DEPTH")
    CORE_DATA_SOURCE: str = "system"
    CACHE_MAX_SIZE: int = 200
    APPLICATION_HOME: str = Field(f"{str(Path(__file__).parent)}/home", env="APPLICATION_HOME")
    # Access Control
    DMSS_ADMIN: str = Field("dmss-admin", env="DMSS_ADMIN")
    DMSS_ADMIN_ROLE: str = Field("dmss-admin", env="DMSS_ADMIN_ROLE")
    # Authentication
    AUTH_ENABLED: bool = Field(False, env="AUTH_ENABLED")
    TEST_TOKEN: bool = False  # This value should only be changed at runtime by test setup
    OAUTH_WELL_KNOWN: str = Field(None, env="OAUTH_WELL_KNOWN")
    OAUTH_TOKEN_ENDPOINT: str = Field("", env="OAUTH_TOKEN_ENDPOINT")
    OAUTH_AUTH_ENDPOINT: str = Field("", env="OAUTH_AUTH_ENDPOINT")
    OAUTH_CLIENT_ID: str = Field("dmss", env="OAUTH_CLIENT_ID")
    OAUTH_CLIENT_SECRET: str = Field("", env="OAUTH_CLIENT_SECRET")
    AUTH_AUDIENCE: str = Field("dmss", env="OAUTH_AUDIENCE")
    MICROSOFT_AUTH_PROVIDER: str = "login.microsoftonline.com"
    AUTH_PROVIDER_FOR_ROLE_CHECK: AuthProviderForRoleCheck = Field(None, env="AUTH_PROVIDER_FOR_ROLE_CHECK")
    AAD_ENTERPRISE_APP_OID: str = Field(
        "", env="AAD_ENTERPRISE_APP_OID", description="The ObjectId of the Azure AD Enterprise Application"
    )


config = Config()
if not config.AUTH_ENABLED:
    print("################ WARNING ################")
    print("#       Authentication is disabled      #")
    print("################ WARNING ################")
else:
    print(f"Authentication is enabled. Admin user is: {config.DMSS_ADMIN}, admin role is: {config.DMSS_ADMIN_ROLE}")

if config.TEST_TOKEN:
    print("########################### WARNING ################################")
    print("#  Authentication is configured to use the mock test certificates  #")
    print("########################### WARNING ################################")

if config.AUTH_ENABLED and not all((config.OAUTH_WELL_KNOWN, config.OAUTH_TOKEN_ENDPOINT, config.OAUTH_AUTH_ENDPOINT)):
    raise ValueError(
        "Environment variable 'OAUTH_WELL_KNOWN', 'OAUTH_AUTH_ENDPOINT',"
        "and 'OAUTH_TOKEN_ENDPOINT' must be set when 'AUTH_ENABLED' is 'True'"
    )

if config.AUTH_PROVIDER_FOR_ROLE_CHECK:
    if not all((config.OAUTH_CLIENT_ID, config.OAUTH_CLIENT_SECRET)):
        raise EnvironmentError(
            "Environment variables 'OAUTH_CLIENT_ID' and 'OAUTH_CLIENT_SECRET' are required if "
            + "live role checks are enabled with 'AUTH_PROVIDER_FOR_ROLE_CHECK'"
        )
    if (
        config.AUTH_PROVIDER_FOR_ROLE_CHECK == AuthProviderForRoleCheck.AZURE_ACTIVE_DIRECTORY
        and not config.AAD_ENTERPRISE_APP_OID
    ):
        raise EnvironmentError("Missing required environment variable 'AAD_ENTERPRISE_APP_OID'")

default_user: User = User(**{"user_id": "nologin", "full_name": "Not Authenticated", "email": "nologin@example.com"})
