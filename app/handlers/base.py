from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.core.redis import redis_session
from app.keyboards.menu import get_menu_kb
from app.services.one_time_code_repository import model_repository

router = Router()


@router.message(Command("start"))
async def start_cmd(message: Message):
    if not await model_repository.check_pattern(message.from_user.id, redis_session):
        await model_repository.set(message.from_user.id, "animagineXL_Euler", redis_session)
    await message.answer(f"Привет, {message.from_user.username} \n"
                         f"Для использования бота: /menu")


@router.message(Command("menu"))
async def menu(message: Message):
    await message.answer(
        text="Меню бота",
        reply_markup=get_menu_kb()
    )


@router.message(Command("about"))
async def about(message: Message):
    await message.answer("Бот для генерации изображений с помощью Stable Diffusion XL \n"
                         "by @laaemi")
