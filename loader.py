import logging

from aiogram import Bot, Dispatcher
from aiogram.types import ParseMode, BotCommand
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import load_config
from filters.admin import AdminFilter

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
)
config = load_config()

storage = MemoryStorage()
bot = Bot(token=config['token'], parse_mode=ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)

# """ Установка комманд бота """
# await bot.set_my_commands([
#     BotCommand('start', 'Запустить бота'),
#     BotCommand('word', 'Перевести слово'),
#     BotCommand('menu', 'Меню бота'),
# ])

""" Регистрация кастомных фильтров """
dp.filters_factory.bind(AdminFilter)
