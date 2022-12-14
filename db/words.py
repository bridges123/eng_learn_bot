import logging
import json

from .init_base import cursor, con


def get_words() -> list:
    cursor.execute("SELECT word_eng, word_rus FROM words ORDER BY id DESC")
    words = cursor.fetchmany(50)
    return words


def get_word_translation(word_eng: str) -> str | None:
    cursor.execute("SELECT word_rus FROM words WHERE word_eng = ?", (word_eng,))
    translation = cursor.fetchone()
    if translation:
        return translation[0]
    else:
        return None


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
        WHERE word_eng != ?
        ORDER BY random()
        LIMIT 3
    """, (word,))
    choices: list = cursor.fetchall()
    if len(choices):
        # Отброс tuples и совмещение в list с правильным переводом
        return [word[0] for word in choices] + [translation]
    else:
        return None


def add_word(word_eng: str, word_rus: str) -> bool:
    try:
        cursor.execute("REPLACE INTO words (id, word_eng, word_rus) VALUES "
                       "((SELECT id FROM words WHERE word_eng = ?), ?, ?)",
                       (word_eng, word_eng, word_rus))
        con.commit()
        return True
    except Exception as ex:
        logging.error(f'Error add word in base {ex}')
        return False


def add_many_words_in_base(file_name: str) -> bool:
    with open(file_name) as file:
        data: dict = json.load(file)
        if data and len(data):
            for word_eng, word_rus in data.items():
                cursor.execute("REPLACE INTO words (id, word_eng, word_rus) VALUES "
                               "((SELECT id FROM words WHERE word_eng = ?), ?, ?)",
                               (word_eng, word_eng, word_rus))
            con.commit()
            return True
        else:
            logging.error(f'Error empty data: {data}, {file_name}')
        return False


def add_word_to_guessed(telegram_id: int, word: str) -> bool:
    word_id: int | None = get_word_id(word)
    if not word_id:
        return False
    else:
        cursor.execute("INSERT INTO guessed_words (user_telegram_id, word_id) VALUES (?, ?)", (telegram_id, word_id))
        con.commit()
        return True


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


def edit_word_translation(word_eng: str, word_rus: str) -> bool:
    try:
        cursor.execute("UPDATE words SET word_rus = ? WHERE word_eng = ?",
                       (word_rus, word_eng))
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
