from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, BufferedInputFile

from app.callbacks.menu import MenuCallback
from app.callbacks.models_samplers import ModelsSamplersCallback
from app.core.redis import redis_session
from app.filters.auth_filter import AuthFilter
from app.filters.generation_process_filter import GenFilter
from app.filters.timeout_filter import TimeoutFilter
from app.keyboards.menu import get_api_key_kb
from app.keyboards.models import get_models_kb
from app.keyboards.samplers import get_samplers_kb
from app.services.image_generator import get_image
from app.services.one_time_code_repository import api_key_repository, model_repository
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
        text="Введите prompt: "
    )
    await state.set_state(ImageGen.input_prompt)


@router.message(ImageGen.input_prompt, AuthFilter())
async def send_image(message: Message, state: FSMContext):
    # if not regex.prompt.match(message.text):
    #     await message.answer(text="Введен некорректный prompt\n"
    #                               "Попробуйте ещё")
    #     return gen_image
    await state.set_state(ImageGen.generating_image)
    mess = await message.answer(text="⏳Ожидайте ... ", reply_to_message_id=message.message_id)
    try:
        file = BufferedInputFile(file=await get_image(message.from_user.id, message.text),
                                 filename="generated_image.png")
        await mess.delete()
        await message.answer_photo(
            photo=file
        )
        await state.clear()
    except:
        await message.answer(text="❌Упс... что-то пошло не так❌")
        await state.clear()


@router.callback_query(MenuCallback.filter(F.choice == "models"), AuthFilter())
async def select_model(callback: CallbackQuery):
    await callback.message.answer(
        text=f"Список моделей",
        reply_markup=await get_models_kb()
    )


@router.callback_query(ModelsSamplersCallback.filter(F.action == "model_selected"))
async def change_model(callback: CallbackQuery, callback_data: ModelsSamplersCallback):
    model = callback_data.choice
    user_id = callback.from_user.id
    sampler = (await model_repository.get_code(user_id, redis_session)).split("_")[1]
    await model_repository.delete_user(user_id, redis_session)
    await model_repository.set(user_id, f"{model}_{sampler}", redis_session)
    await callback.message.delete()
    await callback.answer("Модель изменена!")


@router.callback_query(MenuCallback.filter(F.choice == "samplers"), AuthFilter())
async def select_sampler(callback: CallbackQuery):
    await callback.message.answer(
        text="Список семплеров",
        reply_markup=await get_samplers_kb()
    )


@router.callback_query(ModelsSamplersCallback.filter(F.action == "sampler_selected"))
async def change_sampler(callback: CallbackQuery, callback_data: ModelsSamplersCallback):
    sampler = callback_data.choice
    user_id = callback.from_user.id
    model = (await model_repository.get_code(user_id, redis_session)).split("_")[0]
    await model_repository.delete_user(user_id, redis_session)
    await model_repository.set(user_id, f"{model}_{sampler}", redis_session)
    await callback.message.delete()
    await callback.answer("Семплер изменен!")
