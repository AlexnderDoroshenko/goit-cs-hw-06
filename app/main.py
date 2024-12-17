import threading
from http_serv import create_http_server
from socket_serv import start_socket_server
from logger import get_logger

log = get_logger("main")


def main():
    # Запуск HTTP сервера в окремому потоці
    http_thread = threading.Thread(target=create_http_server)
    http_thread.start()
    log.info("HTTP server started in a separate thread")

    # Запуск Socket сервера в окремому потоці
    socket_thread = threading.Thread(target=start_socket_server)
    socket_thread.start()
    log.info("Socket server started in a separate thread")

    # Дочекаємося завершення роботи обох серверів
    http_thread.join()
    socket_thread.join()

    log.info("Both servers are running")


if __name__ == '__main__':
    main()
