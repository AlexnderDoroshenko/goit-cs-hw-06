import pytest
from app.mongo_db_client import (
    save_message, get_all_messages, messages_collection)


@pytest.mark.asyncio
async def test_db_connection(mongo_setup):
    """ Перевірка підключення до бази даних """
    db_stats = await messages_collection.database.command("dbstats")
    assert db_stats is not None, "Не вдалося підключитися до бази даних"
    assert "db" in db_stats, "Очікуване поле 'db' відсутнє у статистиці бази"


@pytest.mark.asyncio
async def test_save_message(mongo_setup):
    """ Тест на збереження повідомлення """
    username = "test_user"
    message = "Hello, world!"

    # Викликаємо функцію для збереження повідомлення
    await save_message(username, message)

    # Перевіряємо, чи був вставлений 1 документ у колекцію
    saved_message = await messages_collection.find_one({"username": username})
    assert saved_message is not None, "Повідомлення не було збережено"
    assert saved_message['username'] == username, \
        "Ім'я користувача не збігається"
    assert saved_message['message'] == message, \
        "Текст повідомлення не збігається"
    assert 'date' in saved_message, "Повідомлення не містить поля 'date'"


@pytest.mark.asyncio
async def test_get_all_messages(mongo_setup):
    """ Тест на отримання всіх повідомлень """
    # Додаємо тестові повідомлення у базу
    test_messages = [
        {
            "username": "user1",
            "message": "Message 1",
            "date": "2024-12-16 10:00:00",
        },
        {
            "username": "user2",
            "message": "Message 2",
            "date": "2024-12-16 10:05:00",
        }
    ]
    await messages_collection.insert_many(test_messages)

    # Викликаємо функцію для отримання всіх повідомлень
    messages_cursor = await get_all_messages()
    messages = await messages_cursor.to_list(length=100)

    assert len(messages) > 0, "Список повідомлень порожній"
    assert len(messages) == 2, "Кількість повідомлень не відповідає очікуваній"
    assert messages[0]['username'] == "user1", \
        "Ім'я користувача першого повідомлення не збігається"
    assert messages[1]['message'] == "Message 2", \
        "Текст другого повідомлення не збігається"
