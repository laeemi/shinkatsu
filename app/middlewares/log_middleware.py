import logging
from datetime import datetime, timedelta
from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery, Update


class LogMiddleware(BaseMiddleware):
    @staticmethod
    def message_bot_log(message: Message, update: Update) -> None:
        logging.info(f'-------------------------------------------------------------------------------\n'
                     f'Пользователь: {message.from_user.full_name}\n'
                     f'Написал: {message.text}\n'
                     f'Chat_ID(ID): {message.chat.id}\n'
                     f'Ссылка: {message.from_user.username}\n'
                     f'Время: {datetime.utcnow() + timedelta(hours=3)}\n'
                     f'Время сообщения: {message.date + timedelta(hours=3)}\n'
                     f'Update id={update.update_id}'
                     )

    @staticmethod
    def callback_bot_log(callback: CallbackQuery, update: Update) -> None:
        logging.info(f'-------------------------------------------------------------------------------\n'
                     f'Пользователь: {callback.from_user.full_name}\n'
                     f'Отправил callback: {callback.data}\n'
                     f'Chat_ID(ID): {callback.from_user.id}\n'
                     f'Ссылка: {callback.from_user.username}\n'
                     f'Время: {datetime.utcnow() + timedelta(hours=3)}\n'
                     f'Update id={update.update_id}'
                     )

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        if isinstance(event, Update):

            if event.message is not None:
                self.message_bot_log(event.message, event)
            elif event.callback_query is not None:
                self.callback_bot_log(event.callback_query, event)
            logging.info(f'Update: id={event.update_id}\n'
                         f'-------------------------------------------------------------------------------\n')
        return await handler(event, data)
