from aiogram import Bot
from aiogram.methods import DeleteMessage
from aiogram.types import BotCommand

from app.bot.settings import bot_settings

bot = Bot(token=bot_settings.TOKEN)


async def bot_setup(aiogram_bot: Bot) -> None:
    await aiogram_bot.set_my_commands(
        commands=[
            BotCommand(command="start", description="Запуск бота"),
            BotCommand(command="menu", description="Меню бота"),
            BotCommand(command="help", description="Помощь"),
            BotCommand(command="about", description="О боте"),
        ]
    )


async def stop_bot(aiogram_bot: Bot):
    await bot.close()


async def delete_message(chat_id: int, message_id: int):
    await bot(DeleteMessage(chat_id=chat_id, message_id=message_id))