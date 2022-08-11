import logging

from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from loader import dp
from keyboards.reply import admin_kb, words_choice_kb
from .get_words import get_all_words
from .add_word import add_word_start


@dp.message_handler(commands=['start', 'apanel'], state='*', is_admin=True)
async def admin_panel(message: Message):
    await message.answer('Admin panel:', reply_markup=admin_kb)


@dp.message_handler(state='*', is_admin=True)
async def apanel_commands(message: Message):
    match message.text:
        case 'Все слова':
            await get_all_words(message)
        case 'Слова':
            await message.answer('Выберите действие:', reply_markup=words_choice_kb)
        case 'Добавить слово':
            await add_word_start(message)
        case 'Изменить слово':
            pass
        case 'Назад':
            await admin_panel(message)
        case 'Статистика пользователя':
            pass
        case 'Настройки':
            pass
        case 'Поддержка':
            pass
        case _:
            logging.error(f'Error admin panel command is not in list: {message}')
            await message.answer('Ошибка админ-панели!')