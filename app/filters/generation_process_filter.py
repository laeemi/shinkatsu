from aiogram.filters import BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Update
from app.states.image_gen import ImageGen


class GenFilter(BaseFilter):
    def __init__(self):
        super().__init__()

    async def __call__(self, update: Update, state: FSMContext) -> bool:
        return await state.get_state() != ImageGen.generating_image
