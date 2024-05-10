from storage.internal.redis_client import RedisClient

data_source_db = RedisClient(0)
personal_access_token_db = RedisClient(1)
lookup_table_db = RedisClient(2)
acl_lookup_db = RedisClient(3)
document_cache = RedisClient(8)  # 5-6 are used by dm-job
blob_cache = RedisClient(9)
