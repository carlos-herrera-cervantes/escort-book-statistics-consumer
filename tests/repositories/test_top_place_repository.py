from unittest import IsolatedAsyncioTestCase, main
from functools import partial

from repositories.top_place_repository import TopPlaceRepository
from config.db import MongoClient
from common.promise import Promise
from models.top_place import TopState, TopCity, TopZone


class TopPlaceRepositoryTests(IsolatedAsyncioTestCase):

    async def test_get_state_should_return_none(self) -> None:
        MongoClient().connect()
        top_place_repository = TopPlaceRepository()
        top_state: TopState | None = await Promise.resolve(
            partial(top_place_repository.get_state, 'guerrero')
        )
        self.assertIsNone(top_state)

    async def test_get_city_should_return_none(self) -> None:
        MongoClient().connect()
        top_place_repository = TopPlaceRepository()
        top_city: TopCity | None = await Promise.resolve(
            partial(top_place_repository.get_city, 'acapulco')
        )
        self.assertIsNone(top_city)

    async def test_get_zone_should_return_none(self) -> None:
        MongoClient().connect()
        top_place_repository = TopPlaceRepository()
        top_zone: TopZone | None = await Promise.resolve(
            partial(top_place_repository.get_zone, 'centro')
        )
        self.assertIsNone(top_zone)

if __name__ == '__main__':
    main()
