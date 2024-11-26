import json
from config import CHAT_ID

# File paths for saving data
USER_LINKS_FILE = "user_links.json"
LINKS_DATA_FILE = "links_data.json"

# Хранилище ссылок: словарь со структурой { link_name: link_data }
links_data = {}
user_links = {}  # This will store the user IDs and their created link names

def load_user_links():
    """Load user links from a file."""
    global user_links
    try:
        with open(USER_LINKS_FILE, 'r') as f:
            user_links = json.load(f)
    except FileNotFoundError:
        user_links = {}  # If file doesn't exist, start with an empty dictionary
    except json.JSONDecodeError:
        user_links = {}  # Handle case where file is corrupted or empty

def load_links_data():
    """Load links data from a file."""
    global links_data
    try:
        with open(LINKS_DATA_FILE, 'r') as f:
            links_data = json.load(f)
    except FileNotFoundError:
        links_data = {}  # If file doesn't exist, start with an empty dictionary
    except json.JSONDecodeError:
        links_data = {}  # Handle case where file is corrupted or empty

def save_user_links():
    """Save user links to a file."""
    with open(USER_LINKS_FILE, 'w') as f:
        json.dump(user_links, f)

def save_links_data():
    """Save links data to a file."""
    with open(LINKS_DATA_FILE, 'w') as f:
        json.dump(links_data, f)

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
    save_links_data()  # Save links data after adding a new link

def get_links_info():
    """Возвращает информацию обо всех созданных ссылках."""
    return links_data

def user_has_link(user_id):
    """Проверяет, создал ли пользователь ссылку."""
    return user_id in user_links

def add_user_link(user_id, link_name):
    """Добавляет пользователя и его созданную ссылку."""
    user_links[user_id] = link_name
    save_user_links()  # Save user links after adding a new user link

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
    save_links_data()  # Save the cleared links data
    save_user_links()  # Save the cleared user links

# Call these functions to load data at the start
load_user_links()
load_links_data()
