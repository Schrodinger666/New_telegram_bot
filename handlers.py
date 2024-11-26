from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from config import CHAT_ID
from link_manager import get_links_info

MENU_CALLBACK_CREATE_LINK = "create_link"
ASKING_LINK_NAME = 1

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Приветственное сообщение и показ обновлённого меню."""
    await update.message.reply_text(
        "Привет! Я - 🎓Decentrathon Referral🚀🎓.\n\n"
        "Сидишь в нашем канале? Пригласи больше народу!"
    )

    menu_keyboard = [
        [InlineKeyboardButton("Создать уникальную ссылку", callback_data=MENU_CALLBACK_CREATE_LINK)]
    ]
    reply_markup = InlineKeyboardMarkup(menu_keyboard)
    await update.message.reply_text("Выберите действие:", reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик нажатий на кнопки меню."""
    query = update.callback_query
    await query.answer()

    if query.data == MENU_CALLBACK_CREATE_LINK:
        await query.edit_message_text("Введите имя ссылки:")
        return ASKING_LINK_NAME

async def link_name_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатывает имя ссылки, введённое пользователем."""
    link_name = update.message.text.strip()

    # Сохранение ссылки в базу данных
    # Для простоты здесь мы предполагаем, что функция для добавления ссылки уже есть
    # Функцию сохранения и добавления ссылки в базу данных необходимо реализовать.

    await update.message.reply_text(f"Ссылка {link_name} была успешно создана!")

    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отмена процесса создания ссылки."""
    await update.message.reply_text("Отмена создания ссылки.")
    return ConversationHandler.END
