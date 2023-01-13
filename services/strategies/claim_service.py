import asyncio
from datetime import date
from functools import partial

from bson.objectid import ObjectId

from services.interfaces.strategy_interface import Strategy
from repositories.general_statistic_repository import GeneralStatisticRepository
from repositories.user_statistic_repository import UserStatisticRepository
from repositories.tracking_repository import TrackingRepository
from models.general_statistic import GeneralStatistic, StateStatistic, CityStatistic
from models.location import Location
from models.user_statistic import CustomerStatistic, EscortStatistic
from common.promise import Promise


class ClaimService(Strategy):

    def __init__(
        self,
        general_statistic_repository: GeneralStatisticRepository,
        user_statistic_repository: UserStatisticRepository,
        tracking_repository: TrackingRepository
    ):
        self.__general_statistic_repository = general_statistic_repository
        self.__user_statistic_repository = user_statistic_repository
        self.__tracking_repository = tracking_repository

    async def __process_claim(self, today: str) -> None:
        query = {'raw_created_at': today}
        statistic: GeneralStatistic = await Promise.resolve(
            partial(self.__general_statistic_repository.get_general_statistic, query)
        )

        if not statistic:
            new_statistic = {'claims': 1, 'raw_created_at': today}
            await Promise.resolve(
                partial(self.__general_statistic_repository.add_general_statistic, new_statistic)
            )
            return

        changes = {'claims': statistic.claims + 1}
        await Promise.resolve(
            partial(self.__general_statistic_repository.update_general_statistic, statistic.id, changes)
        )

    async def __process_state_claim(self, today: str, location: Location) -> None:
        query = {'raw_created_at': today, 'state': location.state}
        statistic: StateStatistic = await Promise.resolve(
            partial(self.__general_statistic_repository.get_state_statistic, query)
        )

        if not statistic:
            new_statistic = {'claims': 1, 'raw_created_at': today, 'state': location.state}
            await Promise.resolve(
                partial(self.__general_statistic_repository.add_state_statistic, new_statistic)
            )
            return

        changes = {'claims': statistic.claims + 1}
        await Promise.resolve(
            partial(self.__general_statistic_repository.update_state_statistic, statistic.id, changes)
        )

    async def __process_city_claim(self, today: str, location: Location) -> None:
        query = {'raw_created_at': today, 'city': location.city}
        statistic: CityStatistic = await Promise.resolve(
            partial(self.__general_statistic_repository.get_city_statistic, query)
        )

        if not statistic:
            new_statistic = {
                'claims': 1,
                'raw_created_at': today,
                'state': location.state,
                'city': location.city,
            }
            await Promise.resolve(
                partial(self.__general_statistic_repository.add_city_statistic, new_statistic)
            )
            return

        changes = {'claims': statistic.claims + 1}
        await Promise.resolve(
            partial(self.__general_statistic_repository.update_city_statistic, statistic.id, changes)
        )

    async def __process_customer_claim(self, message: dict, today: str) -> None:
        query = {'raw_created_at': today, 'customer_id': ObjectId(message['customerId'])}
        statistic: CustomerStatistic = await Promise.resolve(
            partial(self.__user_statistic_repository.get_customer_statistic, query)
        )

        if not statistic:
            new_statistic = {
                'customer_id': message['customerId'],
                'raw_created_at': today,
                'emitted_claims': 0 if message['to'] == 'Customer' else 1,
                'received_claims': 0 if message['to'] == 'Escort' else 1,
            }
            await Promise.resolve(
                partial(self.__user_statistic_repository.add_customer_statistic, new_statistic)
            )
            return

        changes = {
            'emitted_claims':(
                statistic.emitted_claims if message['to'] == 'Customer' else statistic.emitted_claims + 1
            ),
            'received_claims': (
                statistic.received_claims if message['to'] == 'Escort' else statistic.received_claims + 1
            ),
        }
        await Promise.resolve(
            partial(self.__user_statistic_repository.update_customer_statistic, statistic.id, changes)
        )

    async def __process_escort_claim(self, message: dict, today: str) -> None:
        query = {'raw_created_at': today, 'escort_id': ObjectId(message['escortId'])}
        statistic: EscortStatistic = await Promise.resolve(
            partial(self.__user_statistic_repository.get_escort_statistic, query)
        )

        if not statistic:
            new_statistic = {
                'escort_id': message['escortId'],
                'raw_created_at': today,
                'emitted_claims': 0 if message['to'] == 'Escort' else 1,
                'received_claims': 0 if message['to'] == 'Customer' else 1,
            }
            await Promise.resolve(
                partial(self.__user_statistic_repository.add_escort_statistic, new_statistic)
            )
            return

        changes = {
            'emitted_claims':(
                statistic.emitted_claims if message['to'] == 'Escort' else statistic.emitted_claims + 1
            ),
            'received_claims': (
                statistic.received_claims if message['to'] == 'Customer' else statistic.received_claims + 1
            ),
        }
        await Promise.resolve(
            partial(self.__user_statistic_repository.update_escort_statistic, statistic.id, changes)
        )

    async def process_message(self, message: dict) -> None:
        today: str = date.today().strftime('%Y-%m-%d')
        location: Location = await Promise.resolve(
            partial(self.__tracking_repository.get_escort_location, message['escortId'])
        )

        tasks: list = [
            self.__process_claim(today),
            self.__process_state_claim(today, location),
            self.__process_city_claim(today, location),
            self.__process_customer_claim(message, today),
            self.__process_escort_claim(message, today),
        ]

        await asyncio.gather(*tasks)
