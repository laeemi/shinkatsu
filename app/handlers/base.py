from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.keyboards.menu import get_menu_kb

router = Router()


@router.message(Command("start"))
async def start_cmd(message: Message):
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
