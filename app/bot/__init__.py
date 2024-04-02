from aiogram import Bot
from aiogram.types import BotCommand

from app.bot.settings import bot_settings

bot = Bot(token=bot_settings.TOKEN)


async def bot_setup(aiogram_bot: Bot) -> None:
    await aiogram_bot.set_my_commands(
        commands=[
            BotCommand(command="start", description="Запуск бота"),
            BotCommand(command="menu", description="Меню бота"),
            BotCommand(command="about", description="О боте"),
        ]
    )


async def stop_bot(aiogram_bot: Bot):
    await bot.close()
