import redis

class RedisCache:
#crear conexion con redis
    def __init__(self, host='localhost', port=6379, db=0):
        self.client = redis.StrictRedis(host=host, port=port, db=db, decode_responses=True)
#guardar datos en cache
    def set_cache(self, key, value, expiration=3600):
        self.client.set(key, value, ex=expiration)
#obtener datos desde cache
    def get_cache(self, key):
        return self.client.get(key)
#eliminar datos en cache
    def delete_cache(self, key):
        self.client.delete(key)
