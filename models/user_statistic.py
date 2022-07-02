from datetime import datetime

from mongoengine import *


class CustomerStatistic(Document):
    customer_id: str = ObjectIdField()
    hired_services: int = IntField(default=0)
    spent_money = DecimalField(default=0)
    raw_created_at: str = StringField()
    created_at: datetime = DateTimeField(default=datetime.now())
    emitted_claims: int = IntField(default=0)
    received_claims: int = IntField(default=0)
    meta = {'collection': 'customer_statistic'}


class EscortStatistic(Document):
    escort_id: str = ObjectIdField()
    services_provided: int = IntField(default=0)
    earned_money = DecimalField(default=0)
    raw_created_at: str = StringField()
    created_at: datetime = DateTimeField(default=datetime.now())
    emitted_claims: int = IntField(default=0)
    received_claims: int = IntField(default=0)
    meta = {'collection': 'escort_statistic'}
