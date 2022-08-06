from environs import Env


def load_config():
    env = Env()
    env.read_env('.env')
    return {
        'token': env.str('TELEGRAM_TOKEN'),
        'admins': list(map(int, env.list('ADMINS'))),
    }
