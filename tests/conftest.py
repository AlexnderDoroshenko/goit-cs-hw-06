import pytest
import requests
import asyncio

from app.mongo_db_client import client as socket_client, messages_collection
from dotenv import load_dotenv
from app.http_serv import create_http_server


@pytest.fixture
async def client():
    app = await create_http_server()
    client = await app.test_client()  # Отримуємо тестовий клієнт для роботи з сервером
    yield client
    await app.cleanup()  # Очищаємо ресурси після завершення тестів

# Налаштування для роботи з pytest


@pytest.fixture(scope="session", autouse=True)
def load_env():
    """Завантаження змінних оточення з .env файлу"""
    load_dotenv()


@pytest.fixture(scope="session")
async def mongo_setup():
    """Підключення до реальної бази даних у Docker"""
    # Чекаємо кілька секунд, щоб MongoDB піднявся
    await asyncio.sleep(5)
    yield
    # Видаляємо всі записи після виконання тестів
    await messages_collection.drop()

# Функція для запуску HTTP-сервера


@pytest.fixture(scope="session")
def http_client():

    # Налаштовуємо клієнт для HTTP запитів
    client = requests.Session()

    yield client

    # # Завершуємо процеси серверів після тестування
    # http_process.terminate()
    # socket_process.terminate()


@pytest.fixture(scope="session")
def sock_client():

    # Налаштовуємо клієнт для HTTP запитів
    client = socket_client

    yield client
