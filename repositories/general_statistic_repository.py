from __future__ import annotations

from bson.objectid import ObjectId

from models.general_statistic import GeneralStatistic, StateStatistic, CityStatistic


class GeneralStatisticRepository:

    @staticmethod
    async def get_general_statistic(query: dict) -> GeneralStatistic | None:
        try:
            return GeneralStatistic.objects.get(__raw__=query)
        except Exception as e:
            print('Error getting general statistic: ', e)
            return None

    @staticmethod
    async def get_state_statistic(query: dict) -> StateStatistic | None:
        try:
            return StateStatistic.objects.get(__raw__=query)
        except Exception as e:
            print('Error getting state statistic: ', e)
            return None

    @staticmethod
    async def get_city_statistic(query: dict) -> CityStatistic | None:
        try:
            return CityStatistic.objects.get(__raw__=query)
        except Exception as e:
            print('Error getting city statistic: ', e)
            return None

    @staticmethod
    async def add_general_statistic(statistic: dict) -> None:
        new_statistic: GeneralStatistic = GeneralStatistic(**statistic)
        new_statistic.save()

    @staticmethod
    async def add_state_statistic(statistic: dict) -> None:
        new_statistic: StateStatistic = StateStatistic(**statistic)
        new_statistic.save()

    @staticmethod
    async def add_city_statistic(statistic: dict) -> None:
        new_statistic: CityStatistic = CityStatistic(**statistic)
        new_statistic.save()

    @staticmethod
    async def update_general_statistic(pk: str, changes: dict) -> None:
        GeneralStatistic.objects(id=ObjectId(pk)).update_one(**changes)

    @staticmethod
    async def update_state_statistic(pk: str, changes: dict) -> None:
        StateStatistic.objects(id=ObjectId(pk)).update_one(**changes)

    @staticmethod
    async def update_city_statistic(pk: str, changes: dict) -> None:
        CityStatistic.objects(id=ObjectId(pk)).update_one(**changes)
