import redis
from settings import REDIS_SERVER, REDIS_PASSWD, DEV

if DEV:
        R = redis.Redis()
elif not DEV:
	R = redis.Redis(host=REDIS_SERVER, password=REDIS_PASSWD)
