import logging
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext

from loader import dp
from db import get_stats
from states.words import TranslateWord
from keyboards.reply import menu_kb
from services.translation import translate_word


async def menu_stats(message: Message):
    stats: tuple = get_stats(message.from_user.id)
    if not stats:
        logging.error(f'Error get stats: {message.from_user.id}, {stats}')
        await message.answer('Ошибка получения статистики!')
    else:
        words_total, words_translated, delay = stats
        await message.answer('Ваша статистика:\n'
                             f'Всего слов: {words_total}\n'
                             f'Переведено слов: {words_translated}\n'
                             f'Задержка на рассылку: {delay}',
                             reply_markup=menu_kb)


# отлавливание повторного запроса слов
@dp.message_handler(state=TranslateWord.active)
async def repetion_translate_word(message: Message, state: FSMContext):
    # обработка выхода из режима перевода
    if message.text in ('/start', '/menu', 'Статистика'):
        data: typing.Dict = await state.get_data()
        train_message_id: int | None = data.get('message_id')
        if not train_message_id:
            logging.error(f'Error get train message id: {data}, {message}')
            await message.answer('Ошибка закрытия режима тренировки перевода!')
        else:
            try:
                await dp.bot.delete_message(message.from_user.id, train_message_id + 1)
            except Exception as ex:
                logging.error(f'Exception deleting train message: {ex}, {message}')
        await state.finish()
        await menu_stats(message)
    else:
        await message.answer('Ты уже запросил одно слово!')


@dp.message_handler(commands=['start', 'menu'], state='*')
async def get_menu(message: Message):
    await menu_stats(message)


@dp.message_handler(regexp='Тренировка', state='*')
async def train_translate_command(message: Message, state: FSMContext):
    await translate_word(message, state)


@dp.message_handler(regexp='Статистика', state='*')
async def stats_command(message: Message):
    await menu_stats(message)


@dp.message_handler(regexp='Задержка', state='*')
async def delay_command(message: Message):
    pass


@dp.message_handler(regexp='Рассылка', state='*')
async def distribution_command(message: Message):
    pass
