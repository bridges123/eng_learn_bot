import sqlite3

con = sqlite3.connect("base.db")
cursor = con.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        telegram_id BIGINT PRIMARY KEY,
        words_total INTEGER,
        words_translated INTEGER,
        delay INTEGER
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

con.commit()


def get_words() -> list:
    cursor.execute("SELECT word_eng, word_rus FROM words")
    words = cursor.fetchmany(50)
    return words


def add_word(word_eng: str, word_rus: str, word_image: str) -> None:
    cursor.execute("INSERT INTO words (word_eng, word_rus, word_image) VALUES (?, ?, ?)",
                   (word_eng, word_rus, word_image))
    con.commit()


def translate_word(word_eng: str) -> tuple:
    cursor.execute("SELECT word_rus FROM words WHERE word_eng = ?", (word_eng,))
    return cursor.fetchone()


def get_random_word() -> tuple:
    cursor.execute("SELECT word_eng FROM words ORDER BY random() LIMIT 1")
    return cursor.fetchone()


def update_total_words_count(telegram_id: int) -> None:
    cursor.execute("UPDATE users SET words_total = words_total + 1 WHERE telegram_id = ?", (telegram_id,))
    con.commit()


def update_translated_words_count(telegram_id: int) -> None:
    cursor.execute("UPDATE users SET words_translated = words_translated + 1 WHERE telegram_id = ?", (telegram_id,))
    con.commit()


def add_user(telegram_id: int) -> None:
    cursor.execute("INSERT INTO users (telegram_id, words_total, words_translated, delay) VALUES (?, ?, ?, ?)",
                   (telegram_id, 0, 0, None))
    con.commit()


def get_stats(telegram_id: int) -> tuple:
    cursor.execute("SELECT words_total, words_translated, delay FROM users WHERE telegram_id = ?", (telegram_id,))
    return cursor.fetchone()

