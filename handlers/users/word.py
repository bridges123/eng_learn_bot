import logging
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext

from loader import dp
from db import add_word_to_guessed, translate_word, get_random_word, get_translation_choices
from db import update_total_words_count, update_translated_words_count
from keyboards.inline import translate_choices_kb
from keyboards.callback import word_callback
from states.words import TrainWord


# отлавливание повторного запроса слов
@dp.message_handler(commands=['word'], state=TrainWord.active)
async def repetion_train_word(message: Message):
    await message.answer('Ты уже запросил одно слово!')


# функция вызова запроса слова для перевода
@dp.message_handler(commands=['word'], state='*')
async def train_word(message: Message):
    # добавить добавление текущего слова во временный список, чтобы нельзя было запустить много слов (одинаковые)
    word: str | None = get_random_word()
    if not word:
        logging.error(f'Error all words translated: {word}')
        # добавить обнуление при переводе всех слов
        await message.answer('Ошибка! Ты перевел уже все слова!')
    else:
        translate_choices: list = get_translation_choices(word)
        await message.answer(f'Знаешь слово <b>{word}</b>?', reply_markup=translate_choices_kb(translate_choices))
        await TrainWord.active.set()


# обработка ответа (перевода слова)
@dp.callback_query_handler(word_callback.filter(), state='*')
async def word_callback_know(call: CallbackQuery, callback_data: dict, state: FSMContext):  # state: FSMContext
    """ Обработка callback's от word_keyboard """
    await call.answer(cache_time=60)
    word: str | None = callback_data.get('word')
    if not word:
        logging.error(f'Error get word of callback_data: {word}, {callback_data}')
        await message.answer('Ошибка с выборкой слова (callback)!')
    translation: str | None = translate_word(word)
    if not translation:
        logging.error(f'Error not translation: {translation}')
        translation = 'отсутствует'
    answer: str = callback_data.get('answer')
    telegram_id: int = call.from_user.id
    msg: str
    match answer:
        case 'yes':
            msg = f'Ты угадал, молодец! Перевод: <b>{translation}</b>'
            # Добавляем угаданное слово в фильтр-таблицу и инкременируем счётчики
            add_word_to_guessed(telegram_id, word)
            update_translated_words_count(telegram_id)
            update_total_words_count(telegram_id)
        case 'no':
            msg = f'Запоминай новое слово! Перевод: <b>{translation}</b>'
            update_total_words_count(telegram_id)
        case _:
            msg = 'Ошибка!'
            logging.error(f'Error with answer in callback_data: {callback_data}')
    # pass in bd ???
    await state.finish()
    await call.message.edit_text(msg)
