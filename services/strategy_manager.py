from services.strategies.general_statistic_service import GeneralStatisticService
from services.strategies.payment_service import PaymentService
from services.interfaces.strategy_interface import Strategy
from config.db import MongoClient, PostgresClient
from repositories.tracking_repository import TrackingRepository
from repositories.general_statistic_repository import GeneralStatisticRepository
from repositories.user_statistic_repository import UserStatisticRepository
from repositories.customer_repository import CustomerRepository
from repositories.escort_repository import EscortRepository
from repositories.user_activity_repository import UserActivityRepository
from repositories.top_escort_repository import TopEscortRepository
from repositories.top_place_repository import TopPlaceRepository
from repositories.payment_statistic_repository import PaymentStatisticRepository


class StrategyManager:

    def __init__(self, operation: str) -> None:
        MongoClient().connect()
        postgres_clients: dict = PostgresClient().connect()

        self.__strategies: dict = {
            'new-user': GeneralStatisticService(
                GeneralStatisticRepository(),
                TrackingRepository(postgres_clients['tracking_db']),
            ),
            'service-paid': PaymentService(
                UserStatisticRepository(),
                CustomerRepository(postgres_clients['customer_db']),
                EscortRepository(postgres_clients['escort_db']),
                UserActivityRepository(),
                TrackingRepository(postgres_clients['tracking_db']),
                GeneralStatisticRepository(),
                TopEscortRepository(),
                TopPlaceRepository(),
                PaymentStatisticRepository(),
            )
        }
        self.__operation: str = operation

    async def process_message(self, message: dict) -> None:
        strategy: Strategy = self.__strategies.get(self.__operation)

        if not strategy:
            return

        await strategy.process_message(message)


def initialize_manager(operation: str) -> StrategyManager:
    return StrategyManager(operation)
