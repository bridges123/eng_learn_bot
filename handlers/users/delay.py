import logging
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext

from loader import dp
from db import get_current_delay, set_new_delay
from states.user import Delay, UserMenu
from keyboards.reply import delay_choice_kb, menu_kb, back_kb
from keyboards.reply import change_button, back
from services.menu import menu_stats


async def set_delay(message: Message):
    cur_delay: int = get_current_delay(message.from_user.id)
    if cur_delay:
        await message.answer(f'Ваша задержка: <b>{cur_delay}</b> мин. Желаете изменить?', reply_markup=delay_choice_kb)
        await Delay.change_choice.set()
    else:
        await message.answer('Введите желаемую задержку на рассылку (в минутах):', reply_markup=back_kb)
        await Delay.set_delay.set()


@dp.message_handler(state=Delay.change_choice)
async def choice_change_delay(message: Message):
    match message.text:
        case change_button.text:
            await message.answer('Введите желаемую задержку на рассылку (в минутах):',
                                 reply_markup=back_kb)
            await Delay.set_delay.set()
        case back.text:
            await UserMenu.active.set()
            await menu_stats(message)
        case _:
            if message.text in ('/start', '/menu'):
                await UserMenu.active.set()
                await menu_stats(message)


@dp.message_handler(state=Delay.set_delay)
async def set_delay_handler(message: Message):
    if message.text in ('/start', '/menu', back.text):
        await UserMenu.active.set()
        await menu_stats(message)
    elif message.text.isnumeric():
        new_delay: int = int(message.text)
        if 1 <= new_delay <= 4320:
            response: bool = set_new_delay(message.from_user.id, new_delay)
            if response:
                await message.answer(f'Задержка <b>{new_delay}</b> успешно установлена.', reply_markup=menu_kb)
                await UserMenu.active.set()
        else:
            await message.answer('Введите корректную задержку (1-4320 мин):', reply_markup=back_kb)
    else:
        await message.answer('Введите корректную задержку (1-4320 мин):', reply_markup=back_kb)
