from typing import Optional, List

import requests
from cachetools import cached, TTLCache
from fastapi import HTTPException, Security
from fastapi.security import OAuth2AuthorizationCodeBearer
from jose import jwt, JWTError
from pydantic import BaseModel
from starlette import status

from config import config
from utils.logging import logger

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=config.OAUTH_AUTH_ENDPOINT, tokenUrl=config.OAUTH_TOKEN_ENDPOINT,
)

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="Token validation failed", headers={"WWW-Authenticate": "Bearer"}
)


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    roles: List[str] = []


default_user: User = User(**{"username": "nologin", "full_name": "Not Authenticated", "email": "nologin@example.com"})


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


async def get_current_user(token: str = Security(oauth2_scheme) if config.AUTH_ENABLED else None) -> User:
    if not config.AUTH_ENABLED:
        return default_user
    oid_config = fetch_openid_configuration()
    try:
        payload = jwt.decode(token, {"keys": oid_config["jwks"]}, algorithms=["RS256"], audience=config.AUTH_AUDIENCE)
        user = User(username=payload["sub"], **payload)
    except JWTError as error:
        logger.warning(error)
        raise credentials_exception

    if user is None:
        raise credentials_exception
    return user
