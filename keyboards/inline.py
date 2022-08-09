from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from random import shuffle

from .callback import word_callback


def translate_choices_kb(choices: list) -> InlineKeyboardMarkup:
    # row width = 2
    lenght: int = len(choices)
    res: list = [
        InlineKeyboardButton(choices[i], callback_data=word_callback.new(answer='no', word=choices[i]))
        for i in range(lenght - 1)
    ]
    res.append(InlineKeyboardButton(choices[-1], callback_data=word_callback.new(answer='yes', word=choices[-1])))
    shuffle(res)
    keyboard: list = [[res[2 * i + j] for j in range(2)] for i in range(lenght // 2)]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
