import datetime
import logging
import sqlite3

con = sqlite3.connect("base.db")
cursor = con.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        telegram_id BIGINT PRIMARY KEY,
        username VARCHAR,
        words_total INTEGER DEFAULT 0,
        words_translated INTEGER DEFAULT 0,
        delay INTEGER DEFAULT 60,
        distribution BOOLEAN DEFAULT 0,
        last_distrib DATETIME
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS words (
        id INTEGER PRIMARY KEY,
        word_eng VARCHAR,
        word_rus VACHAR,
        word_image VARCHAR
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS guessed_words (
        user_telegram_id BIGINT REFERENCES users(telegram_id) ON DELETE CASCADE,
        word_id INTEGER REFERENCES words(id) ON DELETE CASCADE
    )
""")

con.commit()


def get_words() -> list:
    cursor.execute("SELECT word_eng, word_rus FROM words ORDER BY id DESC")
    words = cursor.fetchmany(50)
    return words


def add_word(word_eng: str, word_rus: str, word_image: str) -> bool:
    try:
        cursor.execute("INSERT INTO words (word_eng, word_rus, word_image) VALUES (?, ?, ?)",
                       (word_eng, word_rus, word_image))
        con.commit()
        return True
    except Exception as ex:
        logging.error(f'Error add word in base {ex}')
        return False


def get_word_translation(word_eng: str) -> str | None:
    cursor.execute("SELECT word_rus FROM words WHERE word_eng = ?", (word_eng,))
    translation = cursor.fetchone()
    if translation:
        return translation[0]
    else:
        return None


def get_random_word() -> str | None:
    cursor.execute("""
        SELECT w.word_eng FROM words w 
        LEFT JOIN guessed_words gw 
        ON w.id = gw.word_id 
        WHERE gw.word_id IS NULL 
        ORDER BY random() 
        LIMIT 1
    """)
    word = cursor.fetchone()
    if word:
        return word[0]
    else:
        return None


def get_translation_choices(word: str) -> list | None:
    translation: str = get_word_translation(word)
    cursor.execute(f"""
        SELECT word_rus
        FROM words w
        LEFT JOIN guessed_words gw
        ON w.id = gw.word_id 
        WHERE word_eng != ? AND gw.word_id IS NULL
        ORDER BY random()
        LIMIT 3
    """, (word,))
    choices: list = cursor.fetchall()
    if len(choices):
        # Отброс tuples и совмещение в list с правильным переводом
        return [word[0] for word in choices] + [translation]
    else:
        return None


def update_total_words_count(telegram_id: int) -> bool:
    try:
        cursor.execute("UPDATE users SET words_total = words_total + 1 WHERE telegram_id = ?", (telegram_id,))
        con.commit()
        return True
    except Exception as ex:
        logging.error(f'Error update total count in base {ex}')
        return False


def update_translated_words_count(telegram_id: int) -> bool:
    try:
        cursor.execute("UPDATE users SET words_translated = words_translated + 1 WHERE telegram_id = ?", (telegram_id,))
        con.commit()
        return True
    except Exception as ex:
        logging.error(f'Error update translated count in base {ex}')
        return False


def edit_word_translation(word_eng: str, word_rus: str, word_image: str) -> bool:
    try:
        cursor.execute("UPDATE words SET word_rus = ?, word_image = ? WHERE word_eng = ?", (word_rus, word_image, word_eng))
        con.commit()
        return True
    except Exception as ex:
        logging.error(f'Error edit translation in base {ex}')
        return False


def delete_word(word: str) -> bool:
    try:
        cursor.execute("DELETE FROM words WHERE word_eng = ?", (word,))
        con.commit()
        return True
    except Exception as ex:
        logging.error(f'Error delete word from base {ex}')
        return False


def get_word_id(word: str) -> int | None:
    cursor.execute("SELECT id FROM words WHERE word_eng = ?", (word,))
    word_id = cursor.fetchone()
    if word_id:
        return word_id[0]
    else:
        return None


def get_check_word(word: str) -> str | None:
    cursor.execute("SELECT word_eng FROM words WHERE word_eng = ?", (word,))
    word_id = cursor.fetchone()
    if word_id:
        return word_id[0]
    else:
        return None


def add_word_to_guessed(telegram_id: int, word: str) -> bool:
    word_id: int | None = get_word_id(word)
    if not word_id:
        return False
    else:
        cursor.execute("INSERT INTO guessed_words (user_telegram_id, word_id) VALUES (?, ?)", (telegram_id, word_id))
        con.commit()
        return True


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


def set_new_delay(telegram_id: int, new_delay: int) -> bool:
    try:
        cursor.execute("UPDATE users SET delay = ? WHERE telegram_id = ?", (new_delay, telegram_id))
        con.commit()
        return True
    except Exception as ex:
        logging.error(f'Error update delay: {ex}, {telegram_id}, {new_delay}')
        return False


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


def update_last_distrib(telegram_id: int, new_distrib: datetime.datetime) -> None:
    try:
        cursor.execute("UPDATE users SET last_distrib = ? WHERE telegram_id = ?", (new_distrib, telegram_id))
        con.commit()
    except Exception as ex:
        logging.error(f'Error update last distrib in base: {ex}, {telegram_id}')