import logging
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext

from loader import dp
from db import get_stats_by_telegram_id
from states.words import TranslateWord, UserMenu
from states.admin import AdminPanel
from keyboards.reply import menu_kb, admin_kb
from services.translation import translate_word


async def menu_stats(message: Message):
    stats: tuple = get_stats_by_telegram_id(message.from_user.id)
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


@dp.message_handler(commands=['apanel'], state='*')
async def get_apanel(message: Message):
    await message.answer('Admin panel:', reply_markup=admin_kb)
    await AdminPanel.active.set()


@dp.message_handler(commands=['start', 'menu'], state='*')
async def get_menu(message: Message):
    await UserMenu.active.set()
    await menu_stats(message)


@dp.message_handler(content_types=['text'], state=UserMenu.active)
async def menu_commands(message: Message, state: FSMContext):
    match message.text:
        case 'Тренировка':
            await translate_word(message, state)
        case 'Статистика':
            await menu_stats(message)
        case 'Задержка':
            pass
        case 'Рассылка':
            pass
        case _:
            await message.answer('Такой команды нет. Попробуйте /menu')
