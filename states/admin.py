from aiogram.dispatcher.filters.state import State, StatesGroup


class AdminPanel(StatesGroup):
    active = State()


class UserStats(StatesGroup):
    choose_mode = State()
    telegram_id = State()
    username = State()