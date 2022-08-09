import translators as ts


def google_translate_word(word: str) -> str:
    try:
        translation: str = ts.google(word, from_language='en', to_language='ru')
    except Exception as ex:
        translation: str = 'отсутствует'
        logging.error(f'Error google translate: {ex}')
    return translation
