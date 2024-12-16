from aiohttp import web

from mongo_db_client import save_message
from http_serv import render_template

# Обробник для головної сторінки


async def handle_home(request):
    return web.Response(
        text=render_template('index.html'), content_type='text/html')

# Обробник для сторінки повідомлень


async def handle_message(request):
    if request.method == 'POST':
        data = await request.post()
        username = data.get('username')
        message = data.get('message')

        # Збереження повідомлення в MongoDB
        await save_message(username, message)

        # Повертаємо підтвердження
        return web.Response(text=f"Message from {username}: {message}")

    return web.Response(
        text=render_template('message.html'), content_type='text/html')

# Обробник для 404 сторінки


async def handle_error(request):
    return web.Response(
        text=render_template('error.html'), content_type='text/html')

# Налаштування маршрутів


def setup_routes(app):
    app.router.add_get('/', handle_home)  # Головна сторінка
    app.router.add_get('/message', handle_message)  # Сторінка повідомлень
    app.router.add_post('/message', handle_message)  # Обробка повідомлень
    app.router.add_get('/error', handle_error)  # Сторінка 404
