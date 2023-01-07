from __future__ import annotations

from bson.objectid import ObjectId

from models.top_place import TopState, TopCity, TopZone


class TopPlaceRepository:

    @staticmethod
    def get_state(state: str) -> TopState | None:
        try:
            return TopState.objects.get(__raw__={'name': state})
        except Exception as e:
            print('Error getting state: ', e)
            return None

    @staticmethod
    def add_state(state: dict, services: int) -> None:
        threshold_to_gain_state_place = 100000

        if services < threshold_to_gain_state_place:
            return

        new_state: TopState = TopState(**state)
        new_state.save()

    @staticmethod
    def update_state(pk: str, changes: dict) -> None:
        TopState.objects(id=ObjectId(pk)).update_one(**changes)

    @staticmethod
    def get_city(city: str) -> TopCity | None:
        try:
            return TopCity.objects.get(__raw__={'name': city})
        except Exception as e:
            print('Error getting city: ', e)
            return None

    @staticmethod
    def add_city(city: dict, services: int) -> None:
        threshold_to_gain_city_place = 50000

        if services < threshold_to_gain_city_place:
            return

        new_city: TopCity = TopCity(**city)
        new_city.save()

    @staticmethod
    def update_city(pk: str, changes: dict) -> None:
        TopCity.objects(id=ObjectId(pk)).update_one(**changes)

    @staticmethod
    def get_zone(zone: str) -> TopZone | None:
        try:
            return TopZone.objects.get(__raw__={'name': zone})
        except Exception as e:
            print('Error getting zone: ', e)
            return None

    @staticmethod
    def add_zone(zone: dict, services: int) -> None:
        threshold_to_gain_zone_place = 10000

        if services < threshold_to_gain_zone_place:
            return

        new_zone: TopZone = TopZone(**zone)
        new_zone.save()

    @staticmethod
    def update_zone(pk: str, changes: dict) -> None:
        TopZone.objects(id=ObjectId(pk)).update_one(**changes)
