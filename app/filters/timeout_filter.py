from aiogram.filters import BaseFilter
from aiogram.types import Update

from app.core.redis import redis_session
from app.services.one_time_code_repository import timeout_repository


class TimeoutFilter(BaseFilter):
    def __init__(self):
        super().__init__()

    async def __call__(self, update: Update) -> bool:
        return await timeout_repository.check(update.from_user.id, "timeout", redis_session)
