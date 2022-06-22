from __future__ import annotations
import json

from bson.objectid import ObjectId
from bson.json_util import dumps

from models.top_escort import TopGeneralEscort, TopStateEscort, TopCityEscort


class TopEscortRepository:

    @staticmethod
    async def get_general_place(escort_id: str) -> TopGeneralEscort | None:
        try:
            return TopGeneralEscort.objects.get(__raw__={'escort_id': ObjectId(escort_id)})
        except Exception as e:
            print('Error getting general place: ', e)
            return None

    @staticmethod
    async def add_general_place(escort: dict, services: int) -> None:
        if services < 100:
            return

        top: TopGeneralEscort = TopGeneralEscort(**escort)
        top.save()

    @staticmethod
    async def update_general_place(escort_id: id, changes: dict) -> None:
        TopGeneralEscort.objects(id=ObjectId(escort_id)).update_one(**changes)

    @staticmethod
    async def get_state_place(escort_id: str) -> TopStateEscort | None:
        try:
            return TopStateEscort.objects.get(__raw__={'escort_id': ObjectId(escort_id)})
        except Exception as e:
            print('Error getting state place: ', e)
            return None

    @staticmethod
    async def count_services_by_state(state: str) -> int:
        pipeline: list = [{'$group': {'_id': None, 'total': {'$sum': '$services'}}}]
        cursor = TopStateEscort.objects(__raw__={'state': state}).aggregate(pipeline)
        results: dict = json.loads(dumps(cursor))

        return results[0]['total'] if len(results) else 0

    @staticmethod
    async def add_state_place(escort: dict, services: int) -> None:
        if services < 50:
            return
        
        top: TopStateEscort = TopStateEscort(**escort)
        top.save()

    @staticmethod
    async def update_state_place(escort_id: str, changes: dict) -> None:
        TopStateEscort.objects(id=ObjectId(escort_id)).update_one(**changes)

    @staticmethod
    async def get_city_place(escort_id: str) -> TopCityEscort | None:
        try:
            return TopCityEscort.objects.get(__raw__={'escort_id': ObjectId(escort_id)})
        except Exception as e:
            print('Error getting city place: ', e)
            return None

    @staticmethod
    async def count_services_by_city(city: str) -> int:
        pipeline: list = [{'$group': {'_id': None, 'total': {'$sum': '$services'}}}]
        cursor = TopStateEscort.objects(__raw__={'city': city}).aggregate(pipeline)
        results: dict = json.loads(dumps(cursor))

        return results[0]['total'] if len(results) else 0

    @staticmethod
    async def add_city_place(escort: dict, services: int) -> None:
        if services < 25:
            return

        top: TopCityEscort = TopCityEscort(**escort)
        top.save()

    @staticmethod
    async def update_city_place(escort_id: str, changes: dict) -> None:
        TopCityEscort.objects(id=ObjectId(escort_id)).update_one(**changes)
