from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove

from loader import dp
from states.admin import UserStats, AdminPanel
from keyboards.reply import search_mode_kb, admin_kb
from keyboards.reply import telegram_id_mode, username_mode, back
from db.user import get_stats_by_telegram_id, get_stats_by_username


@dp.message_handler(commands=['get_stats'], state='*', is_admin=True)
async def get_stats(message: Message):
    await message.answer('Выберите режим поиска:', reply_markup=search_mode_kb)
    await UserStats.choose_mode.set()


@dp.message_handler(state=UserStats.choose_mode, is_admin=True)
async def search_choose_mode(message: Message, state: FSMContext):
    mode: str = message.text
    match mode:
        case telegram_id_mode.text:
            await state.update_data(mode='telegram_id')
            await message.answer('Введите Telegram ID пользователя:', reply_markup=ReplyKeyboardRemove())
            await UserStats.telegram_id.set()
        case username_mode.text:
            await state.update_data(mode='username')
            await message.answer('Введите Username пользователя:', reply_markup=ReplyKeyboardRemove())
            await UserStats.username.set()
        case back.text:
            await AdminPanel.active.set()
            await message.answer('Admin panel:', reply_markup=admin_kb)
        case _:
            if mode in ('/apanel', 'start'):
                await message.answer('Admin panel:', reply_markup=admin_kb)
                await AdminPanel.active.set()


@dp.message_handler(state=UserStats.telegram_id, is_admin=True)
async def stats_by_telegram_id(message: Message):
    telegram_id: str = message.text
    stats: str | None = get_stats_by_telegram_id(telegram_id)
    if not stats:
        await message.answer('Пользователь с таким ID не был найден.', reply_markup=admin_kb)
    else:
        words_total, words_translated, delay = stats
        await message.answer(f'Статистика <b>{telegram_id}</b>:\n'
                             f'Всего слов: {words_total}\n'
                             f'Переведено слов: {words_translated}\n'
                             f'Задержка на рассылку: {delay}',
                             reply_markup=admin_kb)
    await AdminPanel.active.set()


@dp.message_handler(state=UserStats.username, is_admin=True)
async def stats_by_username(message: Message):
    username: str = message.text
    stats: str | None = get_stats_by_username(username)
    if not stats:
        await message.answer('Пользователь с таким Username не был найден.', reply_markup=admin_kb)
    else:
        words_total, words_translated, delay = stats
        await message.answer(f'Статистика <b>{username}</b>:\n'
                             f'Всего слов: {words_total}\n'
                             f'Переведено слов: {words_translated}\n'
                             f'Задержка на рассылку: {delay}',
                             reply_markup=admin_kb)
    await AdminPanel.active.set()