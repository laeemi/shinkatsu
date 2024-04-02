from aiogram import Dispatcher

from app.handlers import base, menu
from app.middlewares.log_middleware import LogMiddleware

dp = Dispatcher()


def registration_dispatcher(dispatcher: Dispatcher) -> None:
    dispatcher.update.middleware(LogMiddleware())
    dispatcher.include_router(base.router)
    dispatcher.include_router(menu.router)
