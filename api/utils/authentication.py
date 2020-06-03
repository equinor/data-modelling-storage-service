import json

import jwt
import requests
from cachetools import cached, TTLCache
from flask import g
from jwt.algorithms import RSAAlgorithm

from api.classes.user import User
from api.config import Config
from api.core.storage.repository_exceptions import AuthenticationException
from api.utils.logging import logger


@cached(cache=TTLCache(maxsize=128, ttl=86400))
def get_cert(key_id):
    """
    Fetches JSON-Web-Keys from the env AUTH_JWK_URL url
    Returns a RSA PEM byte object from the key with the same 'kid' as the token.
    Time-To-Live cache that expires every 24h
    """
    try:
        jwks = requests.get(Config.AUTH_JWK_URL).json()["keys"]
        return next((RSAAlgorithm.from_jwk(json.dumps(key)) for key in jwks if key["kid"] == key_id))
    except requests.RequestException as error:
        raise AuthenticationException(error)


def decode_jwt(token):
    try:
        # If authentication is disabled, we create a mock user with the higest privileges.
        if not Config.AUTH_ENABLED:
            g.user = User(name="No Auth", upn="noauth@hogwarts.edu", roles=["global_admin"])
            return {}

        # If Auth is configured with a secret, we use that to decode the token
        if Config.AUTH_SECRET:
            decoded_token = jwt.decode(
                token, Config.AUTH_SECRET, algorithms="HS256", audience=Config.AUTH_JWT_AUDIENCE
            )
        # If auth is enabled and no secret provided, fallback to RSA based token signing.
        else:
            cert = get_cert(jwt.get_unverified_header(token)["kid"])
            decoded_token = jwt.decode(token, cert, algorithms="RS256", audience=Config.AUTH_JWT_AUDIENCE)
        g.user = User(**decoded_token)
        return decoded_token
    except Exception as e:
        logger.warning(f"Unauthorized Request: {e}")
