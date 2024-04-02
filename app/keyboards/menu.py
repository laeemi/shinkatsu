from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.callbacks.menu import MenuCallback


def get_menu_kb() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="API KEY", callback_data=MenuCallback(choice="api_key").pack())],
        [InlineKeyboardButton(text="Генерация изображений", callback_data=MenuCallback(choice="gen").pack())],
        [InlineKeyboardButton(text="Выбрать Модель", callback_data=MenuCallback(choice="models").pack())],
        [InlineKeyboardButton(text="Выбрать Семплер", callback_data=MenuCallback(choice="samplers").pack())],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_api_key_kb() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="Изменить", callback_data=MenuCallback(choice="api_key").pack())]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
