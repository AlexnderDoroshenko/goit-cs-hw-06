import pytest
import subprocess
import time
import requests
import socket
from multiprocessing import Process

# Функція для запуску HTTP-сервера


def start_http_server():
    subprocess.run(["python", "main.py"], cwd="./app")

# Функція для запуску сокет-сервера


def start_socket_server():
    subprocess.run(["python", "socket_server.py"], cwd="./app")


@pytest.fixture(scope="session")
def client():
    # Запускаємо HTTP сервер у фоновому процесі
    http_process = Process(target=start_http_server)
    http_process.start()
    time.sleep(1)  # чекаємо, щоб сервер запустився

    # Запускаємо сокет-сервер у фоновому процесі
    socket_process = Process(target=start_socket_server)
    socket_process.start()
    time.sleep(1)  # чекаємо, щоб сервер запустився

    # Налаштовуємо клієнт для HTTP запитів
    client = requests.Session()

    yield client

    # Завершуємо процеси серверів після тестування
    http_process.terminate()
    socket_process.terminate()
