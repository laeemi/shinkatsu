from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.callbacks.menu import MenuCallback


def get_menu_kb() -> InlineKeyboardMarkup:
    buttons = [
            [InlineKeyboardButton(text="Генерация изображений", callback_data=MenuCallback(foo="gen").pack())],
            [InlineKeyboardButton(text="Доступные Модели", callback_data=MenuCallback(foo="models").pack())],
            [InlineKeyboardButton(text="Доступные Loras", callback_data=MenuCallback(foo="loras").pack())],
            [InlineKeyboardButton(text="Доступные Семплеры", callback_data=MenuCallback(foo="samplers").pack())],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)