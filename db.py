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

cursor.execute("""
    CREATE TABLE IF NOT EXISTS guessed_words (
        user_telegram_id BIGINT REFERENCES users(telegram_id),
        word_id INTEGER REFERENCES words(id)
    )
""")

con.commit()


def get_words() -> list:
    cursor.execute("SELECT word_eng, word_rus FROM words ORDER BY id DESC")
    words = cursor.fetchmany(50)
    return words


def add_word(word_eng: str, word_rus: str, word_image: str) -> None:
    cursor.execute("INSERT INTO words (word_eng, word_rus, word_image) VALUES (?, ?, ?)",
                   (word_eng, word_rus, word_image))
    con.commit()


def translate_word(word_eng: str) -> str | None:
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


def get_random_translates(word: str) -> tuple:
    pass


def update_total_words_count(telegram_id: int) -> None:
    cursor.execute("UPDATE users SET words_total = words_total + 1 WHERE telegram_id = ?", (telegram_id,))
    con.commit()


def update_translated_words_count(telegram_id: int) -> None:
    cursor.execute("UPDATE users SET words_translated = words_translated + 1 WHERE telegram_id = ?", (telegram_id,))
    con.commit()


def get_word_id(word: str) -> int | None:
    cursor.execute("SELECT id FROM words WHERE word_eng = ?", (word,))
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


def add_user(telegram_id: int) -> None:
    cursor.execute("INSERT INTO users (telegram_id, words_total, words_translated, delay) VALUES (?, ?, ?, ?)",
                   (telegram_id, 0, 0, None))
    con.commit()


def get_stats(telegram_id: int) -> tuple:
    cursor.execute("SELECT words_total, words_translated, delay FROM users WHERE telegram_id = ?", (telegram_id,))
    return cursor.fetchone()
