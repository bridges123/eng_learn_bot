import logging
import typing

from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove

from loader import dp
from states.words import AddWord
from keyboards.reply import add_word_kb, add_button, own_button
from keyboards.reply import confirm_kb, confirm_button, cancel_button
from services.translation import google_translate_word
from db import add_word


@dp.message_handler(commands=['start'], state='*', is_admin=True)
async def hello_admin_handler(message: Message):
    await message.answer('Hello admin!')


@dp.message_handler(commands=['add_word'], state='*', is_admin=True)
async def add_word_start(message: Message, state: FSMContext):
    await message.answer('Введите слово, которое хотите добавить:', reply_markup=ReplyKeyboardRemove())
    await AddWord.word_eng.set()


@dp.message_handler(content_types=['text'], state=AddWord.word_eng, is_admin=True)
async def add_word_eng(message: Message, state: FSMContext):
    word_eng: str = message.text
    # translation: str = '123'
    translation: str = google_translate_word(word_eng)
    await state.update_data(word=word_eng)
    await state.update_data(translation=translation)
    await message.answer(f'Предложен перевод: <b>{translation}</b>. Добавить, или предложите свой?',
                         reply_markup=add_word_kb)
    await AddWord.is_translate.set()


@dp.message_handler(content_types=['text'], state=AddWord.is_translate, is_admin=True)
async def add_word_is_translate(message: Message, state: FSMContext):
    answer: str = message.text
    match answer:
        case add_button.text:
            data: typing.Dict = await state.get_data()
            await message.answer(f'Будет добавлено слово <b>{data.get("word")}</b> '
                                 f'с переводом <b>{data.get("translation")}</b>.',
                                 reply_markup=confirm_kb)
            await AddWord.confirm.set()
        case own_button.text:
            await message.answer('Введите свой вариант перевода:', reply_markup=ReplyKeyboardRemove())
            await AddWord.word_rus.set()
        case _:
            logging.error(f'Error adding new word admin: {await state.get_data()}')
            await message.answer('Ошибка добавления нового слова!', reply_markup=ReplyKeyboardRemove())
            await state.finish()


@dp.message_handler(content_types=['text'], state=AddWord.word_rus, is_admin=True)
async def add_word_rus(message: Message, state: FSMContext):
    word_rus: str = message.text
    await state.update_data(translation=word_rus)
    data: typing.Dict = await state.get_data()
    await message.answer(f'Будет добавлено слово <b>{data.get("word")}</b> '
                         f'с переводом <b>{data.get("translation")}</b>.',
                         reply_markup=confirm_kb)
    await AddWord.confirm.set()


@dp.message_handler(content_types=['text'], state=AddWord.confirm, is_admin=True)
async def add_word_confirm(message: Message, state: FSMContext):
    answer: str = message.text
    match answer:
        case confirm_button.text:
            data: typing.Dict = await state.get_data()
            word = data.get('word')
            translation = data.get('translation')
            if word and translation:
                add_word(word, translation, '') # add image path
                await message.answer('Слово успешно добавлено.', reply_markup=ReplyKeyboardRemove())
            else:
                logging.error(f'Error adding word: None values. {data}')
                await message.answer('Ошибка добавления нового слова!', reply_markup=ReplyKeyboardRemove())
        case cancel_button.text:
            await message.answer('Добавление слова отменено!', reply_markup=ReplyKeyboardRemove())
        case _:
            logging.error(f'Error confirm new word admin: {answer}')
            await message.answer('Ошибка с подтверждением!', reply_markup=ReplyKeyboardRemove())
    await state.finish()
