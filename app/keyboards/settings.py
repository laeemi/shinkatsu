from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.callbacks.menu import MenuCallback
from app.callbacks.settings import SettingsCallback


def get_settings_kb() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="Негативный Prompt",
                              callback_data=SettingsCallback(choice="negative_prompt").pack())],
        [InlineKeyboardButton(text="Количество изображений",
                              callback_data=SettingsCallback(choice="imgs_count").pack())],
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
        [InlineKeyboardButton(text="Отменить", callback_data=SettingsCallback(choice="prompt_cancel").pack())]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_num_of_imgs_kb() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text="1", callback_data=SettingsCallback(choice="change_count", count="1").pack()),
            InlineKeyboardButton(text="2", callback_data=SettingsCallback(choice="change_count", count="2").pack())
        ],
        [
            InlineKeyboardButton(text="3", callback_data=SettingsCallback(choice="change_count", count="3").pack()),
            InlineKeyboardButton(text="4", callback_data=SettingsCallback(choice="change_count", count="4").pack())
        ],
        [InlineKeyboardButton(text="5", callback_data=SettingsCallback(choice="change_count", count="5").pack())],
        [InlineKeyboardButton(text="Назад", callback_data=SettingsCallback(choice="num_of_imgs_back").pack())]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)