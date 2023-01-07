from unittest import IsolatedAsyncioTestCase, main
from functools import partial

from repositories.user_statistic_repository import UserStatisticRepository
from config.db import MongoClient
from common.promise import Promise
from models.user_statistic import CustomerStatistic, EscortStatistic


class UserStatisticRepositoryTests(IsolatedAsyncioTestCase):

    async def test_get_customer_statistic_should_return_none(self) -> None:
        MongoClient().connect()
        user_statistic_repository = UserStatisticRepository()
        customer_statistic: CustomerStatistic | None = await Promise.resolve(
            partial(user_statistic_repository.get_customer_statistic, {})
        )
        self.assertIsNone(customer_statistic)

    async def test_count_customer_statistic_should_return_0(self) -> None:
        MongoClient().connect()
        user_statistic_repository = UserStatisticRepository()
        counter: int = await Promise.resolve(
            partial(user_statistic_repository.count_customer_statistic, {})
        )
        self.assertIs(counter, 0)

    async def test_get_escort_statistic_should_return_none(self) -> None:
        MongoClient().connect()
        user_statistic_repository = UserStatisticRepository()
        escort_statistic: EscortStatistic | None = await Promise.resolve(
            partial(user_statistic_repository.get_escort_statistic, {})
        )
        self.assertIsNone(escort_statistic)

    async def test_count_escort_statistic_should_return_0(self) -> None:
        MongoClient().connect()
        user_statistic_repository = UserStatisticRepository()
        counter: int = await Promise.resolve(
            partial(user_statistic_repository.count_escort_statistic, {})
        )
        self.assertIs(counter, 0)

    async def test_sum_services_should_return_0(self) -> None:
        MongoClient().connect()
        user_statistic_repository = UserStatisticRepository()
        counter: int = await Promise.resolve(
            partial(user_statistic_repository.sum_services, '63bae7bae66d7087123ec95d')
        )
        self.assertIs(counter, 0)

if __name__ == '__main__':
    main()
