import os

from enum import Enum


class PostgresClient(Enum):
    USER_DB = str = os.getenv('USER_DB')
    PASSWORD_DB = os.getenv('PASS_DB')
    PORT_DB = int(os.getenv('PORT_DB'))
    TRACKING_DB_HOST = os.getenv('TRACKING_DB_HOST')
    ESCORT_DB_HOST = os.getenv('ESCORT_DB_HOST')
    CUSTOMER_DB_HOST = os.getenv('CUSTOMER_DB_HOST')


class PostgresDB(Enum):
    TRACKING = os.getenv("TRACKING_DB")
    ESCORT = os.getenv("ESCORT_DB")
    CUSTOMER = os.getenv("CUSTOMER_DB")
