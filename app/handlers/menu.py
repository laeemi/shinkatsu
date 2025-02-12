import logging
import traceback

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, BufferedInputFile, InputMediaPhoto

from app.callbacks.menu import MenuCallback
from app.callbacks.settings import SettingsCallback
from app.core.redis import redis_session
from app.filters.auth_filter import AuthFilter
from app.filters.generation_process_filter import GenFilter
from app.filters.timeout_filter import TimeoutFilter
from app.keyboards.menu import get_api_key_kb
from app.keyboards.settings import get_prompt_cancel_kb
from app.services.image_generator import get_image
from app.services.one_time_code_repository import api_key_repository
from app.states.image_gen import ImageGen

router = Router()
router.callback_query.filter(GenFilter())
router.message.filter(GenFilter())


@router.callback_query(TimeoutFilter())
async def timeout(message: Message):
    await message.answer(text=f"🕒Время ожидания: 5 минут")


@router.callback_query(MenuCallback.filter(F.choice == "api_key"), AuthFilter())
async def change_api_key(callback: CallbackQuery):
    api_key = await api_key_repository.get_code(callback.from_user.id, redis_session)
    await callback.message.answer(
        text=f"Ваш API KEY: {api_key}",
        reply_markup=get_api_key_kb()
    )


@router.callback_query(MenuCallback.filter(F.choice == "api_key"))
async def input_api_key(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        text="Получить API KEY - @VisionCraft_bot\n"
             "Введите api key: "
    )
    await state.set_state(ImageGen.input_api_key)


@router.message(ImageGen.input_api_key)
async def save_api_key(message: Message, state: FSMContext):
    if len(message.text) < 10:
        await message.answer(text="Некорректный api key\n"
                                  "Попробуйте ещё")
        return input_api_key
    await api_key_repository.set(message.from_user.id, message.text, redis_session)
    await message.answer(
        text="api key сохранен!"
    )
    await state.clear()


@router.callback_query(MenuCallback.filter(F.choice == "gen"), AuthFilter())
async def gen_image(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        text="Введите Prompt (на английском): ",
        reply_markup=get_prompt_cancel_kb()
    )
    await state.set_state(ImageGen.input_prompt)


@router.callback_query(ImageGen.input_prompt, SettingsCallback.filter(F.choice == "prompt_cancel"), AuthFilter())
async def prompt_input_cancel(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.answer()
    await state.clear()


@router.message(ImageGen.input_prompt, AuthFilter())
async def send_image(message: Message, state: FSMContext):
    # if not regex.prompt.match(message.text):
    #     await message.answer(text="Введен некорректный prompt\n"
    #                               "Попробуйте ещё")
    #     return gen_image
    await state.set_state(ImageGen.generating_image)
    mess = await message.answer(text="⏳Ожидайте ... ", reply_to_message_id=message.message_id)
    try:
        images = await get_image(message.from_user.id, message.text)
        media = [InputMediaPhoto(
            media=BufferedInputFile(file=image, filename="generated_image.png")
        ) for image in images]
        await mess.delete()
        await message.answer_media_group(
            media=media
        )
        await state.clear()
    except:
        logging.info(f"ERROR TRACEBACK: {traceback.format_exc()}")
        await message.answer(text="❌Упс... что-то пошло не так❌")
        await state.clear()
