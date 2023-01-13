import mongoengine
import psycopg2

from common.singleton import SingletonMeta
from config.mongo import MongoClient as MongoSettings
from config.postgres import PostgresClient as PostgresSettings, PostgresDB


class MongoClient(metaclass=SingletonMeta):

    def __init__(self) -> None:
        self.__db = MongoSettings.MONGO_URI.value

    def connect(self) -> None:
        print('Successful connected to Mongo DB')
        mongoengine.connect(host=self.__db)


class PostgresClient(metaclass=SingletonMeta):

    def __init__(self) -> None:
        self.__tracking_db = (
            f'dbname={PostgresDB.TRACKING.value} ' +
            f'user={PostgresSettings.USER_DB.value} ' +
            f'password={PostgresSettings.PASSWORD_DB.value} ' +
            f'host={PostgresSettings.TRACKING_DB_HOST.value} ' +
            f'port={PostgresSettings.PORT_DB.value}'
        )
        self.__escort_db = (
            f'dbname={PostgresDB.ESCORT.value} ' +
            f'user={PostgresSettings.USER_DB.value} ' +
            f'password={PostgresSettings.PASSWORD_DB.value} ' +
            f'host={PostgresSettings.ESCORT_DB_HOST.value} ' +
            f'port={PostgresSettings.PORT_DB.value}'
        )
        self.__customer_db = (
            f'dbname={PostgresDB.CUSTOMER.value} ' +
            f'user={PostgresSettings.USER_DB.value} ' +
            f'password={PostgresSettings.PASSWORD_DB.value} ' +
            f'host={PostgresSettings.CUSTOMER_DB_HOST.value} ' +
            f'port={PostgresSettings.PORT_DB.value}'
        )

    def connect(self) -> dict:
        connections: dict = {
            'tracking_db': psycopg2.connect(self.__tracking_db),
            'escort_db': psycopg2.connect(self.__escort_db),
            'customer_db': psycopg2.connect(self.__customer_db),
        }
        print('Successful connected to Postgres')
        return connections
