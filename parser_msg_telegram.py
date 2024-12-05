# -*- coding: utf-8 -*-
"""
Модуль для парсерингу повідомлень із дампу чату з Telegram.

Автор: Вікторія, Михайло; GENOVA
Дата створення: 2024-12-02
Версія: 2.0
Опис: Цей модуль містить функцію "load_and_filter_json" призначену для
парсерингу повідомлень з JSON файлу дампу Telegram чату по заданим полям.
Інформація завантажується з JSON файлу дампу Telegram чату,
далі повідомлення фільтруються за заданими полями.
Результатом роботи функції (модуля) є JSON файл "parsed_msg"
з структурованою інформацією про повідомлення дампу чату з Telegram.
Весь процес логується.

Залежності:
- json
- logger_config (модуль логування)
"""

import json
from logger_config import logger  # Імпорт налаштованого логера з модуля logger_config

def load_and_filter_json(input_file, output_file="parsed_msg.json"):
    """
    Функція для парсерингу повідомлень із дампу чату з Telegram

    Args:
        input_file (str): Шлях до вхідного JSON файлу.
        output_file (str): Шлях до вихідного JSON файлу.

    Returns:
        dict: Відфільтровані дані у форматі словника.
    """
    logger.info(f"Початок обробки файлу дампу чату Telegram: {input_file}")
    
    try:
        # Завантаження даних із JSON файлу
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        logger.info(f"Дані успішно завантажено з файлу: {input_file}")
    except FileNotFoundError:
        logger.error(f"Файл {input_file} не знайдено.")
        return
    except json.JSONDecodeError as e:
        logger.error(f"Помилка читання JSON файлу {input_file}: {e}")
        return

    # Створення структури для збереження відфільтрованих даних
    filtered_data = {
        "name": data.get("name", ""),
        "id": data.get("id", ""),
        "messages": []
    }

    def find_and_filter_messages(data):
        """
        Функція рекурсивного пошуку списку "messages" у словнику та фільтрація відповідних полів.

        Args:
            data (dict або list): Дані для пошуку.
        """
        if isinstance(data, list):
            for message in data:  # Ітеруємо кожен елемент списку
                if isinstance(message, dict):  # Перевіряємо, чи є елемент словником
                    # Перевірка, чи поле "text" є списком або рядком, і отримання чистого тексту
                    text_content = ""
                    if isinstance(message.get("text"), list):
                        text_content = "".join(
                            [item["text"] if isinstance(item, dict) and "text" in item else item
                             for item in message["text"] if isinstance(item, (str, dict))]
                        ).strip()
                    elif isinstance(message.get("text"), str):
                        text_content = message["text"].strip()

                    if not text_content:  # Пропускаємо повідомлення, якщо текст відсутній
                        logger.debug(f"Пропущено повідомлення з ID: {message.get('id', 'невідомий')} - відсутній текст.")
                        continue

                    # Зберігаємо тільки повідомлення з текстом
                    filtered_message = {
                        "id": message.get("id", ""),
                        "date": message.get("date", ""),
                        "from": message.get("from", ""),
                        "from_id": message.get("from_id", ""),
                        "text": text_content
                    }
                    filtered_data["messages"].append(filtered_message)
                    logger.debug(f"Оброблено повідомлення з ID: {filtered_message['id']}")
        # Якщо вхідні дані є словником
        elif isinstance(data, dict):
            for key, value in data.items():  # Ітеруємо ключі та значення словника
                if key == "messages" and isinstance(value, list):
                    # Якщо знайдено ключ "messages" зі списком, обробляємо цей список
                    find_and_filter_messages(value)  # Рекурсивний виклик для списку повідомлень
                elif isinstance(value, (dict, list)):
                    # Якщо значення є словником або списком, рекурсивно обробляємо вкладені дані
                    find_and_filter_messages(value)  # Рекурсивний виклик для вкладених даних

    # Виконання рекурсивного пошуку
    logger.info("Початок фільтрації повідомлень з дампу чату Telegram...")
    find_and_filter_messages(data)
    logger.info(f"Фільтрація завершена. Загальна кількість повідомлень: {len(filtered_data['messages'])}")

    try:
        # Збереження результату у вихідний файл
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(filtered_data, f, ensure_ascii=False, indent=4)
        logger.info(f"Відфільтровані дані збережено у файл: {output_file}")
    except IOError as e:
        logger.error(f"Помилка запису у файл {output_file}: {e}")
        return
    with open(f'static/{output_file}', 'w', encoding='utf-8') as f:
        json.dump(filtered_data, f, ensure_ascii=False, indent=4)
    
    return filtered_data

if __name__ == "__main__":
    # Приклад використання функції парсингу дампу чату Telegram
    
    # Вхідний файл
    input_file = 'result.json'

    # Виклик функції
    try:
        result = load_and_filter_json(input_file)
        if result:
            logger.info(f"Процес завершено. Оброблено повідомлень: {len(result['messages'])}")
        else:
            logger.warning("Процес завершено з помилками.")
    except Exception as e:
        logger.error(f"Непередбачена помилка: {e}")


