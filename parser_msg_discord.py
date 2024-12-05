# -*- coding: utf-8 -*-
"""
Модуль для парсерингу повідомлень з каналів Discord.

Автор: Олександр, Михайло; GENOVA
Дата створення: 2024-12-02
Версія: 1.0
Опис: Модуль містить функцію "parse_discord_channel" призначену для 
парсерингу повідомлень з каналів Discord по заданим параметрам.
Збирається потрібна інформація та формується в потрібну структуру.
Результатом роботи функції (модуля) є JSON файл "parsed_msg"
з структурованою інформацією про повідомлення з каналу.
Весь процес логується.

Залежності:
- requests
- json
- logger_config (модуль логування)
"""

import requests
import json
from logger_config import logger # Імпорт налаштованого логера з модуля logger_config


def parse_discord_channel(discord_token, channel_id, channel_name, output_file="parsed_msg.json"):
    """
    Функція для парсингу повідомлень із Discord каналу.

    Args:
        discord_token (str): Токен для авторизації в Discord.
        channel_id (str): ID каналу, з якого потрібно отримати повідомлення.
        channel_name (str): Назва каналу.
        output_file (str): Ім'я файлу, куди будуть збережені результати. (parsed_msg)

    Returns:
        dict: Словник із повною інформацією про канал та повідомлення.
    """
    logger.info(f"Початок парсингу каналу: {channel_name} (ID: {channel_id})")
    
    # Ініціалізація сесії для виконання HTTP-запитів
    session = requests.Session()
    session.headers['Authorization'] = discord_token # Додаємо токен авторизації у заголовок запиту

    def fetch_messages(channel_id, last_id=None):
        """
        Функція для отримання повідомлення з каналу.
        
        Args:
            channel_id (str): ID каналу.
            last_id (str, optional): ID останнього повідомлення для пагінації.

        Returns:
            list: Список повідомлень.
        """
        # Формуємо URL для отримання повідомлень із каналу
        url = f"https://discord.com/api/v9/channels/{channel_id}/messages?limit=100"
        if last_id:
            url += f"&before={last_id}" # Додаємо параметр пагінації для завантаження попередніх повідомлень
        logger.debug(f"Запит до URL: {url}")
        
        # Виконуємо GET-запит
        response = session.get(url)
        response.raise_for_status()
        return response.json()

    # Ініціалізація змінних для збору всіх повідомлень
    last_id = None
    all_messages = []

    while True:
        try:
            # Завантажуємо повідомлення з каналу
            messages = fetch_messages(channel_id, last_id)
            if not messages: # Якщо повідомлення відсутні, завершити парсинг
                logger.info("Усі повідомлення отримано.")
                break
            
            # Обробка кожного повідомлення
            for msg in messages:
                message_data = {
                    "id": msg["id"], # ID повідомлення
                    "date": msg["timestamp"].split(".")[0], # Дати та час відправки повідомлення
                    "from": msg["author"]["username"], # Автор повідомлення
                    "from_id": msg["author"]["id"], # ID автора
                    "text": msg.get("content", ""), # Текст повідомлення
                }
                if message_data["text"]: # Зберігаємо тільки непорожні повідомлення
                    all_messages.append(message_data)

            # Оновлення останнього ID для наступної ітерації
            last_id = messages[-1]["id"]
            logger.info(f"Отримано {len(messages)} повідомлень. Загалом: {len(all_messages)}")

        except requests.RequestException as request_error:
            logger.error(f"Помилка запиту: {request_error}")
            break
        except Exception as e:
            logger.error(f"Невідома помилка: {e}")
            break

    # Формування структури результату
    full_info_channel = {
        "name": channel_name,
        "id": channel_id,
        "messages": all_messages[::-1]  # Повідомлення у хронологічному порядку
    }

    # Зберігаємо результати у JSON-файл
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(full_info_channel, file, ensure_ascii=False, indent=4)

    logger.info(f"Парсинг завершено. Збережено {len(all_messages)} повідомлень у файл '{output_file}'.")
    with open(f'static/{output_file}', "w", encoding="utf-8") as file:
        json.dump(full_info_channel, file, ensure_ascii=False, indent=4)
    return full_info_channel


if __name__ == "__main__":
    # Приклад використання функції парсингу Discord
    
    # Ввід даних для роботи функції
    discord_token = input("Введіть токен Discord: ").strip()
    channel_id = input("Введіть ID каналу: ").strip()
    channel_name = input("Введіть назву каналу: ").strip()

    # Виклик функції
    try:
        parse_discord_channel(discord_token, channel_id, channel_name)
    except Exception as e:
        logger.error(f"Парсинг не завершено через помилку: {e}")
