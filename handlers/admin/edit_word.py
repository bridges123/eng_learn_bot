import logging
import typing

from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove

from loader import dp
from states.words import EditWord
from states.admin import AdminPanel
from keyboards.reply import words_choice_kb, edit_choice_kb, confirm_kb
from keyboards.reply import edit_translate_button, delete_word_button, confirm_button, cancel_button
from db import get_check_word, edit_word_translation, delete_word


@dp.message_handler(commands=['edit_word'], state='*', is_admin=True)
async def edit_word_start(message: Message):
    await message.answer('Введите слово, которое хотите изменить:', reply_markup=ReplyKeyboardRemove())
    await EditWord.word_eng.set()


@dp.message_handler(content_types=['text'], state=EditWord.word_eng, is_admin=True)
async def edit_word_eng(message: Message, state: FSMContext):
    word_eng: str = message.text
    checked_word: str | None = get_check_word(word_eng)
    if not checked_word:
        logging.error(f'Error not find gived word {checked_word}')
        await message.answer('Ошибка! Слово не было найдено.', reply_markup=words_choice_kb)
        await AdminPanel.active.set()
    else:
        await state.update_data(word=checked_word)
        await message.answer(f'Слово <b>{checked_word}</b> найдено. Выберите действие:', reply_markup=edit_choice_kb)
        await EditWord.edit_choice.set()


@dp.message_handler(content_types=['text'], state=EditWord.edit_choice, is_admin=True)
async def edit_delete_choice(message: Message, state: FSMContext):
    data: typing.Dict = await state.get_data()
    choice: str = message.text
    match choice:
        case edit_translate_button.text:
            await message.answer('Введите новый перевод слова:', reply_markup=ReplyKeyboardRemove())
            await EditWord.edited_translation.set()
        case delete_word_button.text:
            word: str | None = data.get('word')
            if not word:
                logging.error(f'Error get word in choice func {data}, {choice}')
                await message.answer('Ошибка получения слова!', reply_markup=words_choice_kb)
            else:
                response: bool = delete_word(word)
                if response:
                    await message.answer(f'Слово <b>{word}</b> удалено.', reply_markup=words_choice_kb)
                else:
                    await message.answer(f'Ошибка! Не удалось удалить слово.', reply_markup=words_choice_kb)
            await AdminPanel.active.set()
        case _:
            if choice in ('/apanel', 'start'):
                await message.answer('Admin panel:', reply_markup=admin_kb)
                await AdminPanel.active.set()


@dp.message_handler(content_types=['text'], state=EditWord.edited_translation, is_admin=True)
async def edit_new_translation(message: Message, state: FSMContext):
    new_translation: str = message.text
    await state.update_data(translation=new_translation)
    data: typing.Dict = await state.get_data()
    await message.answer(f'Перевод слова <b>{data.get("word")}</b> '
                         f'будет изменён на <b>{data.get("translation")}</b>.',
                         reply_markup=confirm_kb)
    await EditWord.edit_confirm.set()


@dp.message_handler(content_types=['text'], state=EditWord.edit_confirm, is_admin=True)
async def edit_word_confirm(message: Message, state: FSMContext):
    answer: str = message.text
    match answer:
        case confirm_button.text:
            data: typing.Dict = await state.get_data()
            word = data.get('word')
            translation = data.get('translation')
            if word and translation:
                # add get edited image
                response: bool = edit_word_translation(word, translation, '')
                if response:
                    await message.answer('Перевод успешно изменён.', reply_markup=words_choice_kb)
                else:
                    await message.answer('Ошибка! Не удалось изменить перевод.', reply_markup=words_choice_kb)
            else:
                logging.error(f'Error adding word: None values. {data}')
                await message.answer('Ошибка добавления нового слова!', reply_markup=words_choice_kb)
        case cancel_button.text:
            await message.answer('Добавление слова отменено!', reply_markup=words_choice_kb)
        case _:
            logging.error(f'Error confirm new word admin: {answer}')
            await message.answer('Ошибка с подтверждением!', reply_markup=words_choice_kb)
    await AdminPanel.active.set()