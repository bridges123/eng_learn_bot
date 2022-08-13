from aiogram.dispatcher.filters.state import State, StatesGroup


class UserStats(StatesGroup):
    choose_mode = State()
    telegram_id = State()
    username = State()