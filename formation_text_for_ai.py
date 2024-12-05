# -*- coding: utf-8 -*-
"""
Модуль для формування тексту для передачі на обробку віртуальним експертом.

Автор: Вікторія, Михайло; GENOVA
Дата створення: 2024-12-02
Версія: 2.0
Опис: Цей модуль містить функцію "filter_specific_fields" призначену для
формування тексту по заданим полям для подальшої передачі на обробку віртуальним експертом.
Інформація завантажується з JSON файлу "parsed_msg",
далі повідомлення фільтруються за заданими полями.
Результатом роботи функції (модуля) є багаторядкова змінна
з структурованою інформацією, яка в подальшому обробляється ШІ.
Весь процес логується.

Залежності:
- json
- logger_config (модуль логування)
"""

import json
from logger_config import logger  # Імпорт налаштованого логера з модуля logger_config


def filter_specific_fields(input_file="parsed_msg.json"):
    """
    Функція для формування тексту для передачі на обробку ШІ.
    Фільтрації повідомлень, залишаючи поля "from" та "text" у форматі "ім'я:текст".

    Args:
        input_file (str): Шлях до вхідного JSON файлу.

    Returns:
        str: Відфільтровані дані у вигляді багаторядкового тексту.
    """
    logger.info(f"Початок обробки файлу (для формування тексту для ШІ):{input_file}")

    try:
        # Завантаження даних із JSON файлу
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        logger.info(f"Дані успішно завантажено з файлу: {input_file}")
    except FileNotFoundError:
        logger.error(f"Файл {input_file} не знайдено.")
        return ""
    except json.JSONDecodeError as e:
        logger.error(f"Помилка читання JSON файлу {input_file}: {e}")
        return ""

    # Створення структури для збереження відфільтрованих даних
    filtered_data = []

    # Рекурсивний пошук та фільтрація повідомлень
    def find_and_filter_messages(data):
       """
       Рекурсивна функція для пошуку та фільтрації повідомлень у вхідних даних.
       
       Args:
           data (list або dict): Дані для обробки, що можуть бути списком або словником.
       """
       if isinstance(data, list):
            # Ітеруємося через список, щоб знайти повідомлення
            for message in data:
                if isinstance(message, dict):
                    # Отримання полів "from" та "text" зі словника повідомлення
                    from_field = message.get("from", "")
                    text_field = message.get("text", "")
                    
                    # Обробка поля "text" у випадку, якщо воно є списком
                    if isinstance(text_field, list):
                        
                        # Збираємо всі текстові елементи в один рядок, якщо поле "text" є списком
                        text_field = "".join(
                            [item["text"] if isinstance(item, dict) and "text" in item else item
                             for item in text_field if isinstance(item, (str, dict))]
                        ).strip()
                        
                    # Обробка поля "text" у випадку, якщо воно є рядком
                    elif isinstance(text_field, str):
                        text_field = text_field.strip()
                        
                    # Зберігаємо повідомлення, тільки якщо обидва поля не пусті
                    if from_field and text_field:  
                        filtered_data.append(f"{from_field}: {text_field}")
                        logger.debug(f"Оброблено повідомлення від: {from_field}")
        
       # Якщо вхідні дані є словником
       elif isinstance(data, dict):
            for key, value in data.items():
                # Обробка ключа "messages", якщо він є списком
                if key == "messages" and isinstance(value, list):
                    # Рекурсивний виклик для списку повідомлень
                    find_and_filter_messages(value)
                # Рекурсивна обробка вкладених словників або списків
                elif isinstance(value, (dict, list)):
                    find_and_filter_messages(value)

    # Виконання рекурсивного пошуку
    logger.info("Початок фільтрації повідомлень...")
    find_and_filter_messages(data)
    logger.info(f"Фільтрація завершена. Загальна кількість відфільтрованих повідомлень: {len(filtered_data)}")

    # Формування тексту для багаторядкової змінної
    text_for_ai = "\n".join(filtered_data)

    output_file = "parsed_msg_for_ai.txt"
    try:
        # Збереження результату у вихідний файл
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(text_for_ai)
        logger.info(f"Відфільтровані дані збережено у файл: {output_file}")
    except IOError as e:
        logger.error(f"Помилка запису у файл {output_file}: {e}")
        return
        
    return text_for_ai

if __name__ == "__main__":
    # Приклад використання функції для формування тексту для ШІ
    
    # Виклик функції
    try:
        text_for_ai = filter_specific_fields()
        print(text_for_ai)  # Вивід результату у консоль
    except Exception as e:
        logger.error(f"Непередбачена помилка: {e}")
        