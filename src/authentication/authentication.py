import requests
from cachetools import cached, TTLCache
from fastapi import HTTPException, Security
from fastapi.security import OAuth2AuthorizationCodeBearer
from jose import jwt, JWTError
from requests import HTTPError
from starlette import status

from authentication.mock_users import fake_users_db
from authentication.models import TokenData, User
from config import Config
from utils.logging import logger


oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=Config.OAUTH_AUTH_ENDPOINT, tokenUrl=Config.OAUTH_TOKEN_ENDPOINT,
)

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="Token validation failed", headers={"WWW-Authenticate": "Bearer"}
)


@cached(cache=TTLCache(maxsize=32, ttl=86400))
def fetch_openid_configuration() -> dict:
    try:
        oid_conf_response = requests.get(Config.OAUTH_WELL_KNOWN)
        oid_conf_response.raise_for_status()
        oid_conf = oid_conf_response.json()
    except (ConnectionError, HTTPError) as error:
        logger.error(f"Failed to fetch OpenId Connect configuration for '{Config.OAUTH_WELL_KNOWN}': {error}")
        raise error

    try:
        json_web_key_set_response = requests.get(oid_conf["jwks_uri"])
        json_web_key_set_response.raise_for_status()
    except HTTPError as error:
        logger.error(f"Failed to fetch OpenId Connect JWKS from '{oid_conf['jwks_uri']}': {error}")
        raise error
    return {
        "authorization_endpoint": oid_conf["authorization_endpoint"],
        "token_endpoint": oid_conf["token_endpoint"],
        "jwks": json_web_key_set_response.json()["keys"],
    }


async def get_current_user(token: str = Security(oauth2_scheme) if Config.AUTH_ENABLED else None) -> User:
    if not Config.AUTH_ENABLED:
        return fake_users_db["nologin"]
    config = fetch_openid_configuration()
    try:
        payload = jwt.decode(token, config["jwks"], algorithms=["RS256"], audience="dmss")
        token_data = TokenData(username=payload["sub"], **payload)
    except JWTError as error:
        logger.warning(error)
        raise credentials_exception
    user = fake_users_db.get(token_data.username)
    if user is None:
        raise credentials_exception
    return user
