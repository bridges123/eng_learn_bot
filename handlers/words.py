import logging
from aiogram.types import Message, CallbackQuery

from loader import dp
from utils import translate_word
from keyboards.inline import word_kb
from keyboards.callback import word_callback


@dp.message_handler(commands=['word'], state='*')
async def word_command(message: Message):
    await message.answer('Знаешь слово suck?', reply_markup=word_kb('suck'))


@dp.callback_query_handler(word_callback.filter(), state='*')
async def word_callback_know(call: CallbackQuery, callback_data: dict):  # state: FSMContext
    """ Обработка callback's от word_keyboard """
    await call.answer(cache_time=60)
    logging.info(callback_data)
    translation: str = translate_word(callback_data.get('answer'))
    if not translation:
        translation = 'отсутствует'
    answer: str = callback_data.get('answer')
    msg: str
    match answer:
        case 'yes':
            msg = f'Ты угадал, молодец! Перевод: {translation}'
            # пометки для бд
        case 'no':
            msg = f'Запоминай новое слово! Перевод: {translation}'
            # пометки для бд
        case _:
            msg = 'Ошибка!'
            logging.error(f'Error with answer in callback_data: {callback_data}')
    # pass in bd
    await call.message.edit_text(msg)
