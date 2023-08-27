from instance.config import REDIS_HOST, REDIS_PORT
import redis

redis_host = REDIS_HOST
redis_port = REDIS_PORT
redis_client = redis.Redis(host=redis_host, port=redis_port)
