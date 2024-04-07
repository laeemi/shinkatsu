from typing import Optional

from aiogram.filters.callback_data import CallbackData


class SettingsCallback(CallbackData, prefix="settings"):
    choice: str
    count: Optional[str] = None
