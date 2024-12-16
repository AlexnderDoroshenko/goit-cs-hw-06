import motor.motor_asyncio
import datetime
import os

from main import logger


USER = os.environ.get("MONGO_INITDB_ROOT_USERNAME")
PASSWORD = os.environ.get("MONGO_INITDB_ROOT_PASSWORD")
DB_NAME = os.environ.get("MONGO_INITDB_DATABASE")
MONGO_URI = os.environ.get("MONGO_URI") \
    or f"mongodb://{USER}:{PASSWORD}@localhost:27017"
if "None" in MONGO_URI:
    raise ValueError(
        "Some credentials are missed in MONGO_URI and value has None")

# Підключення до MongoDB
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]
messages_collection = db['messages']


async def save_message(username, message):
    message_doc = {
        "username": username,
        "message": message,
        "date": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    await messages_collection.insert_one(message_doc)
    logger.info(messages_collection.find())

# TODO : Finish db insertion for docker.
