import logging
from aiogram.types import Message

from db.user import get_stats_by_telegram_id
from keyboards.reply import menu_kb


async def menu_stats(message: Message):
    stats: tuple = get_stats_by_telegram_id(message.from_user.id)
    if not stats:
        logging.error(f'Error get stats: {message.from_user.id}, {stats}')
        await message.answer('Ошибка получения статистики!')
    else:
        words_total, words_translated, delay = stats
        await message.answer(f'<b>Всего слов:</b> <i>{words_total}</i>\n'
                             f'<b>Переведено слов:</b> <i>{words_translated}</i>\n'
                             f'<b>Задержка на рассылку:</b> <i>{delay} мин</i>',
                             reply_markup=menu_kb)
        