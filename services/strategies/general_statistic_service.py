import asyncio
from datetime import date
from functools import partial

from repositories.general_statistic_repository import GeneralStatisticRepository
from repositories.tracking_repository import TrackingRepository
from models.general_statistic import GeneralStatistic, StateStatistic, CityStatistic
from models.location import Location
from services.interfaces.strategy_interface import Strategy
from common.promise import Promise


class GeneralStatisticService(Strategy):

    def __init__(
        self,
        general_statistic_repository: GeneralStatisticRepository,
        tracking_repository: TrackingRepository,
    ):
        self.__general_statistic_repository = general_statistic_repository
        self.__tracking_repository = tracking_repository

    async def __process_general_statistic(self, message: dict, today: str) -> None:
        query = {'raw_created_at': today}
        statistic: GeneralStatistic = await Promise.resolve(
            partial(self.__general_statistic_repository.get_general_statistic, query)
        )

        user_type: str = message['userType']

        if not statistic:
            new_statistic = {
                'total_customers': 1 if user_type == 'Customer' else 0,
                'total_escorts': 1 if user_type == 'Escort' else 0,
                'raw_created_at': today,
            }
            await Promise.resolve(
                partial(self.__general_statistic_repository.add_general_statistic, new_statistic)
            )
            return

        total_customers: int = statistic.total_customers
        total_escorts: int = statistic.total_escorts
        changes = {
            'total_customers': 1 + total_customers if user_type == 'Customer' else total_customers,
            'total_escorts': 1 + total_escorts if user_type == 'Escort' else total_escorts,
        }
        await Promise.resolve(
            partial(self.__general_statistic_repository.update_general_statistic, statistic.id, changes)
        )

    async def __process_state_statistic(self, message: dict, today: str, location: Location) -> None:
        query = {'raw_created_at': today, 'state': location.state}
        statistic: StateStatistic = await Promise.resolve(
            partial(self.__general_statistic_repository.get_state_statistic, query)
        )

        user_type: str = message['userType']

        if not statistic:
            new_statistic = {
                'total_customers': 1 if user_type == 'Customer' else 0,
                'total_escorts': 1 if user_type == 'Escort' else 0,
                'state': location.state,
                'raw_created_at': today,
            }
            await Promise.resolve(
                partial(self.__general_statistic_repository.add_state_statistic, new_statistic)
            )
            return

        total_customers: int = statistic.total_customers
        total_escorts: int = statistic.total_escorts
        changes = {
            'total_customers': 1 + total_customers if user_type == 'Customer' else total_customers,
            'total_escorts': 1 + total_escorts if user_type == 'Escort' else total_escorts,
        }
        await Promise.resolve(
            partial(self.__general_statistic_repository.update_state_statistic, statistic.id, changes)
        )

    async def __process_city_statistic(self, message: dict, today: str, location: Location) -> None:
        query = {'raw_created_at': today, 'city': location.city}
        statistic: CityStatistic = await Promise.resolve(
            partial(self.__general_statistic_repository.get_city_statistic, query)
        )

        user_type: str = message['userType']

        if not statistic:
            new_statistic = {
                'total_customers': 1 if user_type == 'Customer' else 0,
                'total_escorts': 1 if user_type == 'Escort' else 0,
                'state': location.state,
                'city': location.city,
                'raw_created_at': today,
            }
            await Promise.resolve(
                partial(self.__general_statistic_repository.add_city_statistic, new_statistic)
            )
            return

        total_customers: int = statistic.total_customers
        total_escorts: int = statistic.total_escorts
        changes = {
            'total_customers': 1 + total_customers if user_type == 'Customer' else total_customers,
            'total_escorts': 1 + total_escorts if user_type == 'Escort' else total_escorts,
        }
        await Promise.resolve(
            partial(self.__general_statistic_repository.update_city_statistic, statistic.id, changes)
        )

    async def process_message(self, message: dict) -> None:
        today: str = date.today().strftime('%Y-%m-%d')
        location: Location = (
            await Promise.resolve(
                partial(self.__tracking_repository.get_escort_location, message['userId'])
            )
            if message['userType'] == 'Escort' else
            await Promise.resolve(
                partial(self.__tracking_repository.get_customer_location, message['userId'])
            )
        )

        tasks: list = [
            self.__process_general_statistic(message, today),
            self.__process_state_statistic(message, today, location),
            self.__process_city_statistic(message, today, location),
        ]

        await asyncio.gather(*tasks)
