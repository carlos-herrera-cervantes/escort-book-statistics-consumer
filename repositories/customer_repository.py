from psycopg2._psycopg import connection, cursor


class CustomerRepository:

    def __init__(self, postgres_client: connection):
        self.__postgres_client = postgres_client

    def count(self) -> int:
        conn: cursor = self.__postgres_client.cursor()
        conn.execute('SELECT COUNT(*) FROM profile;')
        counter: list = conn.fetchone()

        return counter[0]
