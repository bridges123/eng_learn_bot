from aiogram.dispatcher.filters.state import State, StatesGroup


class AddWord(StatesGroup):
    word_eng = State()
    word_rus = State()
    is_translate = State()
    confirm = State()


class EditWord(StatesGroup):
    word_eng = State()
    edit_choice = State()
    edited_translation = State()
    edit_confirm = State()


class TranslateWord(StatesGroup):
    active = State()