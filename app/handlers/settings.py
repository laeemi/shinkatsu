from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.callbacks.menu import MenuCallback
from app.callbacks.models_samplers import ModelsSamplersCallback
from app.callbacks.settings import SettingsCallback
from app.core.redis import redis_session
from app.filters.auth_filter import AuthFilter
from app.filters.generation_process_filter import GenFilter
from app.handlers.base import menu
from app.keyboards.settings import get_settings_kb, get_negative_prompt_kb, get_negative_prompt_cancel_kb, \
    get_num_of_imgs_kb
from app.keyboards.models import get_models_kb
from app.keyboards.samplers import get_samplers_kb
from app.services.one_time_code_repository import model_repository, negative_prompt_repository, images_count_repository
from app.states.change_settings import ChangeSettings

router = Router()
router.callback_query.filter(GenFilter(), AuthFilter())
router.message.filter(GenFilter(), AuthFilter())


@router.message(ChangeSettings.input_n_prompt)
async def save_n_prompt(message: Message, state: FSMContext):
    code = message.text
    if code is None:
        await message.answer(text="Необходимо ввести текст, попробуйте ещё!")
        await negative_prompt_change
    else:
        await negative_prompt_repository.set(message.from_user.id, code, redis_session)
        await message.answer(
            text="Негативный Prompt сменён!"
        )
        await state.clear()


@router.callback_query(MenuCallback.filter(F.choice == "settings"))
async def ai_settings(callback: CallbackQuery):
    await callback.message.edit_text(
        text="⚙️Настройки",
        reply_markup=get_settings_kb()
    )


@router.callback_query(SettingsCallback.filter(F.choice == "negative_prompt"))
async def show_negative_prompt(callback: CallbackQuery):
    n_prompt = await negative_prompt_repository.get_code(callback.from_user.id, redis_session)
    await callback.message.edit_text(
        text=f"Ваш Негативный Prompt - {n_prompt if n_prompt is not None else 'Отсутствует'}",
        reply_markup=get_negative_prompt_kb()
    )


@router.callback_query(SettingsCallback.filter(F.choice == "change_n_prompt"))
async def negative_prompt_change(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text="Введите Негативный Prompt: ",
        reply_markup=get_negative_prompt_cancel_kb()
    )
    await state.set_state(ChangeSettings.input_n_prompt)


@router.callback_query(SettingsCallback.filter(F.choice == "n_prompt_cancel"))
async def negative_prompt_cancel(callback: CallbackQuery):
    return await show_negative_prompt(callback)


@router.callback_query(SettingsCallback.filter(F.choice == "n_prompt_back"))
async def negative_prompt_back(callback: CallbackQuery):
    return await ai_settings(callback)


@router.callback_query(SettingsCallback.filter(F.choice == "settings_back"))
async def negative_prompt_back(callback: CallbackQuery):
    await callback.message.delete()
    return await menu(callback.message)


@router.callback_query(SettingsCallback.filter(F.choice == "imgs_count"))
async def images_count(callback: CallbackQuery):
    num = await images_count_repository.get_code(callback.from_user.id, redis_session)
    await callback.message.edit_text(
        text=f"Выбранное число изображений - {num if num is not None else '3'}",
        reply_markup=get_num_of_imgs_kb()
    )


@router.callback_query(SettingsCallback.filter(F.choice == "num_of_imgs_back"))
async def images_count_back(callback: CallbackQuery):
    return await ai_settings(callback)


@router.callback_query(SettingsCallback.filter(F.choice == "change_count"))
async def change_images_count(callback: CallbackQuery, callback_data: SettingsCallback):
    await images_count_repository.set(callback.from_user.id, callback_data.count, redis_session)
    await callback.message.answer(
        text="Количество изображений сменено!"
    )


@router.callback_query(SettingsCallback.filter(F.choice == "models"))
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


@router.callback_query(SettingsCallback.filter(F.choice == "samplers"))
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
