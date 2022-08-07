import logging
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove

from loader import dp
from keyboards.reply import menu_kb
from db import get_stats
from .word import train_word


@dp.message_handler(commands=['menu'], state='*')
async def menu(message: Message):
    stats: tuple = get_stats(message.from_user.id)
    if not stats:
        logging.error(f'Error get stats: {message.from_user.id}, {stats}')
        await message.answer('Ошибка получения статистики!')
    else:
        words_total, words_translated, delay = stats
        await message.answer('Ваша статистика:\n'
                             f'Всего слов: {words_total}\n'
                             f'Переведено слов: {words_translated}\n'
                             f'Задержка на рассылку: {delay}',
                             reply_markup=menu_kb)


@dp.message_handler(regexp='Тренировка', state='*')
async def train_command(message: Message):
    await train_word(message)


@dp.message_handler(regexp='Задержка', state='*')
async def delay_command(message: Message):
    pass


@dp.message_handler(regexp='Рассылка', state='*')
async def distribution_command(message: Message):
    pass
