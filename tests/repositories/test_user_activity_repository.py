from unittest import IsolatedAsyncioTestCase, main
from functools import partial

from repositories.user_activity_repository import UserActivityRepository
from config.db import MongoClient
from common.promise import Promise
from models.user_activity import GeneralUserActivity, StateUserActivity, CityUserActivity


class UserActivityRepositoryTests(IsolatedAsyncioTestCase):

    async def test_get_general_user_activity_should_return_none(self) -> None:
        MongoClient().connect()
        user_activity_repository = UserActivityRepository()
        general_user_activity: GeneralUserActivity | None = await Promise.resolve(
            partial(user_activity_repository.get_general_user_activity, {})
        )
        self.assertIsNone(general_user_activity)

    async def test_get_state_user_activity_should_return_none(self) -> None:
        MongoClient().connect()
        user_activity_repository = UserActivityRepository()
        state_user_activity: StateUserActivity | None = await Promise.resolve(
            partial(user_activity_repository.get_state_user_activity, {})
        )
        self.assertIsNone(state_user_activity)

    async def test_get_city_user_activity_should_return_none(self) -> None:
        MongoClient().connect()
        user_activity_repository = UserActivityRepository()
        city_user_activity: CityUserActivity | None = await Promise.resolve(
            partial(user_activity_repository.get_city_user_activity, {})
        )
        self.assertIsNone(city_user_activity)

if __name__ == '__main__':
    main()
