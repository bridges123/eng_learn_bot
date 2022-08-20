import logging
import typing

from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove

from loader import dp
from states.user import AddWord
from states.admin import AdminPanel
from keyboards.reply import add_word_kb, confirm_kb, words_choice_kb, admin_kb
from keyboards.reply import add_button, own_button, confirm_button, cancel_button, back
from services.translation import google_translate_word
from db.words import add_word, add_many_words_in_base


@dp.message_handler(commands=['add_many_words'], state='*', is_admin=True)
async def add_many_words(message: Message):
    await message.answer('Отправьте файл со словами в формате JSON (ключ - слово на eng, значение - перевод):')
    await AddWord.many_words_file.set()


@dp.message_handler(commands=['add_word'], state='*', is_admin=True)
async def add_word_start(message: Message):
    await message.answer('Введите слово, которое хотите добавить:', reply_markup=ReplyKeyboardRemove())
    await AddWord.word_eng.set()


@dp.message_handler(content_types=['document'], state=AddWord.many_words_file, is_admin=True)
async def add_many_words(message: Message):
    doc: dict = message.document
    await message.document.download()
    if doc['mime_type'] == 'application/json' and doc['file_size'] < 50_000_000:
        response: bool = add_many_words_in_base(doc['file_name'])
        if response:
            await message.answer('Слова успешно добавлены.', reply_markup=admin_kb)
        else:
            await message.answer('Ошибка добавления слов.', reply_markup=admin_kb)
    else:
        await message.answer('Неверный формат файла (JSON) или слишком большой размер (50 mb).', reply_markup=admin_kb)
    await AdminPanel.active.set()


@dp.message_handler(content_types=['text'], state=AddWord.word_eng, is_admin=True)
async def add_word_eng(message: Message, state: FSMContext):
    word_eng: str = message.text
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
        case back.text:
            await message.answer('Выберите действие:', reply_markup=words_choice_kb)
            await AdminPanel.active.set()
        case _:
            if answer in ('/apanel', 'start'):
                await message.answer('Admin panel:', reply_markup=admin_kb)
                await AdminPanel.active.set()


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
                response: bool = add_word(word, translation)  # add image path
                if response:
                    await message.answer('Слово успешно добавлено.', reply_markup=words_choice_kb)
                else:
                    await message.answer(f'Ошибка! Не удалось добавить слово.', reply_markup=words_choice_kb)
            else:
                logging.error(f'Error adding word: None values. {data}')
                await message.answer('Ошибка добавления нового слова!', reply_markup=words_choice_kb)
        case cancel_button.text:
            await message.answer('Добавление слова отменено!', reply_markup=words_choice_kb)
        case _:
            logging.error(f'Error confirm new word admin: {answer}')
            await message.answer('Ошибка с подтверждением!', reply_markup=words_choice_kb)
    await AdminPanel.active.set()
