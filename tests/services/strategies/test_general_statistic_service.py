from unittest.mock import Mock
from unittest import IsolatedAsyncioTestCase, main
from datetime import datetime

from services.strategies.general_statistic_service import GeneralStatisticService
from models.location import Location
from models.general_statistic import GeneralStatistic, StateStatistic, CityStatistic


class GeneralStatisticServiceTests(IsolatedAsyncioTestCase):

    async def test_process_message_should_add_statistic(self) -> None:
        mock_general_statistic_repository = Mock()
        mock_tracking_repository = Mock()

        general_statistic_service = GeneralStatisticService(
            mock_general_statistic_repository,
            mock_tracking_repository
        )

        location = Location()
        location.state = 'guerrero'
        location.city = 'acapulco'
        location.country = 'MX'

        mock_tracking_repository.get_escort_location.return_value = location
        mock_general_statistic_repository.get_general_statistic.return_value = None
        mock_general_statistic_repository.get_state_statistic.return_value = None
        mock_general_statistic_repository.get_city_statistic.return_value = None

        message = {
            'userId': '63bb8b99c4d7402205f931bb',
            'userType': 'Escort'
        }
        await general_statistic_service.process_message(message)

        mock_tracking_repository.get_escort_location.assert_called_once()
        mock_general_statistic_repository.get_general_statistic.assert_called_once()
        mock_general_statistic_repository.add_general_statistic.assert_called_once()
        mock_general_statistic_repository.get_state_statistic.assert_called_once()
        mock_general_statistic_repository.add_state_statistic.assert_called_once()
        mock_general_statistic_repository.get_city_statistic.assert_called_once()
        mock_general_statistic_repository.add_city_statistic.assert_called_once()

    async def test_process_message_should_update_statistic(self) -> None:
        mock_general_statistic_repository = Mock()
        mock_tracking_repository = Mock()

        general_statistic_service = GeneralStatisticService(
            mock_general_statistic_repository,
            mock_tracking_repository
        )

        location = Location()
        location.state = 'guerrero'
        location.city = 'acapulco'
        location.country = 'MX'
        mock_tracking_repository.get_customer_location.return_value = location

        general_statistic = GeneralStatistic()
        general_statistic.total_customers = 10
        general_statistic.total_escorts = 2
        general_statistic.earnings = 1200
        general_statistic.raw_created_at = '2023-01-01'
        general_statistic.claims = 0
        general_statistic.created_at = datetime.now()
        mock_general_statistic_repository.get_general_statistic.return_value = general_statistic

        state_statistic = StateStatistic()
        state_statistic.total_customers = 10
        state_statistic.total_escorts = 2
        state_statistic.earnings = 1200
        state_statistic.state = 'guerrero'
        state_statistic.raw_created_at = '2023-01-01'
        state_statistic.claims = 0
        state_statistic.created_at = datetime.now()
        mock_general_statistic_repository.get_state_statistic.return_value = state_statistic

        city_statistic = CityStatistic()
        city_statistic.total_customers = 10
        city_statistic.total_escorts = 2
        city_statistic.earnings = 1200
        city_statistic.city = 'acapulco'
        city_statistic.state = 'guerrero'
        city_statistic.raw_created_at = '2023-01-01'
        city_statistic.claims = 0
        city_statistic.created_at = datetime.now()
        mock_general_statistic_repository.get_city_statistic.return_value = city_statistic

        message = {
            'userId': '63bb8b99c4d7402205f931bb',
            'userType': 'Customer'
        }
        await general_statistic_service.process_message(message)

        mock_tracking_repository.get_customer_location.assert_called_once()
        mock_general_statistic_repository.get_general_statistic.assert_called_once()
        mock_general_statistic_repository.update_general_statistic.assert_called_once()
        mock_general_statistic_repository.get_state_statistic.assert_called_once()
        mock_general_statistic_repository.update_state_statistic.assert_called_once()
        mock_general_statistic_repository.get_city_statistic.assert_called_once()
        mock_general_statistic_repository.update_city_statistic.assert_called_once()

if __name__ == '__main__':
    main()
