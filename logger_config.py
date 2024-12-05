# -*- coding: utf-8 -*-
"""
Модуль логування.

Автор: Михайло; GENOVA
Дата створення: 2024-12-02
Версія: 1.0
Опис: Цей модуль містить конфігурація логування проекту.
Записи здійснюються від рівня INFO та вище.
(Для написання коду та тестування використовувався рівень DEBUG)

Залежності:
- logging
"""

import logging

# Налаштування логування
LOG_FORMAT = "%(asctime)s — %(levelname)s — %(message)s"
logging.basicConfig(
    level=logging.INFO, #logging.DEBUG
    format=LOG_FORMAT,
    handlers=[
        logging.FileHandler("project.log", mode='a', encoding='utf-8'),  # Логування у файл
        logging.StreamHandler()  # Логування в консоль
    ]
)

# Експорт налаштованого логера
logger = logging.getLogger("project_logger")
