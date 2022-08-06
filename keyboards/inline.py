from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from .callback import word_callback


def word_kb(word: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton('Знаю', callback_data=word_callback.new(answer='yes', word=word)),
                InlineKeyboardButton('Не знаю', callback_data=word_callback.new(answer='no', word=word)),
            ],
        ]
    )
