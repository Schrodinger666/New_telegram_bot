from config import CHAT_ID

# Хранилище ссылок: словарь со структурой { link_name: link_data }
links_data = {}
user_links = {}  # This will store the user IDs and their created link names

def link_name_exists(link_name):
    """Проверяет, существует ли ссылка с указанным именем."""
    return link_name in links_data

def add_link(link_name, link_object):
    """Добавляет новую ссылку в хранилище."""
    links_data[link_name] = {
        'invite_link': link_object.invite_link,
        'name': link_object.name,
        'is_primary': link_object.is_primary,
        'is_revoked': link_object.is_revoked
    }

def get_links_info():
    """Возвращает информацию обо всех созданных ссылках."""
    return links_data

def user_has_link(user_id):
    """Проверяет, создал ли пользователь ссылку."""
    return user_id in user_links

def add_user_link(user_id, link_name):
    """Добавляет пользователя и его созданную ссылку."""
    user_links[user_id] = link_name

async def delete_all_links(context):
    """Удаляет все созданные ссылки, отзывает их в чате и очищает хранилище."""
    global links_data
    if not links_data:
        # Нет ссылок для удаления
        return

    for link_name, data in list(links_data.items()):
        invite_link = data['invite_link']
        try:
            # Отзываем (revoke) созданную ссылку
            revoked_link = await context.bot.revoke_chat_invite_link(
                chat_id=CHAT_ID,
                invite_link=invite_link
            )
            # Обновляем статус ссылки в хранилище
            links_data[link_name]['is_revoked'] = revoked_link.is_revoked
        except Exception as e:
            print(f"Не удалось отозвать ссылку {invite_link}: {e}")

    # Удаляем все ссылки из хранилища
    links_data.clear()
    user_links.clear()  # Clear the user links as well
