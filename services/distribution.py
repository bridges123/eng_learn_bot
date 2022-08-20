import asyncio
from datetime import datetime

from db.user import get_users_distribution, update_last_distrib
from services.translation import translate_word


async def distribution_cycle():
    while True:
        users: list | None = get_users_distribution()
        if users:
            for user in users:
                # user: tuple
                # telegram_id: int
                # delay: int
                # distribution: int
                # last_distrib: float
                telegram_id, delay, distribution, last_distrib = user
                if distribution:
                    if not last_distrib:
                        update_last_distrib(telegram_id, datetime.now().timestamp())
                    elif datetime.now().timestamp() > last_distrib + delay * 60:
                        await translate_word(telegram_id)
                        update_last_distrib(telegram_id, datetime.now().timestamp())
        await asyncio.sleep(1)