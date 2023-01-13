from unittest import IsolatedAsyncioTestCase, main
from functools import partial

from repositories.payment_statistic_repository import PaymentStatisticRepository
from config.db import MongoClient
from common.promise import Promise
from models.payment_statistic import PaymentStatistic, PaymentStateStatistic, PaymentCityStatistic


class PaymentStatisticRepositoryTests(IsolatedAsyncioTestCase):

    async def test_get_payment_statistic_should_return_empty_list(self) -> None:
        MongoClient().connect()
        payment_statistic_repository = PaymentStatisticRepository()
        payment_statistics: list[PaymentStatistic] = await Promise.resolve(
            partial(payment_statistic_repository.get_payment_statistic, {})
        )
        self.assertCountEqual(payment_statistics, [])

    async def test_get_state_payment_statistic_should_return_empty_list(self) -> None:
        MongoClient().connect()
        payment_statistic_repository = PaymentStatisticRepository()
        payment_state_statistics: list[PaymentStateStatistic] = await Promise.resolve(
            partial(payment_statistic_repository.get_state_payment_statistic, {})
        )
        self.assertCountEqual(payment_state_statistics, [])

    async def test_get_city_payment_statistic_should_return_empty_list(self) -> None:
        MongoClient().connect()
        payment_statistic_repository = PaymentStatisticRepository()
        payment_city_statistics: list[PaymentCityStatistic] = await Promise.resolve(
            partial(payment_statistic_repository.get_city_payment_statistic, {})
        )
        self.assertCountEqual(payment_city_statistics, [])

if __name__ == '__main__':
    main()
