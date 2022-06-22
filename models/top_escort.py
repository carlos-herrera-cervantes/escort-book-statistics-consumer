from datetime import datetime

from mongoengine import *


class TopGeneralEscort(Document):
    escort_id: str = ObjectIdField()
    name: str = StringField()
    services: int = IntField(default=100)
    created_at: datetime = DateTimeField(default=datetime.now())


class TopStateEscort(Document):
    escort_id: str = ObjectIdField()
    name: str = StringField()
    state: str = StringField()
    services: int = IntField(default=50)
    created_at: datetime = DateTimeField(default=datetime.now())


class TopCityEscort(Document):
    escort_id: str = ObjectIdField()
    name: str = StringField()
    city: str = StringField()
    state: str = StringField()
    services: int = IntField(default=25)
    created_at: datetime = DateTimeField(default=datetime.now())
