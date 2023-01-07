from bson.objectid import ObjectId

from models.payment_statistic import PaymentStatistic, PaymentStateStatistic, PaymentCityStatistic


class PaymentStatisticRepository:

    @staticmethod
    def get_payment_statistic(query: dict) -> list[PaymentStatistic]:
        return PaymentStatistic.objects(__raw__=query)

    @staticmethod
    def add_payment_statistic(payment: dict) -> None:
        new_payment: PaymentStatistic = PaymentStatistic(**payment)
        new_payment.save()

    @staticmethod
    def update_payment_statistic(pk: str, changes: dict) -> None:
        PaymentStatistic.objects(id=ObjectId(pk)).update_one(**changes)

    @staticmethod
    def get_state_payment_statistic(query: dict) -> list[PaymentStateStatistic]:
        return PaymentStateStatistic.objects(__raw__=query)

    @staticmethod
    def add_state_payment_statistic(payment: dict) -> None:
        new_payment: PaymentStateStatistic = PaymentStateStatistic(**payment)
        new_payment.save()

    @staticmethod
    def update_state_payment_statistic(pk: str, changes: dict) -> None:
        PaymentStateStatistic.objects(id=ObjectId(pk)).update_one(**changes)

    @staticmethod
    def get_city_payment_statistic(query: dict) -> list[PaymentCityStatistic]:
        return PaymentCityStatistic.objects(__raw__=query)

    @staticmethod
    def add_city_payment_statistic(payment: dict) -> None:
        new_payment: PaymentCityStatistic = PaymentCityStatistic(**payment)
        new_payment.save()

    @staticmethod
    def update_city_payment_statistic(pk: str, changes: dict) -> None:
        PaymentCityStatistic.objects(id=ObjectId(pk)).update_one(**changes)
