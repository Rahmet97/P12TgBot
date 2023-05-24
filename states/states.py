from aiogram.dispatcher.filters.state import StatesGroup, State


class UserState(StatesGroup):
    phone = State()
    full_name = State()
    age = State()
