import aiohttp
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.callbacks.models_samplers import ModelsSamplersCallback


async def fetch_xl_samplers():
    """Get all available samplers for SDXL models"""
    async with aiohttp.ClientSession() as session:
        async with session.get('https://visioncraft.top/samplers-xl') as response:
            return await response.json()


async def get_samplers_kb() -> InlineKeyboardMarkup:
    samplers = await fetch_xl_samplers()
    buttons = [
        [
            InlineKeyboardButton(
                text=f"{sampler}",
                callback_data=ModelsSamplersCallback(action="sampler_selected", choice=f"{sampler}").pack())
        ] for sampler in samplers
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
