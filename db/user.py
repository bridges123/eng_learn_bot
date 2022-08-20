import datetime
import logging

from .init_base import cursor


def add_user(telegram_id: int, username: str) -> bool:
    try:
        cursor.execute("INSERT INTO users "
                       "(telegram_id, username) "
                       "VALUES (?, ?)",
                       (telegram_id, username))
        con.commit()
        return True
    except Exception as ex:
        logging.error(f'Error add user in base {ex}')
        return False


def get_stats_by_telegram_id(telegram_id: int | str) -> tuple | None:
    cursor.execute("SELECT words_total, words_translated, delay FROM users WHERE telegram_id = ?", (telegram_id,))
    return cursor.fetchone()


def get_stats_by_username(username: str) -> tuple | None:
    cursor.execute("SELECT words_total, words_translated, delay FROM users WHERE username = ?", (username,))
    return cursor.fetchone()


def get_current_delay(telegram_id: int) -> int | None:
    cursor.execute("SELECT delay FROM users WHERE telegram_id = ?", (telegram_id,))
    cur_delay = cursor.fetchone()
    if cur_delay:
        return cur_delay[0]
    else:
        return None


def change_distrib(telegram_id: int) -> tuple:
    try:
        cursor.execute("SELECT distribution FROM users WHERE telegram_id = ?", (telegram_id,))
        distrib = cursor.fetchone()
        if distrib:
            distrib: bool = distrib[0]
            cursor.execute(f"UPDATE users SET distribution = ? WHERE telegram_id = ?",
                           (not distrib, telegram_id))
            con.commit()
            return True, not distrib
        else:
            return False, False
    except Exception as ex:
        logging.error(f'Error change distrib: {ex}, {telegram_id}')
        return False, False


def get_users_distribution() -> list | None:
    try:
        cursor.execute("SELECT telegram_id, delay, distribution, last_distrib FROM users")
        users = cursor.fetchall()
        if len(users):
            return users
        else:
            return None
    except Exception as ex:
        logging.error(f'Error get all users distrib: {ex}')
        return None


def set_new_delay(telegram_id: int, new_delay: int) -> bool:
    try:
        cursor.execute("UPDATE users SET delay = ? WHERE telegram_id = ?", (new_delay, telegram_id))
        con.commit()
        return True
    except Exception as ex:
        logging.error(f'Error update delay: {ex}, {telegram_id}, {new_delay}')
        return False


def update_last_distrib(telegram_id: int, new_distrib: datetime.datetime) -> None:
    try:
        cursor.execute("UPDATE users SET last_distrib = ? WHERE telegram_id = ?", (new_distrib, telegram_id))
        con.commit()
    except Exception as ex:
        logging.error(f'Error update last distrib in base: {ex}, {telegram_id}')
