import asyncio
from http_serv import create_http_server
from socket_serv import start_socket_server
import logging

# Налаштування логування
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


class TaskLoggerAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        task_name = asyncio.current_task().get_name(
        ) if asyncio.current_task() else 'unknown'
        return f"[{task_name}] {msg}", kwargs


logger = TaskLoggerAdapter(logging.getLogger(__name__), {})


async def main():
    loop = asyncio.get_event_loop()

    # Запуск HTTP сервера
    loop.create_task(create_http_server())  # Стартуємо HTTP сервер
    logger.info("Run http server started")

    # Запуск Socket сервера
    loop.create_task(start_socket_server())
    logger.info("Run socket server started")

    await asyncio.gather()  # Чекаємо на обидва сервери
    logger.info("Socket and http servers up procedure is ended")

if __name__ == '__main__':
    asyncio.run(main())
