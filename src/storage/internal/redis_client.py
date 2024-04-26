import json

import redis
from redis.exceptions import DataError

from config import config


def get_redis_client(database: int) -> redis.Redis:
    db = redis.Redis(
        host=config.REDIS_HOST,
        port=config.REDIS_PORT,
        password=config.REDIS_PASSWORD,
        db=database,
        decode_responses=True,
        ssl=config.REDIS_SSL_ENABLED,
    )

    return db


class RedisClient:
    def __init__(self, database: int):
        self.client = get_redis_client(database)

    def get(self, key: str) -> dict | None:
        if value := self.client.get(key):
            return json.loads(value)
        return None

    def set(self, key: str, value: dict) -> None:
        try:
            self.client.set(key, json.dumps(value))
        except DataError as e:
            raise ValueError(f"Failed to set key '{key}' with value '{value}'") from e

    def list_keys(self) -> list[str]:
        return self.client.keys()

    def delete(self, key: str) -> None:
        self.client.delete(key)
