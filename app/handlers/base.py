from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.core.redis import redis_session
from app.filters.generation_process_filter import GenFilter
from app.keyboards.menu import get_menu_kb
from app.services.one_time_code_repository import model_repository

router = Router()
router.callback_query.filter(GenFilter())
router.message.filter(GenFilter())


@router.message(Command("start"))
async def start_cmd(message: Message):
    if not await model_repository.check_pattern(message.from_user.id, redis_session):
        await model_repository.set(message.from_user.id, "animagineXL_Euler", redis_session)
    await message.answer(f"👋Привет, {message.from_user.username} \n"
                         f"📋Меню бота: /menu\n"
                         f"📢Для работы обязателен API KEY❗")


@router.message(Command("menu"), )
async def menu(message: Message):
    if not await model_repository.check_pattern(message.from_user.id, redis_session):
        await model_repository.set(message.from_user.id, "animagineXL_Euler", redis_session)
    model, sampler = (await model_repository.get_code(message.from_user.id, redis_session)).split("_")
    await message.answer(
        text=f"Меню бота\n"
             f"Выбранная модель: {model}\n"
             f"Выбранный семплер: {sampler}\n",
        reply_markup=get_menu_kb()
    )


@router.message(Command("help"))
async def about(message: Message):
    await message.answer("1) Для использования бота необходимо: \n"
                         " - Настроить API KEY в /menu - API KEY\n"
                         " - Для получения API KEY перейдите в @VisionCraft_bot и выполните необходимые условия\n"
                         "2) Чтобы настроить бота перейдите в /menu - Настройки"
                         )


@router.message(Command("about"))
async def about(message: Message):
    await message.answer("Бот для генерации изображений с помощью Stable Diffusion XL \n"
                         "by @laaemi")
