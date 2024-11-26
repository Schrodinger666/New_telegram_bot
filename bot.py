import logging
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, filters
import config
from handlers import (start_command, button_handler, link_name_handler, cancel, ASKING_LINK_NAME)

# Включаем логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    # Создаём приложение для бота
    application = ApplicationBuilder().token(config.TOKEN).build()

    # Обработчик для команды /start
    application.add_handler(CommandHandler("start", start_command))

    # ConversationHandler для создания ссылки
    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(button_handler, pattern="^create_link$")],
        states={
            ASKING_LINK_NAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, link_name_handler)
            ]
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        allow_reentry=True
    )

    application.add_handler(conv_handler)

    # Запускаем бота в режиме polling
    application.run_polling()

if __name__ == "__main__":
    main()
