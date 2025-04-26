from environs import Env

env = Env()
env.read_env()  # Чтение .env файла

BOT_TOKEN = env.str("BOT_TOKEN")
DEBUG = env.bool("DEBUG", default=False)