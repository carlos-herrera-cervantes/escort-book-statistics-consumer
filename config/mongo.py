import os

from enum import Enum


class MongoClient(Enum):
    MONGO_URI = os.getenv('MONGO_DB')
