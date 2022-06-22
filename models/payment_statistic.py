from datetime import datetime

from mongoengine import *


class PaymentStatistic(Document):
    name: str = StringField()
    services: int = IntField(default=1)
    raw_created_at: str = StringField()
    created_at: datetime = DateTimeField(default=datetime.now())
    meta = {'collection': 'payment_statistic'}


class PaymentStateStatistic(Document):
    name: str = StringField()
    services: int = IntField(default=1)
    state: str = StringField()
    raw_created_at: str = StringField()
    created_at: datetime = DateTimeField(default=datetime.now())
    meta = {'collection': 'payment_state_statistic'}


class PaymentCityStatistic(Document):
    name: str = StringField()
    services: int = IntField(default=1)
    state: str = StringField()
    city: str = StringField()
    raw_created_at: str = StringField()
    created_at: datetime = DateTimeField(default=datetime.now())
    meta = {'collection': 'payment_city_statistic'}
