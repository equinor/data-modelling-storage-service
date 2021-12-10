from cryptography.fernet import Fernet

from config import config


def key_loaded():
    if not config.SECRET_KEY:
        raise EnvironmentError(
            "The encryption/decryption was attempted without supplying the 'SECRET_KEY' environment variable"
        )


def generate_key():
    key = Fernet.generate_key()
    return key.decode()


def encrypt(message: str) -> str:
    key_loaded()
    fernet = Fernet(config.SECRET_KEY)
    message_as_bytes = message.encode()
    token = fernet.encrypt(message_as_bytes)
    return token.decode()


def decrypt(token: str) -> str:
    if not token:
        return ""
    key_loaded()
    fernet = Fernet(config.SECRET_KEY)
    token_as_bytes = token.encode()
    message_as_bytes = fernet.decrypt(token_as_bytes)
    return message_as_bytes.decode()
