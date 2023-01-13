from unittest import IsolatedAsyncioTestCase, main
from functools import partial

from repositories.top_escort_repository import TopEscortRepository
from config.db import MongoClient
from common.promise import Promise
from models.top_escort import TopGeneralEscort, TopStateEscort, TopCityEscort


class TopEscortRepositoryTests(IsolatedAsyncioTestCase):

    async def test_get_general_place_should_return_none(self) -> None:
        MongoClient().connect()
        top_escort_repository = TopEscortRepository()
        top_general_escort: TopGeneralEscort | None = await Promise.resolve(
            partial(top_escort_repository.get_general_place, '63ba464315a031e5004079de')
        )
        self.assertIsNone(top_general_escort)

    async def test_get_state_place_should_return_none(self) -> None:
        MongoClient().connect()
        top_escort_repository = TopEscortRepository()
        top_state_escort: TopStateEscort | None = await Promise.resolve(
            partial(top_escort_repository.get_state_place, '63ba48ec930f2ad8b1ca404e')
        )
        self.assertIsNone(top_state_escort)

    async def test_count_services_by_state_should_return_0(self) -> None:
        MongoClient().connect()
        top_escort_repository = TopEscortRepository()
        counter: int = await Promise.resolve(
            partial(top_escort_repository.count_services_by_state, 'guerrero')
        )
        self.assertIs(counter, 0)

    async def test_get_city_place_should_return_none(self) -> None:
        MongoClient().connect()
        top_escort_repository = TopEscortRepository()
        top_city_escort: TopCityEscort | None = await Promise.resolve(
            partial(top_escort_repository.get_city_place, '63ba4befaccdecfcb24a416c')
        )
        self.assertIsNone(top_city_escort)

    async def test_count_services_by_city_should_return_0(self) -> None:
        MongoClient().connect()
        top_escort_repository = TopEscortRepository()
        counter: int = await Promise.resolve(
            partial(top_escort_repository.count_services_by_city, 'acapulco')
        )
        self.assertIs(counter, 0)

if __name__ == '__main__':
    main()
