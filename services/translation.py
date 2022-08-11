import translators as ts
import logging

from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from db import get_random_word, get_translation_choices
from keyboards.inline import translate_choices_kb
from states.words import TranslateWord


async def translate_word(message: Message, state: FSMContext):
    # добавить добавление текущего слова во временный список, чтобы нельзя было запустить много слов (одинаковые)
    word: str | None = get_random_word()
    if not word:
        logging.error(f'Error all words translated: {word}')
        # добавить обнуление при переводе всех слов !!!!!
        await message.answer('Ошибка! Ты перевел уже все слова!')
    else:
        translate_choices: list = get_translation_choices(word)
        if not translate_choices:
            logging.error(f'Error no translate choices: {translate_choices}, {word}')
            await message.answer('Ошибка! Ты перевел уже все слова!')
        else:
            await message.answer(f'Знаешь слово <b>{word}</b>?', reply_markup=translate_choices_kb(word, translate_choices))
            await TranslateWord.active.set()
            await state.update_data(message_id=message.message_id)


def google_translate_word(word: str) -> str:
    try:
        translation: str = ts.google(word, from_language='en', to_language='ru')
    except Exception as ex:
        translation: str = 'отсутствует'
        logging.error(f'Error google translate: {ex}')
    return translation
