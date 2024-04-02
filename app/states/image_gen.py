from aiogram.fsm.state import StatesGroup, State


class ImageGen(StatesGroup):
    input_prompt = State()
    generating_image = State()
    input_api_key = State()
