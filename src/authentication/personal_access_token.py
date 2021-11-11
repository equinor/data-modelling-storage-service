import datetime

from jose import jwt, JWTError

from config import config
from domain_classes.user import User
from utils.exceptions import credentials_exception
from utils.logging import logger


def create_personal_access_token(user: User) -> str:
    # set expire time to 1 year
    exp = int(datetime.datetime.now().timestamp()) + int(datetime.timedelta(days=365).total_seconds())
    payload = {
        "username": user.username,
        "email": user.email,
        "fullname": user.full_name,
        "roles": user.roles,
        "aud": config.AUTH_AUDIENCE,
        "iss": config.JWT_SELF_SIGNING_ISSUER,
        "exp": exp,
    }
    token = jwt.encode(payload, config.SECRET_KEY, algorithm="HS512")
    return token


def validate_personal_access_token(pat: str) -> User:
    try:
        payload = jwt.decode(pat, config.SECRET_KEY, ["HS512"], audience=config.AUTH_AUDIENCE)
        user = User(**payload)
        return user
    except JWTError as error:
        logger.warning(error)
        raise credentials_exception
