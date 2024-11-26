import os
from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env
load_dotenv()

# Конфигурация бота
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Конфигурация базы данных
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", 5432)  # Порт по умолчанию

# Проверка на наличие необходимых переменных окружения
if not TOKEN:
    raise ValueError("BOT_TOKEN не установлен в .env файле")
if not DATABASE_PASSWORD:
    raise ValueError("DATABASE_PASSWORD не установлен в .env файле")
if not DB_HOST:
    raise ValueError("DB_HOST не установлен в .env файле")
if not CHAT_ID:
    raise ValueError("CHAT_ID не установлен в .env файле")

# Конфигурация для подключения к базе данных
DB_CONFIG = {
    "host": DB_HOST,
    "port": DB_PORT,
    "password": DATABASE_PASSWORD
}
