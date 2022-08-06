import logging
from aiogram.types import Message, CallbackQuery

from loader import dp


@dp.message_handler(commands=['start'], state='*', is_admin=True)
async def hello_admin_handler(message: Message):
    await message.answer('Hello admin!')


@dp.message_handler(commands=['add_word'], state='*', is_admin=True)
async def add_word_handler(message: Message):
    await message.answer('Введите слово, которое хотите добавить:')
    # добавить предложение перевода / или свой