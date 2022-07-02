from datetime import datetime

from mongoengine import *


class TopState(Document):
    name: str = StringField()
    services: int = IntField()
    created_at: datetime = DateTimeField(default=datetime.now())


class TopCity(Document):
    name: str = StringField()
    state: str = StringField()
    services: int = IntField()
    created_at: datetime = DateTimeField(default=datetime.now())


class TopZone(Document):
    name: str = StringField()
    city: str = StringField()
    state: str = StringField()
    services: int = IntField()
    created_at: datetime = DateTimeField(default=datetime.now())
