import redis
from app.core.config import Settings

client = redis.Redis(

    host=Settings.REDIS_HOST,
    port=Settings.REDIS_PORT,
    decode_responses=Settings.DECODE_RESPONSES

)

