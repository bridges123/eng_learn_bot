import logging
import typing

from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext

from loader import dp
from db import add_word_to_guessed, get_word_translation, update_total_words_count, update_translated_words_count
from keyboards.callback import word_callback


# обработка ответа (перевода слова)
@dp.callback_query_handler(word_callback.filter(), state='*')
async def word_callback_know(call: CallbackQuery, callback_data: dict, state: FSMContext):
    """ Обработка callback's от word_keyboard """
    await call.answer(cache_time=60)
    word: str | None = callback_data.get('word')
    if not word:
        logging.error(f'Error get word of callback_data: {word}, {callback_data}')
        await message.answer('Ошибка с выборкой слова (callback)!')
    translation: str | None = get_word_translation(word)
    if not translation:
        logging.error(f'Error not translation: {translation}')
        translation = 'отсутствует'
    answer: str = callback_data.get('answer')
    telegram_id: int = call.from_user.id
    msg: str
    match answer:
        case 'yes':
            msg = f'Молодец! Ты угадал: <b>{word} - {translation}</b>'
            # Добавляем угаданное слово в фильтр-таблицу и инкременируем счётчики
            add_word_to_guessed(telegram_id, word)
            update_translated_words_count(telegram_id)
            update_total_words_count(telegram_id)
        case 'no':
            msg = f'Неверно! Запоминай новое слово: <b>{word} - {translation}</b>'
            update_total_words_count(telegram_id)
        case _:
            msg = 'Ошибка!'
            logging.error(f'Error with answer in callback_data: {callback_data}')
    # pass in bd ???
    await state.finish()
    await call.message.edit_text(msg)
