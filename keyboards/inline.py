from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from random import shuffle

from .callback import word_callback


def translate_choices_kb(word: str, choices: list) -> InlineKeyboardMarkup:
    """ Клавиатура с вариантами перевода слова """
    row_width: int = 2
    lenght: int = len(choices)
    # список кнопок, и последняя - верный callback
    buttons: list = [
        InlineKeyboardButton(choices[i], callback_data=word_callback.new(answer='no', word=word))
        for i in range(lenght - 1)
    ]
    buttons.append(InlineKeyboardButton(choices[-1], callback_data=word_callback.new(answer='yes', word=word)))
    # Перемешивание вариантов и построение клавиатуры
    shuffle(buttons)
    keyboard: list = [[buttons[row_width * i + j] for j in range(row_width)] for i in range(lenght // row_width)]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
