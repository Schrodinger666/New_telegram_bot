import psycopg2
from config import DB_CONFIG

# Функция для подключения к базе данных
def get_db_connection():
    conn = psycopg2.connect(
        host=DB_CONFIG["host"],
        port=DB_CONFIG["port"],
        password=DB_CONFIG["password"]
    )
    return conn

# Пример использования подключения
def get_links_info():
    """Получить информацию о ссылках из базы данных."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM links")  # Предположим, что у вас есть таблица "links"
        rows = cursor.fetchall()

        links_info = {}
        for row in rows:
            link_name = row[0]  # Предположим, что первое поле — это имя ссылки
            invite_link = row[1]  # И второе — ссылка
            links_info[link_name] = {"invite_link": invite_link}

        cursor.close()
        conn.close()
        
        return links_info
    except Exception as e:
        print(f"Ошибка при подключении к базе данных: {e}")
        return {}

# Другие функции (например, добавление ссылок, проверка существования и т.д.) можно добавить аналогично.
