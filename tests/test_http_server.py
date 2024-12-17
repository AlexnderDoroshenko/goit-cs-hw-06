import pytest
from app.mongo_db_client import messages_collection

# Тест для головної сторінки


@pytest.mark.asyncio
async def test_home(client):
    resp = await client.get('/')  # Робимо GET-запит на головну сторінку
    assert resp.status == 200  # Перевіряємо статус відповіді
    html = await resp.text()
    # Перевіряємо, чи є в HTML сторінки правильний контент
    assert "<title>Home</title>" in html


# Тест для сторінки повідомлень
@pytest.mark.asyncio
async def test_message_page(client):
    # Робимо GET-запит на сторінку повідомлень
    resp = await client.get('/message')
    assert resp.status == 200  # Перевіряємо статус відповіді
    html = await resp.text()
    assert "Send a message" in html  # Перевіряємо наявність тексту на сторінці


# Тест для обробки форми повідомлення
@pytest.mark.asyncio
async def test_post_message(client):
    # Надсилаємо POST-запит з даними форми
    data = {'username': 'test_user', 'message': 'Test message'}
    resp = await client.post('/message', data=data)

    # Перевіряємо статус відповіді
    assert resp.status == 200
    response_text = await resp.text()
    # Перевіряємо, чи правильно відправлене повідомлення
    assert "Message from test_user: Test message" in response_text

    # Перевіряємо, чи воно потрапило в базу даних (MongoDB)
    # Для цього можна додати тест для перевірки запису в MongoDB, наприклад:
    last_message = await messages_collection.find_one({"username": "test_user"})
    assert last_message is not None
    assert last_message["message"] == "Test message"
    assert last_message["username"] == "test_user"
