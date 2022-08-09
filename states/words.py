from aiogram.dispatcher.filters.state import State, StatesGroup


class AddWord(StatesGroup):
    word_eng = State()
    word_rus = State()
    is_translate = State()
    confirm = State()


class EditWord(StatesGroup):
    word_eng = State()
    edited_word_eng = State()
    edited_word_rus = State()
    is_translate = State()
    confirm = State()


class TrainWord(StatesGroup):
    active = State()