from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.callbacks.menu import MenuCallback
from app.callbacks.settings import SettingsCallback


def get_settings_kb() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="Негативный Prompt",
                              callback_data=SettingsCallback(choice="negative_prompt").pack())],
        [InlineKeyboardButton(text="Модель", callback_data=SettingsCallback(choice="models").pack())],
        [InlineKeyboardButton(text="Семплер", callback_data=SettingsCallback(choice="samplers").pack())],
        [InlineKeyboardButton(text="Назад", callback_data=SettingsCallback(choice="settings_back").pack())],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_negative_prompt_kb() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="Изменить", callback_data=SettingsCallback(choice="change_n_prompt").pack())],
        [InlineKeyboardButton(text="Назад", callback_data=SettingsCallback(choice="n_prompt_back").pack())]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_negative_prompt_cancel_kb() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="Отменить", callback_data=SettingsCallback(choice="n_prompt_cancel").pack())]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_prompt_cancel_kb() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="Отменить", callback_data=MenuCallback(choice="prompt_cancel").pack())]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
