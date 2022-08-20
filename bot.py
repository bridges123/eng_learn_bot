import asyncio

from loader import dp, logger
from handlers.admin import admin_panel, add_word, get_words
from handlers.users import menu, word_callback
from db.init_base import con
from services.distribution import distribution_cycle


async def bot_start():
    # start
    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await dp.bot.session.close()
        con.close()


async def main():
    bot_task = asyncio.create_task(bot_start())
    distribution_task = asyncio.create_task(distribution_cycle())
    await asyncio.gather(bot_task, distribution_task)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
