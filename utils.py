import json
import logging


def translate_word(word: str) -> str:
    try:
        with open('words.json', 'r') as file:
            words: str = json.load(file)
            print(words)
            return '123'
    except Exception as ex:
        logging.error(f'ERROR with words.json: {ex}')