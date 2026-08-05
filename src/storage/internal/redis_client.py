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

    def get_many(self, keys: list[str]) -> list[dict | None]:
        """Read many keys in a single round trip. A key that is not set reads back as None."""
        if not keys:
            return []
        return [json.loads(value) if value else None for value in self.client.mget(keys)]

    def set(self, key: str, value: dict, ttl: int | None = None) -> None:
        try:
            self.client.set(key, json.dumps(value), ex=ttl)
        except DataError as e:
            raise ValueError(f"Failed to set key '{key}' with value '{value}'") from e

    def set_many(self, values: dict[str, dict], ttl: int | None = None) -> None:
        """Write many keys in a single round trip.

        Redis' own MSET cannot express a time to live, so this pipelines the individual writes
        instead, which is still one round trip.
        """
        if not values:
            return
        pipeline = self.client.pipeline(transaction=False)
        for key, value in values.items():
            pipeline.set(key, json.dumps(value), ex=ttl)
        try:
            # The commands are only encoded here, so this is where a bad value is rejected.
            pipeline.execute()
        except DataError as e:
            raise ValueError(f"Failed to set keys '{', '.join(values)}'") from e

    def list_keys(self) -> list[str]:
        return self.client.keys()

    def delete(self, key: str) -> None:
        self.client.delete(key)
