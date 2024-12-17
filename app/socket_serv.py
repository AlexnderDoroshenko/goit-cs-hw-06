import socket
import threading
from datetime import datetime

from logger import get_logger
from mongo_db_client import messages_collection

log = get_logger("Socket_server")

HOST = 'localhost'
PORT = 5000


def handle_client(conn, addr):
    """ Обробка одного клієнтського підключення """
    log.info(f"Connected by {addr}")
    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                break

            try:
                message_data = eval(data.decode('utf-8'))
                message_data['date'] = datetime.now().strftime(
                    '%Y-%m-%d %H:%M:%S.%f')
                messages_collection.insert_one(message_data)
                log.info(f"Message saved: {message_data}")
            except Exception as e:
                log.error(f"Error: {e}")


def start_socket_server():
    """ Старт багатопотокового сокет-сервера """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        log.info(f"Socket server is listening on port {PORT}...")

        while True:
            conn, addr = server_socket.accept()
            client_thread = threading.Thread(
                target=handle_client, args=(conn, addr))
            client_thread.start()


if __name__ == "__main__":
    start_socket_server()
