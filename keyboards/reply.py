from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


""" Клавиатура подтверждения """
confirm_kb = ReplyKeyboardMarkup(resize_keyboard=True)
confirm_button = KeyboardButton('Подтвердить')
cancel_button = KeyboardButton('Отменить')
confirm_kb.add(confirm_button, cancel_button)


""" Клавиатура меню """
menu_kb = ReplyKeyboardMarkup(resize_keyboard=True)
train_button = KeyboardButton('Тренировка')
stats = KeyboardButton('Статистика')
delay_button = KeyboardButton('Задержка')
distribution_button = KeyboardButton('Рассылка')
menu_kb.add(train_button, stats)
menu_kb.add(delay_button, distribution_button)


""" Клавиатура админа """
admin_kb = ReplyKeyboardMarkup(resize_keyboard=True)
words = KeyboardButton('Слова')
get_stats = KeyboardButton('Статистика пользователя')
# add edit admin staffdfxb
# settings = KeyboardButton('Настройки')
# support = KeyboardButton('Поддержка')
admin_kb.add(words, get_stats)
# admin_kb.add(settings, support)


""" Клавиатура выбора под-меню 'Слова' """
words_choice_kb = ReplyKeyboardMarkup(resize_keyboard=True)
all_words = KeyboardButton('Все слова')
add_word = KeyboardButton('Добавить слово')
change_word = KeyboardButton('Изменить/Удалить')
back = KeyboardButton('Назад')
words_choice_kb.add(all_words, add_word)
words_choice_kb.add(change_word, back)


""" Клавиатура выбора режима добавления слов """
add_mode_kb = ReplyKeyboardMarkup(resize_keyboard=True)
one_word_button = KeyboardButton('Одно слово')
many_word_button = KeyboardButton('Много слов')
add_mode_kb.add(one_word_button, many_word_button)
add_mode_kb.add(back)


""" Клавиатура добавления нового слова """
add_word_kb = ReplyKeyboardMarkup(resize_keyboard=True)
add_button = KeyboardButton('Добавить')
own_button = KeyboardButton('Свой перевод')
add_word_kb.add(add_button, own_button)
add_word_kb.add(back)


""" Клавиатура выбора действия со словом """
edit_choice_kb = ReplyKeyboardMarkup(resize_keyboard=True)
edit_translate_button = KeyboardButton('Изменить перевод')
delete_word_button = KeyboardButton('Удалить слово')
edit_choice_kb.add(edit_translate_button, delete_word_button)


""" Клавиатура выбора режима поиска пользователя """
search_mode_kb = ReplyKeyboardMarkup(resize_keyboard=True)
telegram_id_mode = KeyboardButton('Telegram ID')
username_mode = KeyboardButton('Username')
search_mode_kb.add(telegram_id_mode, username_mode)
search_mode_kb.add(back)


""" Клавиатура 'Назад' """
back_kb = ReplyKeyboardMarkup(resize_keyboard=True)
back_kb.add(back)


""" Клавиатура выбора изменения задержки """
delay_choice_kb = ReplyKeyboardMarkup(resize_keyboard=True)
change_button = KeyboardButton('Изменить')
delay_choice_kb.add(change_button, back)