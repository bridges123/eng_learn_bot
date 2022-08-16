import translators as ts
import logging

from aiogram.types import Message, InputFile
from aiogram.dispatcher import FSMContext

from loader import dp
from db import get_random_word, get_translation_choices
from keyboards.inline import translate_choices_kb
from states.user import TranslateWord
from .image_word import create_new_image


async def translate_word(telegram_id: int):
    # добавить добавление текущего слова во временный список, чтобы нельзя было запустить много слов (одинаковые)
    word: str | None = get_random_word()
    if not word:
        logging.error(f'Error all words translated: {word}')
        # добавить обнуление при переводе всех слов !!!!!
        await dp.bot.send_message(telegram_id, 'Ошибка! Ты перевел уже все слова!')
    else:
        translate_choices: list = get_translation_choices(word)
        if not translate_choices:
            logging.error(f'Error no translate choices: {translate_choices}, {word}')
            await dp.bot.send_message(telegram_id, 'Ошибка! Ты перевел уже все слова!')
        else:
            image: str = create_new_image(word)
            msg = await dp.bot.send_photo(telegram_id, InputFile(image),
                                          reply_markup=translate_choices_kb(word, translate_choices))
            cur_state = dp.current_state(chat=telegram_id, user=telegram_id)
            await cur_state.set_state(TranslateWord.active)
            await cur_state.update_data(message_id=msg.message_id)


def google_translate_word(word: str) -> str:
    try:
        translation: str = ts.google(word, from_language='en', to_language='ru')
    except Exception as ex:
        logging.error(f'Error google translate: {ex}')
        translation: str = 'отсутствует'
    return translation
