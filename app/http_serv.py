import socket
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import urllib.parse  # Для парсингу POST-даних
from pathlib import Path

from logger import get_logger
from socket_serv import HOST, PORT

log = get_logger("http_server")

HTTP_SERVER_HOST, HTTP_SERVER_PORT = "0.0.0.0", 3000
SOCKET_SERVER_HOST, SOCKET_SERVER_PORT = HOST, PORT
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
                    log.error("Send to Socket Server Error \n{err}")
                    self.send_response(500)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    # self.get_source('/message.html')
                    self.wfile.write(f"<h1>{err}<h1>")
                else:
                    log.error("Successful response")
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    # self.get_source('/message.html')
                    self.wfile.write(b"<h1>Message Sent Successfully!<h1>")
            else:
                log.error("User Error \n{err}")
                self.send_response(400)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                # self.get_source('/message.html')
                self.wfile.write(
                    b"<h1>All fields should be filled out before send!<h1>")
            self.wfile.write(
                b'<a href="javascript: history.back()">Go Back</a>')
        else:
            log.error("Source not found Error \n{err}")
            self.get_error_source()

    def send_to_socket_server(self, data):
        """ Відправка повідомлення на Socket-сервер """
        log.info("Start send to socket server")
        try:
            with socket.socket(
                    socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect((SOCKET_SERVER_HOST, SOCKET_SERVER_PORT))
                message = f"{data}".encode('utf-8')
                client_socket.sendall(message)
            log.info("Success")
        except Exception as e:
            log.error(f"Error sending data to Socket server: {e}")
            raise ConnectionError(e)


def create_http_server():
    log.info("Start create http")
    httpd = ThreadingHTTPServer(
        (HTTP_SERVER_HOST, HTTP_SERVER_PORT), MyHTTPRequestHandler)
    print(f"Threaded HTTP server running on port {HTTP_SERVER_PORT}...")
    httpd.serve_forever()
    log.info("Http server started")


if __name__ == "__main__":
    create_http_server()
