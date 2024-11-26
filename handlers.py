from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from config import CHAT_ID
from link_manager import link_name_exists, add_link, get_links_info, delete_all_links, user_has_link, add_user_link

MENU_CALLBACK_CREATE_LINK = "create_link"
MENU_CALLBACK_SHOW_LINKS = "show_links"
MENU_CALLBACK_DELETE_ALL_LINKS = "delete_all_links"

# Состояния ConversationHandler
ASKING_LINK_NAME = 1

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Приветственное сообщение и показ обновлённого меню."""
    
    # Отправка приветственного сообщения
    await update.message.reply_text(
        "Привет! Я - 🎓Decentrathon Referral🚀🎓.\n\n"
        "Сидишь в нашем канале? Пригласи больше народу!\n"
        "Пропиши команду /start для начала!"
    )

    # Отправка основного меню
    menu_keyboard = [
        [
            InlineKeyboardButton("Создать уникальную ссылку", callback_data=MENU_CALLBACK_CREATE_LINK)
        ]
    ]
    reply_markup = InlineKeyboardMarkup(menu_keyboard)
    await update.message.reply_text(
        "Выберите действие:",
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик нажатий на кнопки меню."""
    query = update.callback_query
    await query.answer()

    if query.data == MENU_CALLBACK_CREATE_LINK:
        # Check if the user has already created a link
        user_id = update.effective_user.id
        if user_has_link(user_id):
            await query.edit_message_text("Вы уже создали ссылку. Вы не можете создать более одной.")
            return ConversationHandler.END
        
        # Переходим в состояние, запрашиваем имя ссылки
        await query.edit_message_text("Введите свой Telegram @тэг:")
        return ASKING_LINK_NAME
    elif query.data == MENU_CALLBACK_SHOW_LINKS:
        links_info = get_links_info()
        if links_info:
            response = "Список созданных ссылок:\n\n"
            for name, data in links_info.items():
                response += (f"Имя: {name}\n"
                             f"Ссылка: {data['invite_link']}\n"
                             f"Отозвана: {'Да' if data['is_revoked'] else 'Нет'}\n"
                             f"---\n")
            await query.edit_message_text(response)
        else:
            await query.edit_message_text("Пока нет созданных ссылок.")
    elif query.data == MENU_CALLBACK_DELETE_ALL_LINKS:
        # Вызываем функцию для удаления всех ссылок
        await delete_all_links(context)
        await query.edit_message_text("Все ссылки были отозваны и удалены.")
    return ConversationHandler.END

async def link_name_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатывает имя ссылки, введённое пользователем."""
    link_name = update.message.text.strip()
    user_id = update.effective_user.id

    if user_has_link(user_id):
        await update.message.reply_text("Вы уже создали ссылку. Вы не можете создать более одной.")
        return ConversationHandler.END

    if link_name_exists(link_name):
        # Имя занято, просим ввести другое
        await update.message.reply_text("Это имя уже занято. Введите другое уникальное имя:")
        return ASKING_LINK_NAME
    else:
        # Создаем пригласительную ссылку с заданным именем
        chat_invite_link = await context.bot.create_chat_invite_link(
            chat_id=CHAT_ID,
            name=link_name  # Назначаем имя ссылке
        )
        # Сохраняем информацию о ссылке
        add_link(link_name, chat_invite_link)
        add_user_link(user_id, link_name)  # Store the user's created link name
        await update.message.reply_text(f"Ссылка создана:\nИмя: {link_name}\nСсылка: {chat_invite_link.invite_link}")

    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отмена процесса создания ссылки."""
    await update.message.reply_text("Отмена создания ссылки.")
    return ConversationHandler.END
