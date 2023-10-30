from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings

from enums import AuthProviderForRoleCheck


class Config(BaseSettings):
    """Will automatically populate values from environment variables with the same name as the fields"""

    MONGO_USERNAME: str = Field("maf", alias="MONGO_INITDB_ROOT_USERNAME")
    MONGO_PASSWORD: str = Field("maf", alias="MONGO_INITDB_ROOT_PASSWORD")
    MONGO_URI: str | None = Field(None)
    ENVIRONMENT: str = Field("local")
    SECRET_KEY: str | None = Field(None)
    LOGGER_LEVEL: str = Field("DEBUG", to_lower=True)
    MAX_ENTITY_RECURSION_DEPTH: int = Field(50)
    CORE_DATA_SOURCE: str = "system"
    CACHE_MAX_SIZE: int = 200
    APPLICATION_HOME: str = Field(f"{Path(__file__).parent!s}/home")
    # Access Control
    DMSS_ADMIN: str = Field("dmss-admin")
    DMSS_ADMIN_ROLE: str = Field("dmss-admin")
    # Authentication
    AUTH_ENABLED: bool = Field(False)
    TEST_TOKEN: bool = False  # This value should only be changed at runtime by test setup
    OAUTH_WELL_KNOWN: str | None = Field(None)
    OAUTH_TOKEN_ENDPOINT: str = Field("")
    OAUTH_AUTH_ENDPOINT: str = Field("")
    OAUTH_CLIENT_ID: str = Field("dmss")
    OAUTH_CLIENT_SECRET: str = Field("")
    AUTH_AUDIENCE: str = Field("dmss", alias="OAUTH_AUDIENCE")
    OAUTH_AUTH_SCOPE: str = Field("")
    MICROSOFT_AUTH_PROVIDER: str = "login.microsoftonline.com"
    AUTH_PROVIDER_FOR_ROLE_CHECK: AuthProviderForRoleCheck | None = Field(None)
    AAD_ENTERPRISE_APP_OID: str = Field("", description="The ObjectId of the Azure AD Enterprise Application")


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
        raise OSError(
            "Environment variables 'OAUTH_CLIENT_ID' and 'OAUTH_CLIENT_SECRET' are required if "
            + "live role checks are enabled with 'AUTH_PROVIDER_FOR_ROLE_CHECK'"
        )
    if (
        config.AUTH_PROVIDER_FOR_ROLE_CHECK == AuthProviderForRoleCheck.AZURE_ACTIVE_DIRECTORY
        and not config.AAD_ENTERPRISE_APP_OID
    ):
        raise OSError("Missing required environment variable 'AAD_ENTERPRISE_APP_OID'")
