from unittest import IsolatedAsyncioTestCase, main
from functools import partial

from repositories.general_statistic_repository import GeneralStatisticRepository
from config.db import MongoClient
from common.promise import Promise
from models.general_statistic import GeneralStatistic, StateStatistic, CityStatistic


class GeneralStatisticRepositoryTests(IsolatedAsyncioTestCase):

    async def test_get_general_statistic_should_return_none(self) -> None:
        MongoClient().connect()
        general_statistic_repository = GeneralStatisticRepository()
        general_statistic: GeneralStatistic | None = await Promise.resolve(
            partial(general_statistic_repository.get_general_statistic, {})
        )
        self.assertIsNone(general_statistic)

    async def test_get_state_statistic_should_return_none(self) -> None:
        MongoClient().connect()
        general_statistic_repository = GeneralStatisticRepository()
        state_statistic: StateStatistic | None = await Promise.resolve(
            partial(general_statistic_repository.get_state_statistic, {})
        )
        self.assertIsNone(state_statistic)

    async def test_get_city_statistic(self) -> None:
        MongoClient().connect()
        general_statistic_repository = GeneralStatisticRepository()
        city_statistic: CityStatistic | None = await Promise.resolve(
            partial(general_statistic_repository.get_city_statistic, {})
        )
        self.assertIsNone(city_statistic)

if __name__ == '__main__':
    main()
