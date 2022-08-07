import logging
from aiogram.types import Message, CallbackQuery

from loader import dp
from db import translate_word, get_random_word
from db import update_total_words_count, update_translated_words_count
from keyboards.inline import get_word_kb
from keyboards.callback import word_callback


@dp.message_handler(commands=['word'], state='*')
async def train_word(message: Message):
    # добавить добавление текущего слова во временный список, чтобы нельзя было запустить много слов (одинаковые)
    word = get_random_word()
    if not word:
        logging.error(f'Error get random word: {word}')
        await message.answer('Ошибка с подбором слова!')
    else:
        word = word[0]
        await message.answer(f'Знаешь слово <b>{word}</b>?', reply_markup=get_word_kb(word))


@dp.callback_query_handler(word_callback.filter(), state='*')
async def word_callback_know(call: CallbackQuery, callback_data: dict):  # state: FSMContext
    """ Обработка callback's от word_keyboard """
    await call.answer(cache_time=60)
    translation = translate_word(callback_data.get('word'))
    if translation:
        translation = translation[0]
    else:
        translation = 'отсутствует'
    answer: str = callback_data.get('answer')
    telegram_id: int = call.from_user.id
    msg: str
    match answer:
        # добавить запоминание неотгаданных слов
        case 'yes':
            msg = f'Ты угадал, молодец! Перевод: <b>{translation}</b>'
            update_translated_words_count(telegram_id)
            update_total_words_count(telegram_id)
        case 'no':
            msg = f'Запоминай новое слово! Перевод: <b>{translation}</b>'
            update_total_words_count(telegram_id)
        case _:
            msg = 'Ошибка!'
            logging.error(f'Error with answer in callback_data: {callback_data}')
    # pass in bd
    await call.message.edit_text(msg)
