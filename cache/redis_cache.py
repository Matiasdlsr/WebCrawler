import redis

class RedisCache:
    def __init__(self, host='localhost', port=6379, db=0):
        self.client = redis.StrictRedis(host=host, port=port, db=db, decode_responses=True)

    def set_cache(self, key, value, expiration=3600):
        self.client.set(key, value, ex=expiration)

    def get_cache(self, key):
        return self.client.get(key)

    def delete_cache(self, key):
        self.client.delete(key)
