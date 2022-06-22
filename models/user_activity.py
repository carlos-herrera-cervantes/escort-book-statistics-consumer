from datetime import datetime

from mongoengine import *


class GeneralUserActivity(Document):
    active: int = IntField()
    inactive: int = IntField()
    type: str = StringField()
    raw_created_at: str = StringField()
    created_at: datetime = DateTimeField(default=datetime.now())
    meta = {'collection': 'general_user_activity'}


class StateUserActivity(Document):
    active: int = IntField()
    inactive: int = IntField()
    type: str = StringField()
    state: str = StringField()
    raw_created_at: str = StringField()
    created_at: datetime = DateTimeField(default=datetime.now())
    meta = {'collection': 'state_user_activity'}


class CityUserActivity(Document):
    active: int = IntField()
    inactive: int = IntField()
    type: str = StringField()
    city: str = StringField()
    state: str = StringField()
    raw_created_at: str = StringField()
    created_at: datetime = DateTimeField(default=datetime.now())
    meta = {'collection': 'city_user_activity'}
