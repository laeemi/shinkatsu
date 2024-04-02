from redis import asyncio as aioredis

from app.bot import bot_settings

redis = aioredis.from_url(bot_settings.REDIS_URL.unicode_string(), encoding="utf-8", decode_responses=True)


redis_session = redis.client()
