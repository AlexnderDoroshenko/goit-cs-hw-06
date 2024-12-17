import os
import logging
from logging.handlers import RotatingFileHandler


def get_logger(name: str) -> logging.Logger:
    """ 
    Створює логер з окремим файлом для кожного модуля/категорії. 
    Логи зберігаються у папці `app/logs/` під ім'ям `{name}.log`.

    Args:
        name (str): Назва модуля або категорії (наприклад, 'server', 'database').

    Returns:
        logging.Logger: Налаштований логер.
    """
    # 1️⃣ Директорія для логів
    log_dir = os.path.join(os.path.dirname(__file__), 'logs')
    os.makedirs(log_dir, exist_ok=True)  # створюємо папку, якщо її немає

    # 2️⃣ Шлях до файлу для логів
    log_file = os.path.join(log_dir, f'{name}.log')

    # 3️⃣ Форматування логів
    log_formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)s] - %(message)s')

    # 4️⃣ Обробник для запису логів у файл з ротацією
    file_handler = RotatingFileHandler(
        log_file, maxBytes=1_000_000, backupCount=5)
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(logging.DEBUG)  # Усі рівні логів

    # 5️⃣ Обробник для виведення логів у консоль
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    console_handler.setLevel(logging.INFO)  # Лише INFO та вище

    # 6️⃣ Ініціалізація логера
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # Записуємо всі рівні логування
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # 7️⃣ Уникнення дублювання обробників
    if logger.hasHandlers():
        logger.handlers.clear()
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger
