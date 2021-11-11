import requests
from cachetools import cached, TTLCache
from fastapi import Security
from fastapi.security import OAuth2AuthorizationCodeBearer
from jose import jwt, JWTError

from authentication.personal_access_token import validate_personal_access_token
from config import config, default_user
from domain_classes.user import User
from utils.exceptions import credentials_exception
from utils.logging import logger
from utils.mock_token_generator import mock_rsa_public_key

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=config.OAUTH_AUTH_ENDPOINT,
    tokenUrl=config.OAUTH_TOKEN_ENDPOINT,
)


@cached(cache=TTLCache(maxsize=32, ttl=86400))
def fetch_openid_configuration() -> dict:
    try:
        oid_conf_response = requests.get(config.OAUTH_WELL_KNOWN)
        oid_conf_response.raise_for_status()
        oid_conf = oid_conf_response.json()
        json_web_key_set_response = requests.get(oid_conf["jwks_uri"])
        json_web_key_set_response.raise_for_status()
        return {
            "authorization_endpoint": oid_conf["authorization_endpoint"],
            "token_endpoint": oid_conf["token_endpoint"],
            "jwks": json_web_key_set_response.json()["keys"],
        }
    except Exception as error:
        logger.error(f"Failed to fetch OpenId Connect configuration for '{config.OAUTH_WELL_KNOWN}': {error}")
        raise credentials_exception


async def get_current_user(token: str = Security(oauth2_scheme)) -> User:
    if not config.AUTH_ENABLED:
        return default_user

    # If token is issued by THIS API, it's a Personal Access Token with the issuer set to "dmss"
    if jwt.get_unverified_claims(token).get("iss") == config.JWT_SELF_SIGNING_ISSUER:
        return validate_personal_access_token(token)

    # If TEST_TOKEN is true, we are running tests. Use the self signed keys. If not, get keys from auth server.
    key = mock_rsa_public_key if config.TEST_TOKEN else {"keys": fetch_openid_configuration()["jwks"]}

    try:
        payload = jwt.decode(token, key, algorithms=["RS256"], audience=config.AUTH_AUDIENCE)
        user = User(username=payload["sub"], **payload)
    except JWTError as error:
        logger.warning(error)
        raise credentials_exception

    if user is None:
        raise credentials_exception
    return user
