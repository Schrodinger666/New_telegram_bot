import os
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, CallbackContext
import psycopg2
from dotenv import load_dotenv
from datetime import datetime

# Загрузка переменных окружения
load_dotenv()

# Настройки базы данных
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "user": os.getenv("DB_USERNAME"),
    "password": os.getenv("DB_PASSWORD"),
    "dbname": os.getenv("DB_NAME"),
}

# Идентификатор канала
CHANNEL_ID = os.getenv("CHANNEL_ID")

# Подключение к базе данных
def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

# Создание инвайт-ссылки
def create_invite_link(bot: Bot):
    response = bot.create_chat_invite_link(
        chat_id=CHANNEL_ID,
        expire_date=None,  # Бессрочная ссылка
        member_limit=None  # Без ограничения по числу участников
    )
    return response.invite_link

# Команда для создания ссылки
def generate_link(update: Update, context: CallbackContext):
    bot = context.bot

    try:
        # Создаём инвайт-ссылку
        link = create_invite_link(bot)
        update.message.reply_text(f"Ссылка создана: {link}")

        # Сохраняем в базе данных
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO invite_links (link, clicks_count, created_at) VALUES (%s, %s, %s)",
            (link, 0, datetime.now())
        )
        conn.commit()
        cursor.close()
        conn.close()
        update.message.reply_text("Ссылка успешно сохранена в базе данных.")
    except Exception as e:
        update.message.reply_text(f"Ошибка при создании ссылки: {e}")

# Запуск бота
def main():
    # Инициализация бота
    updater = Updater(token=os.getenv("TELEGRAM_TOKEN"))
    dispatcher = updater.dispatcher

    # Регистрация команды
    dispatcher.add_handler(CommandHandler("create_link", generate_link))

    # Запуск
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    # Запуск основного процесса
    main()
