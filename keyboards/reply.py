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


""" Клавиатура меню """
menu_kb = ReplyKeyboardMarkup(resize_keyboard=True)
train_button = KeyboardButton('Тренировка')
delay_button = KeyboardButton('Задержка')
distribution_button = KeyboardButton('Рассылка')
menu_kb.add(train_button, delay_button)
menu_kb.add(distribution_button)