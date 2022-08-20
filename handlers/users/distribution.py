from aiogram.types import Message

from db.user import change_distrib
from keyboards.reply import menu_kb


async def on_off_distrib(message: Message):
    response, distrib = change_distrib(message.from_user.id)
    if response:
        mode: str = 'выключена'
        if distrib:
            mode = 'включена'
        await message.answer(f'Рассылка успешно <b>{mode}</b>', reply_markup=menu_kb)