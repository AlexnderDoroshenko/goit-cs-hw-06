# Використовуємо Python 3.9
FROM python:3.9-slim

# Встановлюємо залежності
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

# Копіюємо весь код в контейнер
COPY ./app /app

# Вказуємо Python-путь для імпорту модулів
ENV PYTHONPATH="/app"

# Відкриваємо порти для HTTP (3000) та WebSocket (5000)
EXPOSE 3000
EXPOSE 5000

# Запускаємо додаток
CMD ["python", "main.py"]
