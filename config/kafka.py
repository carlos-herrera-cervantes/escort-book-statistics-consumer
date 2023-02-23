import os

from enum import Enum


class KafkaClient(Enum):
    SERVERS = os.getenv('KAFKA_HOSTS')
    GROUP_ID = "escort-book-statistics-consumer"
