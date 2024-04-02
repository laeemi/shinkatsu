from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton, BufferedInputFile

from app.callbacks.menu import MenuCallback
from app.core.redis import redis_session
from app.filters.auth_filter import AuthFilter
from app.keyboards.menu import get_api_key_kb
from app.keyboards.models import get_models_kb
from app.keyboards.samplers import get_samplers_kb
from app.services.image_generator import get_image
from app.services.one_time_code_repository import api_key_repository

router = Router()


class ImageGen(StatesGroup):
    input_prompt = State()
    input_api_key = State()


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
        text="Введите api_key: "
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
        text="Введите prompt: "
    )
    await state.set_state(ImageGen.input_prompt)


@router.message(ImageGen.input_prompt, AuthFilter())
async def send_image(message: Message, state: FSMContext):
    # if not regex.prompt.match(message.text):
    #     await message.answer(text="Введен некорректный prompt\n"
    #                               "Попробуйте ещё")
    #     return gen_image
    file = BufferedInputFile(file=await get_image(message.from_user.id, message.text),filename="generated_image.png")
    await message.answer_photo(
        photo=file
    )
    await state.clear()


@router.callback_query(MenuCallback.filter(F.choice == "models"), AuthFilter())
async def select_model(callback: CallbackQuery):
    await callback.message.answer(
        text="Выберите модель",
        reply_markup=await get_models_kb()
    )


@router.callback_query(MenuCallback.filter(F.choice == "samplers"), AuthFilter())
async def select_model(callback: CallbackQuery):
    await callback.message.answer(
        text="Выберите семплер",
        reply_markup=await get_samplers_kb()
    )
