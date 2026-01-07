import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ConfigurationError
import logging

logger = logging.getLogger("core.db.mongo")
logger.setLevel(logging.INFO)

MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
MONGO_PORT = int(os.getenv("MONGO_PORT", 27017))
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "todo_db")
MONGO_USER = os.getenv("MONGO_USER", "")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD", "")

if MONGO_USER and MONGO_PASSWORD:
    MONGO_URI = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB_NAME}"
else:
    MONGO_URI = f"mongodb://{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB_NAME}"


class MongoConnection:
    """
    Singleton MongoDB connection manager with connection pooling.
    Use get_db() to access the database object.
    """

    _client: MongoClient = None
    _db = None

    @classmethod
    def connect(cls):
        if cls._client is None:
            try:
                cls._client = MongoClient(
                    MONGO_URI,
                    maxPoolSize=50,
                    minPoolSize=5,
                    serverSelectionTimeoutMS=5000
                )

                cls._client.server_info()
                cls._db = cls._client[MONGO_DB_NAME]
                logger.info(f"[MongoDB] Connected to {MONGO_DB_NAME} at {MONGO_HOST}:{MONGO_PORT}")
            except (ConnectionFailure, ConfigurationError) as e:
                logger.error(f"[MongoDB] Connection failed: {e}")
                raise

        return cls._db

    @classmethod
    def get_db(cls):
        if cls._db is None:
            return cls.connect()
        return cls._db

    @classmethod
    def close(cls):
        if cls._client:
            cls._client.close()
            cls._client = None
            cls._db = None
            logger.info("[MongoDB] Connection closed")


def get_collection(name: str):
    return MongoConnection.get_db()[name]
