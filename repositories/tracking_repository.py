from psycopg2._psycopg import connection, cursor

from models.location import Location


class TrackingRepository:

    def __init__(self, postgres_client: connection) -> None:
        self.__postgres_client = postgres_client

    def get_escort_location(self, escort_id: str) -> Location:
        conn: cursor = self.__postgres_client.cursor()
        query: str = (
            'SELECT a.escort_id, b.name, c.name, d.name FROM escort_tracking AS a ' +
            'JOIN territory AS b ON st_intersects(a.location, b.location) ' +
            'JOIN state AS c ON b.state_id = c.id '
            'JOIN country AS d ON c.country_id = d.id '
            f"WHERE a.escort_id = '{escort_id}'"
        )
        conn.execute(query)
        rows: list = conn.fetchall()

        try:
            location: Location = Location()
            location.city = rows[0][1]
            location.state = rows[0][2]
            location.country = rows[0][3]

            return location
        except Exception as e:
            print('Error getting escort location: ', e)
            return None

    def get_customer_location(self, customer_id: str) -> Location:
        conn: cursor = self.__postgres_client.cursor()
        query: str = (
            'SELECT a.customer_id, b.name, c.name, d.name FROM customer_tracking AS a ' +
            'JOIN territory AS b ON st_intersects(a.location, b.location) ' +
            'JOIN state AS c ON b.state_id = c.id '
            'JOIN country AS d ON c.country_id = d.id '
            f"WHERE a.customer_id = '{customer_id}'"
        )

        conn.execute(query)
        rows: list = conn.fetchall()

        try:
            location: Location = Location()
            location.city = rows[0][1]
            location.state = rows[0][2]
            location.country = rows[0][3]

            return location
        except Exception as e:
            print('Error getting customer location: ', e)
            return None

    def count_customers_by_city(self, city: str) -> int:
        conn: cursor = self.__postgres_client.cursor()
        query: str = (
            'SELECT COUNT(a.*) FROM customer_tracking AS a ' +
            'JOIN territory AS b ON st_intersects(a.location, b.location) ' +
            f"WHERE b.name = '{city}'"
        )
        conn.execute(query)
        counter: list = conn.fetchone()

        return counter[0]

    def count_escorts_by_city(self, city: str) -> int:
        conn: cursor = self.__postgres_client.cursor()
        query: str = (
            'SELECT COUNT(a.*) FROM escort_tracking AS a ' +
            'JOIN territory AS b ON st_intersects(a.location, b.location) ' +
            f"WHERE b.name = '{city}'"
        )
        conn.execute(query)
        counter: list = conn.fetchone()

        return counter[0]
