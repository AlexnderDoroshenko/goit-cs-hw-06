import socket
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import urllib.parse  # Для парсингу POST-даних
from pathlib import Path
import logging
import time

# Налаштування логування
logging.basicConfig(level=logging.DEBUG)

HTTP_SERVER_PORT = 3000
SOCKET_SERVER_HOST = '0.0.0.0'
SOCKET_SERVER_PORT = 5000
# (Path(__file__).parent).joinpath("templates")
TEMPLATES_PATH = Path(__file__).parent

SOURCE_MAP = {
    "/": 'templates/index.html',
    "/message.html": 'templates/message.html',
    "/error.html": 'templates/error.html',
    "/style.css": 'static/style.css',
    "/logo.png": 'static/logo.png',
}


class MyHTTPRequestHandler(BaseHTTPRequestHandler):

    def get_source(self, path):
        if SOURCE_MAP.get(path):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            source_path = TEMPLATES_PATH.joinpath(SOURCE_MAP.get(path))
            with open(source_path, 'rb') as file:
                self.wfile.write(file.read())
        else:
            self.get_error_source()

    def get_error_source(self, path="/error.html"):
        self.send_response(404)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        source_path = TEMPLATES_PATH.joinpath(SOURCE_MAP.get(path))
        with open(source_path, 'rb') as file:
            self.wfile.write(file.read())

    def do_GET(self):
        """ Обробка GET-запитів (для сторінок і статичних файлів) """
        self.get_source(self.path)

    def do_POST(self):
        """ Обробка POST-запиту на маршрут /send """
        if self.path == '/message':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = urllib.parse.parse_qs(post_data.decode('utf-8'))

            username = data.get('username', [''])[0]
            message = data.get('message', [''])[0]

            if username and message:
                payload = {'username': username, 'message': message}
                try:
                    self.send_to_socket_server(payload)
                except Exception as err:
                    logging.error("Send to Socket Server Error \n{err}")
                    self.send_response(500)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(f"<h1>{err}</h1>")
                else:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(b"<h1>Message Sent Successfully!</h1>")
                    time.sleep(1)
                    self.get_source('/message.html')
            else:
                self.send_response(400)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(
                    b"<h1>All fields should be filled out before send!</h1>")
        else:
            self.get_error_source()

    def send_to_socket_server(self, data):
        """ Відправка повідомлення на Socket-сервер """
        try:
            with socket.socket(
                    socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect((SOCKET_SERVER_HOST, SOCKET_SERVER_PORT))
                message = f"{data}".encode('utf-8')
                client_socket.sendall(message)
        except Exception as e:
            print(f"Error sending data to Socket server: {e}")


def create_http_server():
    httpd = ThreadingHTTPServer(
        ('0.0.0.0', HTTP_SERVER_PORT), MyHTTPRequestHandler)
    print(f"Threaded HTTP server running on port {HTTP_SERVER_PORT}...")
    httpd.serve_forever()


if __name__ == "__main__":
    create_http_server()
