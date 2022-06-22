from __future__ import annotations

from bson.objectid import ObjectId

from models.user_activity import GeneralUserActivity, StateUserActivity, CityUserActivity


class UserActivityRepository:

    @staticmethod
    async def get_general_user_activity(query: dict) -> GeneralUserActivity | None:
        try:
            return GeneralUserActivity.objects.get(__raw__=query)
        except Exception as e:
            print('Error getting general user activity: ', e)
            return None

    @staticmethod
    async def add_general_user_activity(activity: dict) -> None:
        new_activity: GeneralUserActivity = GeneralUserActivity(**activity)
        new_activity.save()

    @staticmethod
    async def update_general_user_activity(pk: str, changes: dict) -> None:
        GeneralUserActivity.objects(id=ObjectId(pk)).update_one(**changes)

    @staticmethod
    async def get_state_user_activity(query: dict) -> StateUserActivity | None:
        try:
            return StateUserActivity.objects.get(__raw__=query)
        except Exception as e:
            print('Error getting state user activity: ', e)
            return None

    @staticmethod
    async def add_state_user_activity(activity: dict) -> None:
        new_activity: StateUserActivity = StateUserActivity(**activity)
        new_activity.save()

    @staticmethod
    async def update_state_user_activity(pk: str, changes: dict) -> None:
        StateUserActivity.objects(id=ObjectId(pk)).update_one(**changes)

    @staticmethod
    async def get_city_user_activity(query: dict) -> CityUserActivity | None:
        try:
            return CityUserActivity.objects.get(__raw__=query)
        except Exception as e:
            print('Error getting city user activity: ', e)
            return None

    @staticmethod
    async def add_city_user_activity(activity: dict) -> None:
        new_activity: CityUserActivity = CityUserActivity(**activity)
        new_activity.save()

    @staticmethod
    async def update_city_user_activity(pk: str, changes: dict) -> None:
        CityUserActivity.objects(id=ObjectId(pk)).update_one(**changes)
