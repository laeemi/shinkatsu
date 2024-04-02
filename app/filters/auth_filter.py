from aiogram.filters import BaseFilter
from aiogram.types import Update

from app.core.redis import redis_session
from app.services.one_time_code_repository import api_key_repository


class AuthFilter(BaseFilter):
    def __init__(self):
        super().__init__()

    async def __call__(self, update: Update) -> bool:
        return await api_key_repository.check_pattern(update.from_user.id, redis_session)
