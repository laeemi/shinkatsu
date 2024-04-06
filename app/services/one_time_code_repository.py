from dataclasses import dataclass
from datetime import timedelta
from typing import Optional

from redis import asyncio as aioredis


@dataclass
class OneTimeCodeRepository:
    key_prefix: str
    period: Optional[timedelta] = None

    def _get_key(self, user_id: str, code: str) -> str:
        return f"{self.key_prefix}:{user_id}:{code}"

    async def delete_code(self, code: str, session: aioredis.Redis):
        pattern = self._get_key("*", code)
        keys = await session.keys(pattern)
        await session.delete(*keys)
        await session.close()

    async def delete_user(self, user_id: str, session: aioredis.Redis):
        pattern = self._get_key(user_id, "*")
        keys = await session.keys(pattern)
        await session.delete(*keys)
        await session.close()

    async def delete(self, user_id: str, code: str, session: aioredis.Redis):
        key = self._get_key(user_id, code)
        await session.delete(key)
        await session.close()

    async def get_user_id(self, code: str, session: aioredis.Redis) -> Optional[int]:
        pattern = self._get_key("*", code)
        keys = await session.keys(pattern)
        await session.close()
        if len(keys) == 0:
            return None
        return int(keys[0].split(":")[1])

    async def get_code(self, user_id: str, session: aioredis.Redis) -> Optional[str]:
        pattern = f"{self.key_prefix}:{user_id}:*"
        keys = await session.keys(pattern)
        await session.close()
        try:
            return str(keys[0].split(":")[2])
        except IndexError:
            return None

    async def set(self, user_id: str, code: str, session: aioredis.Redis):
        key: str = self._get_key(user_id, code)
        await session.set(key, value=1, ex=self.period)
        await session.close()

    async def check(self, user_id: str, code: str, session: aioredis.Redis) -> bool:
        key: str = self._get_key(user_id, code)
        check = await session.exists(key)
        await session.close()
        return check

    async def check_pattern(self, user_id, session: aioredis) -> bool:
        pattern = f"{self.key_prefix}:{user_id}:*"
        keys = await session.keys(pattern)
        await session.close()
        return len(keys) > 0


api_key_repository = OneTimeCodeRepository(key_prefix="api_key")
negative_prompt_repository = OneTimeCodeRepository(key_prefix="n_prompt")
model_repository = OneTimeCodeRepository(key_prefix="model")
timeout_repository = OneTimeCodeRepository(key_prefix="timeout", period=timedelta(minutes=5))
