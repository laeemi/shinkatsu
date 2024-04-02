from aiogram.filters.callback_data import CallbackData


class ModelsSamplersCallback(CallbackData, prefix="models-samplers"):
    action: str
    choice: str
