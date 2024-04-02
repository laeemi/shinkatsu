import asyncio

from app.bot import bot_setup, bot
from app.bot.dispatcher import dp, registration_dispatcher
from app.bot.log import start_logging


async def main():
    await bot_setup(bot)
    start_logging()
    registration_dispatcher(dp)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
