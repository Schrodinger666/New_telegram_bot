import asyncio
from telethon import TelegramClient

# Конфигурация Telegram API
API_ID = '27235548'  # Вставьте свой API ID
API_HASH = '21e3644ab24f136a3dadf5f6aefa5055'  # Вставьте свой API Hash
BOT_USERNAME = '@Decentrathon_Link_create_bot'  # Например, @my_test_bot

# Параметры теста
REQUEST_COUNT = 20  # Общее количество запросов
CONCURRENT_REQUESTS = 5  # Одновременные запросы

async def stress_test(client):
    async def send_request(request_number):
        try:
            # Шаг 1: Отправляем команду /start
            response_start = await client.send_message(BOT_USERNAME, '/start')
            print(f'[{request_number}] Ответ на /start: {response_start.text}')

            # Шаг 2: Получаем ответ от бота с кнопками
            bot_response = await client.get_messages(BOT_USERNAME, limit=1)
            if bot_response[0].buttons:
                # Поиск кнопки "Создать новую ссылку"
                for row in bot_response[0].buttons:
                    for button in row:
                        if button.text == "Создать новую ссылку":
                            print(f'[{request_number}] Нажимаем кнопку: {button.text}')

                            # Шаг 3: Отправляем callback-ответ
                            callback_result = await client(GetBotCallbackAnswer(
                                peer=BOT_USERNAME,
                                msg_id=bot_response[0].id,
                                data=button.data
                            ))
                            print(f'[{request_number}] Ответ на callback: {callback_result.message}')
                            return
                print(f'[{request_number}] Кнопка "Создать новую ссылку" не найдена.')
            else:
                print(f'[{request_number}] Кнопок нет, пропуск.')
        except Exception as e:
            print(f'[{request_number}] Ошибка: {e}')

    # Создание задач
    tasks = [send_request(i + 1) for i in range(REQUEST_COUNT)]
    for i in range(0, len(tasks), CONCURRENT_REQUESTS):
        batch = tasks[i:i + CONCURRENT_REQUESTS]
        await asyncio.gather(*batch)
        print(f'Обработано {i + len(batch)} запросов.')

async def main():
    # Подключение клиента
    async with TelegramClient('stress_test_session', API_ID, API_HASH) as client:
        print('Запускаем стресс-тест...')
        await stress_test(client)
        print('Стресс-тест завершён.')

if __name__ == '__main__':
    asyncio.run(main())