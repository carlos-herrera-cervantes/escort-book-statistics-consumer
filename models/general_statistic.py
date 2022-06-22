from mongoengine import *

from datetime import datetime


class GeneralStatistic(Document):
    total_customers: int = IntField(default=0)
    total_escorts: int = IntField(default=0)
    earnings = DecimalField(default=0)
    raw_created_at: str = StringField()
    created_at: datetime = DateTimeField(default=datetime.now())


class StateStatistic(Document):
    total_customers: int = IntField(default=0)
    total_escorts: int = IntField(default=0)
    earnings = DecimalField(default=0)
    state: str = StringField()
    raw_created_at: str = StringField()
    created_at: datetime = DateTimeField(default=datetime.now())


class CityStatistic(Document):
    total_customers: int = IntField(default=0)
    total_escorts: int = IntField(default=0)
    earnings = DecimalField(default=0)
    city: str = StringField()
    state: str = StringField()
    raw_created_at: str = StringField()
    created_at: datetime = DateTimeField(default=datetime.now())
