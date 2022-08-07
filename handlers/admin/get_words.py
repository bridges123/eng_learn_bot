import logging
import typing

from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext

from loader import dp
from db import get_words


@dp.message_handler(commands=['get_words'], state='*', is_admin=True)
async def add_word_start(message: Message, state: FSMContext):
    words_list: list = get_words()
    if words_list:
        words: str = '\n'.join([' - '.join([f'<b>{eng}</b>', rus]) for eng, rus in words_list])
        await message.answer(f'Первые 50 слов:\n{words}',
                             reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer('Слова в базе отсутствуют! /add_word - чтобы добавить.',
                             reply_markup=ReplyKeyboardRemove())