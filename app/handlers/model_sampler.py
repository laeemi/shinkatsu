from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.callbacks.menu import MenuCallback
from app.callbacks.models_samplers import ModelsSamplersCallback
from app.core.redis import redis_session
from app.filters.auth_filter import AuthFilter
from app.filters.generation_process_filter import GenFilter
from app.keyboards.models import get_models_kb
from app.keyboards.samplers import get_samplers_kb
from app.services.one_time_code_repository import model_repository

router = Router()
router.callback_query.filter(GenFilter())
router.message.filter(GenFilter())


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
