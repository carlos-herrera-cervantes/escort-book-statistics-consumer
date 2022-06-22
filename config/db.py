import os

import mongoengine
import psycopg2

from config.singleton import SingletonMeta


class MongoClient(metaclass=SingletonMeta):

    def __init__(self) -> None:
        self.__db = os.getenv('MONGO_DB')

    def connect(self) -> None:
        print('Successful connected to Mongo DB')
        mongoengine.connect(self.__db)


class PostgresClient(metaclass=SingletonMeta):

    def __init__(self) -> None:
        user_db: str = os.getenv('USER_DB')
        password_db: str = os.getenv('PASS_DB')
        host_db: str = os.getenv('HOST_DB')
        port_db: int = int(os.getenv('PORT_DB'))

        self.__tracking_db = (
            f'dbname={os.getenv("TRACKING_DB")} user={user_db} password={password_db} host={host_db} port={port_db}'
        )
        self.__escort_db = (
            f'dbname={os.getenv("ESCORT_DB")} user={user_db} password={password_db} host={host_db} port={port_db}'
        )
        self.__customer_db = (
            f'dbname={os.getenv("CUSTOMER_DB")} user={user_db} password={password_db} host={host_db} port={port_db}'
        )

    def connect(self) -> dict:
        connections: dict = {
            'tracking_db': psycopg2.connect(self.__tracking_db),
            'escort_db': psycopg2.connect(self.__escort_db),
            'customer_db': psycopg2.connect(self.__customer_db),
        }
        print('Successful connected to Postgres')
        return connections
