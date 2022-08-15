import logging
from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from loader import dp
from db import get_stats_by_telegram_id
from keyboards.reply import menu_kb


async def menu_stats(message: Message):
    stats: tuple = get_stats_by_telegram_id(message.from_user.id)
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