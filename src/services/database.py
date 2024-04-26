from storage.internal.redis_client import RedisClient

data_source_db = RedisClient(0)
personal_access_token_db = RedisClient(1)
lookup_table_db = RedisClient(2)
acl_lookup_db = RedisClient(3)
