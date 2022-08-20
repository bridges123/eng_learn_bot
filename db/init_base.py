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