import aiohttp
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.callbacks.models_samplers import ModelsSamplersCallback


async def fetch_xl_models():
    """Get all available SDXL models"""
    async with aiohttp.ClientSession() as session:
        async with session.get('https://visioncraft.top/models-xl') as response:
            return await response.json()


async def get_models_kb() -> InlineKeyboardMarkup:
    models = await fetch_xl_models()
    buttons = [
        [
            InlineKeyboardButton(
                text=f"{model}",
                callback_data=ModelsSamplersCallback(action="model_selected", choice=f"{model}").pack())
        ] for model in models
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
