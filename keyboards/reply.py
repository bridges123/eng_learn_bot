from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


""" Клавиатура добавления нового слова """
add_word_kb = ReplyKeyboardMarkup(resize_keyboard=True)
add_button = KeyboardButton('Добавить')
own_button = KeyboardButton('Свой перевод')
add_word_kb.add(add_button, own_button)


""" Клавиатура подтверждения """
confirm_kb = ReplyKeyboardMarkup(resize_keyboard=True)
confirm_button = KeyboardButton('Подтвердить')
cancel_button = KeyboardButton('Отменить')
confirm_kb.add(confirm_button, cancel_button)