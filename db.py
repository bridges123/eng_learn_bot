import sqlite3

con = sqlite3.connect("base.db")
cursor = con.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        telegram_id BIGINT PRIMARY KEY,
        words_total INT,
        words_guessed INT,
        delay INT
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS words (
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


def translate_word(word_eng: str) -> str:
    cursor.execute("SELECT word_rus FROM words WHERE word_eng = ?", (word_eng,))
    return cursor.fetchone()


def add_user(telegram_id: int) -> None:
    cursor.execute("INSERT INTO users (telegram_id, words_total, words_guessed, delay) VALUES (?, ?, ?, ?)",
                   (telegram_id, 0, 0, None))
    con.commit()