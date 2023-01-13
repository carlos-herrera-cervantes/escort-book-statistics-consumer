from unittest.mock import Mock
from unittest import IsolatedAsyncioTestCase, main
from datetime import datetime

from services.strategies.claim_service import ClaimService
from models.location import Location
from models.general_statistic import GeneralStatistic, StateStatistic, CityStatistic
from models.user_statistic import CustomerStatistic, EscortStatistic


class ClaimServiceTests(IsolatedAsyncioTestCase):

    async def test_process_message_should_add_statistic(self) -> None:
        mock_general_statistic_repository = Mock()
        mock_user_statistic_repository =  Mock()
        mock_tracking_repository = Mock()

        claimService = ClaimService(
            mock_general_statistic_repository,
            mock_user_statistic_repository,
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
        mock_user_statistic_repository.get_customer_statistic.return_value = None
        mock_user_statistic_repository.get_escort_statistic.return_value = None

        message = {
            'escortId': '63bb21aa51dced513f4910e1',
            'customerId': '63bb21c6e7e0729ee3d2f09b',
            'to': 'Customer',
        }
        await claimService.process_message(message)

        mock_tracking_repository.get_escort_location.assert_called_once()
        mock_general_statistic_repository.get_general_statistic.assert_called_once()
        mock_general_statistic_repository.add_general_statistic.assert_called_once()
        mock_general_statistic_repository.add_state_statistic.assert_called_once()
        mock_general_statistic_repository.add_city_statistic.assert_called_once()
        mock_user_statistic_repository.add_customer_statistic.assert_called_once()
        mock_user_statistic_repository.add_escort_statistic.assert_called_once()

    async def test_process_message_should_update_statistic(self) -> None:
        mock_general_statistic_repository = Mock()
        mock_user_statistic_repository =  Mock()
        mock_tracking_repository = Mock()

        claimService = ClaimService(
            mock_general_statistic_repository,
            mock_user_statistic_repository,
            mock_tracking_repository
        )

        location = Location()
        location.state = 'guerrero'
        location.city = 'acapulco'
        location.country = 'MX'
        mock_tracking_repository.get_escort_location.return_value = location

        general_statistic = GeneralStatistic()
        general_statistic.total_customers = 10
        general_statistic.total_escorts = 20
        general_statistic.earnings = 1200
        general_statistic.raw_created_at = '2023-01-01'
        general_statistic.claims = 0
        general_statistic.created_at = datetime.now()
        mock_general_statistic_repository.get_general_statistic.return_value = general_statistic

        state_statistic = StateStatistic()
        state_statistic.total_customers = 10
        state_statistic.total_escorts = 20
        state_statistic.earnings = 1200
        state_statistic.state = 'guerrero'
        state_statistic.raw_created_at = '2023-01-01'
        state_statistic.claims = 0
        state_statistic.created_at = datetime.now()
        mock_general_statistic_repository.get_state_statistic.return_value = state_statistic

        city_statistic = CityStatistic()
        city_statistic.total_customers = 10
        city_statistic.total_escorts = 20
        city_statistic.earnings = 1200
        city_statistic.city = 'acapulco'
        city_statistic.state = 'guerrero'
        city_statistic.raw_created_at = '2023-01-01'
        city_statistic.claims = 0
        city_statistic.created_at = datetime.now()
        mock_general_statistic_repository.get_city_statistic.return_value = city_statistic

        customer_statistic = CustomerStatistic()
        customer_statistic.customer_id = '63bb6200c03588b7bda7adf2'
        customer_statistic.hired_services = 2
        customer_statistic.spent_money = 1400
        customer_statistic.raw_created_at = '2023-01-01'
        customer_statistic.created_at = datetime.now()
        customer_statistic.emitted_claims = 0
        customer_statistic.received_claims = 0
        mock_user_statistic_repository.get_customer_statistic.return_value = customer_statistic

        escort_statistic = EscortStatistic()
        escort_statistic.escort_id = '63bb6b31dbdf355e91cc6c05'
        escort_statistic.services_provided = 10
        escort_statistic.earned_money = 2000
        escort_statistic.raw_created_at = '2023-01-01'
        escort_statistic.created_at = datetime.now()
        escort_statistic.emitted_claims = 0
        escort_statistic.received_claims = 0
        mock_user_statistic_repository.get_escort_statistic.return_value = escort_statistic

        message = {
            'escortId': '63bb21aa51dced513f4910e1',
            'customerId': '63bb21c6e7e0729ee3d2f09b',
            'to': 'Customer',
        }
        await claimService.process_message(message)

        mock_tracking_repository.get_escort_location.assert_called_once()
        mock_general_statistic_repository.get_general_statistic.assert_called_once()
        mock_general_statistic_repository.update_general_statistic.assert_called_once()
        mock_general_statistic_repository.get_state_statistic.assert_called_once()
        mock_general_statistic_repository.update_state_statistic.assert_called_once()
        mock_general_statistic_repository.get_city_statistic.assert_called_once()
        mock_general_statistic_repository.update_city_statistic.assert_called_once()
        mock_user_statistic_repository.get_customer_statistic.assert_called_once()
        mock_user_statistic_repository.update_customer_statistic.assert_called_once()
        mock_user_statistic_repository.get_escort_statistic.assert_called_once()
        mock_user_statistic_repository.update_escort_statistic.assert_called_once()

if __name__ == '__main__':
    main()
