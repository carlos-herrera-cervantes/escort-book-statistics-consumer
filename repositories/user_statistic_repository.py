from __future__ import annotations
import json

from bson.objectid import ObjectId
from bson.json_util import dumps

from models.user_statistic import CustomerStatistic, EscortStatistic


class UserStatisticRepository:

    @staticmethod
    def get_customer_statistic(query: dict) -> CustomerStatistic | None:
        try:
            return CustomerStatistic.objects.get(__raw__=query)
        except Exception as e:
            print('Exception to query customer statistic: ', e)
            return None

    @staticmethod
    def count_customer_statistic(query: dict) -> int:
        return CustomerStatistic.objects(__raw__=query).count()

    @staticmethod
    def add_customer_statistic(statistic: dict) -> None:
        new_statistic: CustomerStatistic = CustomerStatistic(**statistic)
        new_statistic.save()

    @staticmethod
    def update_customer_statistic(pk: str, changes: dict) -> None:
        CustomerStatistic.objects(id=ObjectId(pk)).update_one(**changes)

    @staticmethod
    def get_escort_statistic(query: dict) -> EscortStatistic | None:
        try:
            return EscortStatistic.objects.get(__raw__=query)
        except Exception as e:
            print('Error getting escort statistic: ', e)
            return None

    @staticmethod
    def count_escort_statistic(query: dict) -> int:
        return EscortStatistic.objects(__raw__=query).count()

    @staticmethod
    def add_escort_statistic(statistic: dict) -> None:
        new_statistic: EscortStatistic = EscortStatistic(**statistic)
        new_statistic.save()

    @staticmethod
    def update_escort_statistic(pk: str, changes: dict) -> None:
        EscortStatistic.objects(id=ObjectId(pk)).update_one(**changes)

    @staticmethod
    def sum_services(escort_id: str) -> int:
        pipeline: list = [{'$group': {'_id': '$escort_id', 'total': {'$sum': '$services_provided'}}}]
        cursor = EscortStatistic.objects(__raw__={'escort_id': ObjectId(escort_id)}).aggregate(pipeline)
        results: dict = json.loads(dumps(cursor))

        return results[0]['total'] if results else 0
