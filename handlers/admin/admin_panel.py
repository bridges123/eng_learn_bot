import logging

from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from loader import dp
from keyboards.reply import admin_kb, words_choice_kb
from states.admin import AdminPanel
from states.user import UserMenu
from services.menu import menu_stats
from .get_words import get_all_words
from .add_word import add_mode_choice
from .edit_word import edit_word_start
from .user_stats import get_stats


@dp.message_handler(commands=['apanel'], state='*', is_admin=True)
async def admin_panel(message: Message):
    await message.answer('Admin panel:', reply_markup=admin_kb)
    await AdminPanel.active.set()


@dp.message_handler(commands=['start', 'menu'], state='*', is_admin=True)
async def user_menu(message: Message):
    await UserMenu.active.set()
    await menu_stats(message)


@dp.message_handler(state=AdminPanel.active, is_admin=True)
async def apanel_commands(message: Message):
    match message.text:
        case 'Все слова':
            await get_all_words(message)
        case 'Слова':
            await message.answer('Выберите действие:', reply_markup=words_choice_kb)
        case 'Добавить слово':
            await add_mode_choice(message)
        case 'Изменить/Удалить':
            await edit_word_start(message)
        case 'Назад':
            await admin_panel(message)
        case 'Статистика пользователя':
            await get_stats(message)
        # add edit admin staff
        # case 'Настройки':
        #     pass
        case _:
            await message.answer('Такой команды нет. Попробуйте /apanel')
