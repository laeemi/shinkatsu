from aiogram.fsm.state import StatesGroup, State


class ChangeSettings(StatesGroup):
    input_n_prompt = State()
