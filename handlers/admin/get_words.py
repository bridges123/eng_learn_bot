from aiogram.types import Message

from loader import dp
from db.words import get_words


@dp.message_handler(commands=['get_words'], state='*', is_admin=True)
async def get_all_words(message: Message):
    words_list: list = get_words()
    if words_list:
        words: str = '\n'.join([' - '.join([f'<b>{eng}</b>', rus]) for eng, rus in words_list])
        await message.answer(f'Первые 50 слов:\n{words}')
    else:
        await message.answer('Слова в базе отсутствуют! /add_word - чтобы добавить.')