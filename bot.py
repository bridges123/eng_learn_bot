import asyncio

from loader import dp
from handlers.admin import admin_panel, add_word, get_words
from handlers.users import menu, word_callback
import db


async def main():
    # start
    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()
        db.con.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
