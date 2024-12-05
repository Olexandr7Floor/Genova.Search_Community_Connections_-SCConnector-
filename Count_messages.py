# -*- coding: utf-8 -*-
"""
Автор: Вікторія
Дата: 2024-12-02
Опис: Скрипт для завантаження JSON файлу, аналізу активності користувачів, 
та збереження результатів у текстовий файл.

Цей скрипт призначений для обробки даних із JSON, включаючи підрахунок кількості повідомлень від кожного користувача 
та виведення їх у текстовий файл у відсортованому вигляді.
"""

import json
from collections import Counter

def load_json(input_file):
    """
    Завантаження JSON даних з вхідного файлу.

    Аргументи:
        input_file (str): Шлях до вхідного JSON файлу.

    Повертає:
        dict: Дані, завантажені з JSON файлу.
    """
    with open(input_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def count_user_messages(data):
    """
    Підрахунок кількості повідомлень від кожного користувача.

    Аргументи:
        data (dict): Дані з JSON файлу.

    Повертає:
        Counter: Словник з кількістю повідомлень від кожного користувача.
    """
    messages = data.get("messages", [])
    user_counts = Counter()
    for message in messages:
        user = message.get("from", "")
        if user:
            user_counts[user] += 1
    return user_counts

def save_user_counts_to_txt(user_counts, output_file):
    """
    Збереження кількості повідомлень від кожного користувача у текстовий файл.

    Аргументи:
        user_counts (Counter): Словник з кількістю повідомлень від кожного користувача.
        output_file (str): Шлях до вихідного текстового файлу.
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        
        f.write(f"Кількість учасників спільноти - {len(user_counts)}\n")
        f.write(f"Кількість повідомлень в спільноті - {sum(user_counts.values())}\n")
        for user, count in user_counts.most_common():
            f.write(f"{user} - {count}\n")
            


if __name__ == "__main__":
    """
    Основна функція для виконання процесу завантаження даних, підрахунку повідомлень та збереження результатів.
    """
    input_file = 'parsed_msg.json'
    output_file = 'user_message_counts.txt'
    data = load_json(input_file)
    user_counts = count_user_messages(data)
    save_user_counts_to_txt(user_counts, output_file)
    
    number_active_users = len(user_counts)
    print(f'Кількість активних користувачів у спільноті {number_active_users}')

    print("Кількість повідомлень від користувачів збережено у '{}'".format(output_file))

