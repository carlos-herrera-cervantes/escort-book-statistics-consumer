import asyncio
from datetime import date

from bson.objectid import ObjectId

from services.interfaces.strategy_interface import Strategy
from repositories.user_statistic_repository import UserStatisticRepository
from repositories.customer_repository import CustomerRepository
from repositories.escort_repository import EscortRepository
from repositories.user_activity_repository import UserActivityRepository
from repositories.tracking_repository import TrackingRepository
from repositories.general_statistic_repository import GeneralStatisticRepository
from repositories.top_escort_repository import TopEscortRepository
from repositories.top_place_repository import TopPlaceRepository
from repositories.payment_statistic_repository import PaymentStatisticRepository
from models.user_statistic import CustomerStatistic, EscortStatistic
from models.user_activity import GeneralUserActivity, StateUserActivity, CityUserActivity
from models.location import Location
from models.general_statistic import GeneralStatistic, StateStatistic, CityStatistic
from models.top_escort import TopGeneralEscort, TopStateEscort, TopCityEscort
from models.escort_profile import EscortProfile
from models.top_place import TopState, TopCity
from models.payment_statistic import PaymentStatistic, PaymentStateStatistic, PaymentCityStatistic


class PaymentService(Strategy):

    def __init__(
            self,
            user_statistic_repository: UserStatisticRepository,
            customer_repository: CustomerRepository,
            escort_repository: EscortRepository,
            user_activity_repository: UserActivityRepository,
            tracking_repository: TrackingRepository,
            general_statistic_repository: GeneralStatisticRepository,
            top_escort_repository: TopEscortRepository,
            top_place_repository: TopPlaceRepository,
            payment_statistic_repository: PaymentStatisticRepository,
    ):
        self.__user_statistic_repository = user_statistic_repository
        self.__customer_repository = customer_repository
        self.__escort_repository = escort_repository
        self.__user_activity_repository = user_activity_repository
        self.__tracking_repository = tracking_repository
        self.__general_statistic_repository = general_statistic_repository
        self.__top_escort_repository = top_escort_repository
        self.__top_place_repository = top_place_repository
        self.__payment_statistic_repository = payment_statistic_repository

    async def __process_customer_statistic(self, message: dict, today: str) -> None:
        query: dict = {'raw_created_at': today, 'customer_id': ObjectId(message['customerId'])}
        statistic: CustomerStatistic = await self.__user_statistic_repository.get_customer_statistic(query)

        if not statistic:
            new_statistic: dict = {
                'customer_id': message['customerId'],
                'hired_services': 1,
                'spent_money': message['serviceCost'],
                'raw_created_at': today,
            }
            await self.__user_statistic_repository.add_customer_statistic(new_statistic)
            return

        changes: dict = {
            'hired_services': 1 + statistic.hired_services,
            'spent_money': message['serviceCost'] + statistic.spent_money,
        }
        await self.__user_statistic_repository.update_customer_statistic(statistic.id, changes)

    async def __process_escort_statistic(self, message: dict, today: str) -> None:
        query: dict = {'raw_created_at': today, 'escort_id': ObjectId(message['escortId'])}
        statistic: EscortStatistic = await self.__user_statistic_repository.get_escort_statistic(query)

        if not statistic:
            new_statistic: dict = {
                'escort_id': message['escortId'],
                'services_provided': 1,
                'earned_money': message['escortProfit'],
                'raw_created_at': today,
            }
            await self.__user_statistic_repository.add_escort_statistic(new_statistic)
            return

        changes: dict = {
            'services_provided': 1 + statistic.services_provided,
            'earned_money': message['escortProfit'] + statistic.earned_money,
        }
        await self.__user_statistic_repository.update_escort_statistic(statistic.id, changes)

    async def __process_user_activity(self, today: str, customer_services: int, escort_services: int) -> None:
        if not customer_services:
            query: dict = {'raw_created_at': today, 'type': 'Customer'}
            customer_activity: GeneralUserActivity = (
                await self.__user_activity_repository.get_general_user_activity(query)
            )

            if customer_activity:
                changes: dict = {
                    'active': customer_activity.active + 1,
                    'inactive':  customer_activity.inactive - 1,
                }
                await self.__user_activity_repository.update_general_user_activity(customer_activity.id, changes)
            else:
                total_customers: int = await self.__customer_repository.count()
                new_activity: dict = {
                    'active': 1,
                    'inactive': total_customers - 1,
                    'type': 'Customer',
                    'raw_created_at': today,
                }
                await self.__user_activity_repository.add_general_user_activity(new_activity)

        if not escort_services:
            query: dict = {'raw_created_at': today, 'type': 'Escort'}
            escort_activity: GeneralUserActivity = (
                await self.__user_activity_repository.get_general_user_activity(query)
            )

            if escort_activity:
                changes: dict = {
                    'active': escort_activity.active + 1,
                    'inactive': escort_activity.inactive - 1,
                }
                await self.__user_activity_repository.update_general_user_activity(escort_activity.id, changes)
            else:
                total_escorts: int = await self.__escort_repository.count()
                new_activity: dict = {
                    'active': 1,
                    'inactive': total_escorts - 1,
                    'type': 'Escort',
                    'raw_created_at': today,
                }
                await self.__user_activity_repository.add_general_user_activity(new_activity)

    async def __process_state_user_activity(
        self,
        today: str,
        customer_services: int,
        escort_services: int,
        location: Location,
    ) -> None:
        if not customer_services:
            query: dict = {'raw_created_at': today, 'type': 'Customer'}
            customer_activity: StateUserActivity = (
                await self.__user_activity_repository.get_state_user_activity(query)
            )

            if customer_activity:
                changes: dict = {
                    'active': customer_activity.active + 1,
                    'inactive':  customer_activity.inactive - 1,
                }
                await self.__user_activity_repository.update_state_user_activity(customer_activity.id, changes)
            else:
                total_customers: int = await self.__tracking_repository.count_customers_by_city(location.city)
                new_activity: dict = {
                    'active': 1,
                    'inactive': total_customers - 1,
                    'state': location.state,
                    'type': 'Customer',
                    'raw_created_at': today,
                }
                await self.__user_activity_repository.add_state_user_activity(new_activity)

        if not escort_services:
            query: dict = {'raw_created_at': today, 'type': 'Escort'}
            escort_activity: StateUserActivity = await self.__user_activity_repository.get_state_user_activity(query)

            if escort_activity:
                changes: dict = {
                    'active': escort_activity.active + 1,
                    'inactive': escort_activity.inactive - 1,
                }
                await self.__user_activity_repository.update_state_user_activity(escort_activity.id, changes)
            else:
                total_escorts: int = await self.__tracking_repository.count_escorts_by_city(location.city)
                new_activity: dict = {
                    'active': 1,
                    'inactive': total_escorts - 1,
                    'state': location.state,
                    'type': 'Escort',
                    'raw_created_at': today,
                }
                await self.__user_activity_repository.add_state_user_activity(new_activity)

    async def __process_city_user_activity(
        self,
        today: str,
        customer_services: int,
        escort_services: int,
        location: Location,
    ) -> None:
        if not customer_services:
            query: dict = {'raw_created_at': today, 'type': 'Customer'}
            customer_activity: CityUserActivity = await self.__user_activity_repository.get_city_user_activity(query)

            if customer_activity:
                changes: dict = {
                    'active': customer_activity.active + 1,
                    'inactive':  customer_activity.inactive - 1,
                }
                await self.__user_activity_repository.update_city_user_activity(customer_activity.id, changes)
            else:
                total_customers: int = await self.__tracking_repository.count_customers_by_city(location.city)
                new_activity: dict = {
                    'active': 1,
                    'inactive': total_customers - 1,
                    'state': location.state,
                    'city': location.city,
                    'type': 'Customer',
                    'raw_created_at': today,
                }
                await self.__user_activity_repository.add_city_user_activity(new_activity)

        if not escort_services:
            query: dict = {'created_at': today, 'type': 'Escort'}
            escort_activity: CityUserActivity = await self.__user_activity_repository.get_city_user_activity(query)

            if escort_activity:
                changes: dict = {
                    'active': escort_activity.active + 1,
                    'inactive': escort_activity.inactive - 1,
                }
                await self.__user_activity_repository.update_city_user_activity(escort_activity.id, changes)
            else:
                total_escorts: int = await self.__tracking_repository.count_escorts_by_city(location.city)
                new_activity: dict = {
                    'active': 1,
                    'inactive': total_escorts - 1,
                    'state': location.state,
                    'city': location.city,
                    'type': 'Escort',
                }
                await self.__user_activity_repository.add_city_user_activity(new_activity)

    async def __process_earnings(self, message: dict, today: str) -> None:
        query: dict = {'raw_created_at': today}
        statistic: GeneralStatistic = await self.__general_statistic_repository.get_general_statistic(query)

        if not statistic:
            new_statistic: dict = {'earnings': message['businessCommission'], 'raw_created_at': today}
            await self.__general_statistic_repository.add_general_statistic(new_statistic)
            return

        changes: dict = {
            'earnings': message['businessCommission'] + statistic.earnings,
        }
        await self.__general_statistic_repository.update_general_statistic(statistic.id, changes)

    async def __process_state_earnings(self, message: dict, today: str, location: Location) -> None:
        query: dict = {'raw_created_at': today, 'state': location.state}
        statistic: StateStatistic = await self.__general_statistic_repository.get_state_statistic(query)

        if not statistic:
            new_statistic: dict = {
                'earnings': message['businessCommission'],
                'state': location.state,
                'raw_created_at': today,
            }
            await self.__general_statistic_repository.add_state_statistic(new_statistic)
            return

        changes: dict = {
            'earnings': message['businessCommission'] + statistic.earnings,
        }
        await self.__general_statistic_repository.update_state_statistic(statistic.id, changes)

    async def __process_city_earnings(self, message: dict, today: str, location: Location) -> None:
        query: dict = {'raw_created_at': today, 'city': location.city}
        statistic: CityStatistic = await self.__general_statistic_repository.get_city_statistic(query)

        if not statistic:
            new_statistic: dict = {
                'earnings': message['businessCommission'],
                'state': location.state,
                'city': location.city,
                'raw_created_at': today,
            }
            await self.__general_statistic_repository.add_city_statistic(new_statistic)
            return

        changes: dict = {
            'earnings': message['businessCommission'] + statistic.earnings,
        }
        await self.__general_statistic_repository.update_city_statistic(statistic.id, changes)
    
    async def __process_top_escorts(self, message: dict) -> None:
        place: TopGeneralEscort = await self.__top_escort_repository.get_general_place(message['escortId'])

        if not place:
            escort: EscortProfile = await self.__escort_repository.get_by_id(message['escortId'])
            services: int = await self.__user_statistic_repository.sum_services(message['escortId'])
            new_place: dict = {
                'escort_id': escort.escort_id,
                'name': f'{escort.first_name} {escort.last_name}',
            }
            await self.__top_escort_repository.add_general_place(new_place, services)
            return

        new_values: dict = {'services': place.services + 1}
        await self.__top_escort_repository.update_general_place(place.escort_id, new_values)

    async def __process_top_escorts_by_state(self, message: dict, location: Location) -> None:
        place: TopStateEscort = await self.__top_escort_repository.get_state_place(message['escortId'])

        if not place:
            escort: EscortProfile = await self.__escort_repository.get_by_id(message['escortId'])
            services: int = await self.__user_statistic_repository.sum_services(message['escortId'])
            new_place: dict = {
                'escort_id': message['escortId'],
                'name': f'{escort.first_name} {escort.last_name}',
                'state': location.state,
            }
            await self.__top_escort_repository.add_state_place(new_place, services)
            return

        new_values: dict = {'services': place.services + 1}
        await self.__top_escort_repository.update_state_place(place.escort_id, new_values)

    async def __process_top_escort_by_city(self, message: dict, location: Location) -> None:
        place: TopCityEscort = await self.__top_escort_repository.get_city_place(message['escortId'])

        if not place:
            escort: EscortProfile = await self.__escort_repository.get_by_id(message['escortId'])
            services: int = await self.__user_statistic_repository.sum_services(message['escortId'])
            new_place: dict = {
                'escort_id': message['escortId'],
                'name': f'{escort.first_name} {escort.last_name}',
                'state': location.state,
                'city': location.city,
            }
            await self.__top_escort_repository.add_city_place(new_place, services)
            return

        new_values: dict = {'services': place.services + 1}
        await self.__top_escort_repository.update_city_place(place.escort_id, new_values)

    async def __process_top_state(self, location: Location) -> None:
        state: TopState = await self.__top_place_repository.get_state(location.state)

        if not state:
            services: int = await self.__top_escort_repository.count_services_by_state(location.state)
            new_state: dict = {'name': location.state, 'services': services}
            await self.__top_place_repository.add_state(new_state, services)
            return

        changes: dict = {'services': state.services + 1}
        await self.__top_place_repository.update_state(state.id, changes)

    async def __process_top_city(self, location: Location):
        city: TopCity = await self.__top_place_repository.get_city(location.city)

        if not city:
            services: int = await self.__top_escort_repository.count_services_by_city(location.city)
            new_city: dict = {'name': location.city, 'services': services, 'state': location.state}
            await self.__top_place_repository.add_city(new_city, services)
            return

        changes: dict = {'services': city.services + 1}
        await self.__top_place_repository.update_city(city.id, changes)

    async def __process_payment(self, today: str, payments: list[str]) -> None:
        query: dict = {'raw_created_at': today, 'name': {'$in': payments}}
        find_payments: list[PaymentStatistic] = (
            await self.__payment_statistic_repository.get_payment_statistic(query)
        )

        if not find_payments:
            tasks: list = [
                self.__payment_statistic_repository.add_payment_statistic({
                    'name': payment,
                    'raw_created_at': today,
                })
                for payment in payments
            ]
            await asyncio.gather(*tasks)
            return

        payment_names: list[str] = [payment.name for payment in find_payments]
        missing_payments: list[str] = list(set(payment_names) - set(payments))

        tasks: list = [
            self.__payment_statistic_repository.add_payment_statistic({
                'name': payment,
                'raw_created_at': today,
            })
            for payment in missing_payments
        ]
        await asyncio.gather(*tasks)

        tasks: list = [
            self.__payment_statistic_repository.update_payment_statistic(payment.id, {
                'services': payment.services + 1,
            })
            for payment in find_payments
        ]
        await asyncio.gather(*tasks)

    async def __process_state_payment(self, today: str, payments: list[str], location: Location) -> None:
        query: dict = {'raw_created_at': today, 'name': {'$in': payments}, 'state': location.state}
        find_payments: list[PaymentStateStatistic] = (
            await self.__payment_statistic_repository.get_state_payment_statistic(query)
        )

        if not find_payments:
            tasks: list = [
                self.__payment_statistic_repository.add_state_payment_statistic({
                    'name': payment,
                    'raw_created_at': today,
                    'state': location.state,
                })
                for payment in payments
            ]
            await asyncio.gather(*tasks)
            return

        payment_name: list[str] = [payment.name for payment in find_payments]
        missing_payments: list[str] = list(set(payment_name) - set(payments))

        tasks: list = [
            self.__payment_statistic_repository.add_state_payment_statistic({
                'name': payment,
                'raw_created_at': today,
                'state': location.state,
            })
            for payment in missing_payments
        ]
        await asyncio.gather(*tasks)

        tasks: list = [
            self.__payment_statistic_repository.update_state_payment_statistic(payment.id, {
                'services': payment.services + 1,
            })
            for payment in find_payments
        ]
        await asyncio.gather(*tasks)

    async def __process_city_payment(self, today, payments: list[str], location: Location) -> None:
        query: dict = {'raw_created_at': today, 'name': {'$in': payments}, 'city': location.city}
        find_payments: list[PaymentCityStatistic] = (
            await self.__payment_statistic_repository.get_city_payment_statistic(query)
        )

        if not find_payments:
            tasks: list = [
                self.__payment_statistic_repository.add_city_payment_statistic({
                    'name': payment,
                    'raw_created_at': today,
                    'state': location.state,
                    'city': location.city,
                })
                for payment in payments
            ]
            await asyncio.gather(*tasks)
            return

        payment_names: list[str] = [payment.name for payment in find_payments]
        missing_payments: list[str] = list(set(payment_names) - set(payments))

        tasks: list = [
            self.__payment_statistic_repository.add_city_payment_statistic({
                'name': payment,
                'raw_created_at': today,
                'state': location.state,
                'city': location.city,
            })
            for payment in missing_payments
        ]
        await asyncio.gather(*tasks)

        tasks: list = [
            self.__payment_statistic_repository.update_city_payment_statistic(payment.id, {
                'services': payment.services + 1,
            })
            for payment in find_payments
        ]
        await asyncio.gather(*tasks)

    async def process_message(self, message: dict) -> None:
        today: str = date.today().strftime('%Y-%m-%d')

        customer_query: dict = {'raw_created_at': today, 'customer_id': ObjectId(message['customerId'])}
        escort_query: dict = {'raw_created_at': today, 'escort_id': ObjectId(message['escortId'])}

        tasks: list = [
            self.__user_statistic_repository.count_customer_statistic(customer_query),
            self.__user_statistic_repository.count_escort_statistic(escort_query),
            self.__tracking_repository.get_escort_location(message['escortId']),
        ]
        [customer_services, escort_services, location] = await asyncio.gather(*tasks)

        await self.__process_user_activity(today, customer_services, escort_services)
        await self.__process_state_user_activity(today, customer_services, escort_services, location)
        await self.__process_city_user_activity(today, customer_services, escort_services, location)

        await self.__process_earnings(message, today)
        await self.__process_state_earnings(message, today, location)
        await self.__process_city_earnings(message, today, location)

        await self.__process_top_state(location)
        await self.__process_top_city(location)

        await self.__process_top_escort_by_city(message, location)
        await self.__process_top_escorts_by_state(message, location)
        await self.__process_top_escorts(message)

        await self.__process_customer_statistic(message, today)
        await self.__process_escort_statistic(message, today)
        
        await self.__process_payment(today, message['paymentMethods'])
        await self.__process_state_payment(today, message['paymentMethods'], location)
        await self.__process_city_payment(today, message['paymentMethods'], location)
