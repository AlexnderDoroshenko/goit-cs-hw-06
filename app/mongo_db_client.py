import datetime
import os
from dotenv import load_dotenv
from pymongo import MongoClient

from logger import get_logger

log = get_logger("mongo_db_client")


# Load environment variables from the .env file (if present)
load_dotenv()
USER = os.environ.get("MONGO_INITDB_ROOT_USERNAME")
PASSWORD = os.environ.get("MONGO_INITDB_ROOT_PASSWORD")
DB_NAME = os.environ.get("MONGO_INITDB_DATABASE")
MONGO_URI = os.environ.get("MONGO_URI") \
    or f"mongodb://{USER}:{PASSWORD}@mongodb:27017"

log.debug(MONGO_URI)
if "None" in MONGO_URI:
    raise ValueError(
        "Some credentials are missed in MONGO_URI and value has None")

# Підключення до MongoDB
try:
    client = MongoClient(MONGO_URI)
except Exception as err:
    log.error(err)
db = client[DB_NAME]
messages_collection = db['messages']


def save_message(username, message):
    message_doc = {
        "username": username,
        "message": message,
        "date": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    result = messages_collection.insert_one(message_doc)
    log.info(f"result is {result}")
    return result


def get_all_messages():
    messages = messages_collection.find({})
    log.info(f'Founded {len(messages)} records in {DB_NAME}.messages')
    return messages
