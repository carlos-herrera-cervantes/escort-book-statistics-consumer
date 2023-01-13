from unittest.mock import Mock
from unittest import IsolatedAsyncioTestCase, main
from datetime import datetime

from services.strategies.payment_service import PaymentService
from models.location import Location
from models.escort_profile import EscortProfile
from models.user_statistic import CustomerStatistic, EscortStatistic
from models.user_activity import GeneralUserActivity, StateUserActivity, CityUserActivity
from models.general_statistic import GeneralStatistic, StateStatistic, CityStatistic
from models.top_escort import TopGeneralEscort, TopStateEscort, TopCityEscort
from models.top_place import TopState, TopCity
from models.payment_statistic import PaymentStatistic, PaymentStateStatistic, PaymentCityStatistic


class PaymentServiceTests(IsolatedAsyncioTestCase):

    async def test_process_message_should_add_statistic(self) -> None:
        mock_user_statistic_repository = Mock()
        mock_customer_repository = Mock()
        mock_escort_repository = Mock()
        mock_user_activity_repository = Mock()
        mock_tracking_repository = Mock()
        mock_general_statistic_repository = Mock()
        mock_top_escort_repository = Mock()
        mock_top_place_repository = Mock()
        mock_payment_statistic_repository = Mock()

        payment_service = PaymentService(
            mock_user_statistic_repository,
            mock_customer_repository,
            mock_escort_repository,
            mock_user_activity_repository,
            mock_tracking_repository,
            mock_general_statistic_repository,
            mock_top_escort_repository,
            mock_top_place_repository,
            mock_payment_statistic_repository
        )

        mock_user_statistic_repository.count_customer_statistic.return_value = 0
        mock_user_statistic_repository.count_escort_statistic.return_value = 0

        location = Location()
        location.state = 'guerrero'
        location.city = 'acapulco'
        location.country = 'MX'
        mock_tracking_repository.get_escort_location.return_value = location

        mock_user_statistic_repository.get_customer_statistic.return_value = None
        mock_user_statistic_repository.get_escort_statistic.return_value = None
        mock_customer_repository.count.return_value = 0
        mock_user_activity_repository.get_general_user_activity.return_value = None
        mock_escort_repository.count.return_value = 0
        mock_user_activity_repository.get_state_user_activity.return_value = None
        mock_tracking_repository.count_customers_by_city.return_value = 0
        mock_user_activity_repository.get_city_user_activity.return_value = None
        mock_tracking_repository.count_escorts_by_city.return_value = 0
        mock_general_statistic_repository.get_general_statistic.return_value = None
        mock_general_statistic_repository.get_state_statistic.return_value = None
        mock_general_statistic_repository.get_city_statistic.return_value = None
        mock_top_escort_repository.get_general_place.return_value = None

        escort_profile = EscortProfile()
        escort_profile.escort_id = '63bcf85a1ad98e1ef77a908c'
        escort_profile.first_name = 'Liz'
        escort_profile.last_name = 'Salado'
        mock_escort_repository.get_by_id.return_value = escort_profile

        mock_user_statistic_repository.sum_services.return_value = 0
        mock_top_escort_repository.get_state_place.return_value = None
        mock_top_escort_repository.get_city_place.return_value = None
        mock_top_place_repository.get_state.return_value = None
        mock_top_escort_repository.count_services_by_state.return_value = 0
        mock_top_place_repository.get_city.return_value = None
        mock_top_escort_repository.count_services_by_city.return_value = 0
        mock_payment_statistic_repository.get_payment_statistic.return_value = []
        mock_payment_statistic_repository.get_state_payment_statistic.return_value = []
        mock_payment_statistic_repository.get_city_payment_statistic.return_value = []

        message = {
            'customerId': '63bcdbf4ab73bec39946dbec',
            'escortId': '63bcdc096517542f46651fd0',
            'serviceCost': 880,
            'escortProfit': 800,
            'businessCommission': 80,
            'paymentMethods': ['cash'],
        }
        await payment_service.process_message(message)

        mock_user_statistic_repository.count_customer_statistic.assert_called()
        mock_user_statistic_repository.count_escort_statistic.assert_called()
        mock_user_statistic_repository.get_customer_statistic.assert_called()
        mock_user_statistic_repository.add_customer_statistic.assert_called()
        mock_user_statistic_repository.get_escort_statistic.assert_called()
        mock_user_statistic_repository.add_escort_statistic.assert_called()
        mock_customer_repository.count.assert_called()
        mock_user_activity_repository.get_general_user_activity.assert_called()
        mock_escort_repository.count.assert_called()
        mock_user_activity_repository.add_general_user_activity.assert_called()
        mock_user_activity_repository.get_state_user_activity.assert_called()
        mock_tracking_repository.count_customers_by_city.assert_called()
        mock_user_activity_repository.add_state_user_activity.assert_called()
        mock_user_activity_repository.get_city_user_activity.asser_called()
        mock_user_activity_repository.add_city_user_activity.assert_called()
        mock_tracking_repository.count_escorts_by_city.assert_called()
        mock_general_statistic_repository.get_general_statistic.assert_called()
        mock_general_statistic_repository.add_general_statistic.assert_called()
        mock_general_statistic_repository.get_state_statistic.assert_called()
        mock_general_statistic_repository.add_state_statistic.assert_called()
        mock_general_statistic_repository.get_city_statistic.assert_called()
        mock_general_statistic_repository.add_city_statistic.assert_called()
        mock_top_escort_repository.get_general_place.assert_called()
        mock_escort_repository.get_by_id.assert_called()
        mock_user_statistic_repository.sum_services.assert_called()
        mock_top_escort_repository.add_general_place.assert_called()
        mock_top_escort_repository.get_state_place.assert_called()
        mock_top_escort_repository.add_state_place.assert_called()
        mock_top_escort_repository.get_city_place.assert_called()
        mock_top_escort_repository.add_city_place.assert_called()
        mock_top_place_repository.get_state.assert_called()
        mock_top_escort_repository.count_services_by_state.assert_called()
        mock_top_place_repository.add_state.assert_called()
        mock_top_place_repository.get_city.assert_called()
        mock_top_escort_repository.count_services_by_city.assert_called()
        mock_top_place_repository.add_city.assert_called()
        mock_payment_statistic_repository.get_payment_statistic.assert_called()
        mock_payment_statistic_repository.add_payment_statistic.assert_called()
        mock_payment_statistic_repository.get_state_payment_statistic.assert_called()
        mock_payment_statistic_repository.add_state_payment_statistic.assert_called()
        mock_payment_statistic_repository.get_city_payment_statistic.assert_called()
        mock_payment_statistic_repository.add_city_payment_statistic.assert_called()

    async def test_process_message_should_update_statistic(self) -> None:
        mock_user_statistic_repository = Mock()
        mock_customer_repository = Mock()
        mock_escort_repository = Mock()
        mock_user_activity_repository = Mock()
        mock_tracking_repository = Mock()
        mock_general_statistic_repository = Mock()
        mock_top_escort_repository = Mock()
        mock_top_place_repository = Mock()
        mock_payment_statistic_repository = Mock()

        payment_service = PaymentService(
            mock_user_statistic_repository,
            mock_customer_repository,
            mock_escort_repository,
            mock_user_activity_repository,
            mock_tracking_repository,
            mock_general_statistic_repository,
            mock_top_escort_repository,
            mock_top_place_repository,
            mock_payment_statistic_repository
        )

        mock_user_statistic_repository.count_customer_statistic.return_value = 0
        mock_user_statistic_repository.count_escort_statistic.return_value = 0

        location = Location()
        location.state = 'guerrero'
        location.city = 'acapulco'
        location.country = 'MX'
        mock_tracking_repository.get_escort_location.return_value = location

        customer_statistic = CustomerStatistic()
        customer_statistic.customer_id = '63bf98639449e47a370a530e'
        customer_statistic.hired_services = 1
        customer_statistic.spent_money = 880
        customer_statistic.raw_created_at = '2023-01-01'
        customer_statistic.created_at = datetime.now()
        customer_statistic.emitted_claims = 0
        customer_statistic.received_claims = 0
        mock_user_statistic_repository.get_customer_statistic.return_value = customer_statistic

        escort_statistic = EscortStatistic()
        escort_statistic.escort_id = '63bf99d5a1ad2aa56ca68e43'
        escort_statistic.services_provided = 1
        escort_statistic.earned_money = 800
        escort_statistic.raw_created_at = '2023-01-01'
        escort_statistic.created_at = datetime.now()
        escort_statistic.emitted_claims = 0
        escort_statistic.received_claims = 0
        mock_user_statistic_repository.get_escort_statistic.return_value = escort_statistic

        general_user_activity = GeneralUserActivity()
        general_user_activity.active = 10
        general_user_activity.inactive = 5
        general_user_activity.type = 'dummy'
        general_user_activity.raw_created_at = '2023-01-01'
        general_user_activity.created_at = datetime.now()
        mock_user_activity_repository.get_general_user_activity.return_value = general_user_activity

        state_user_activity = StateUserActivity()
        state_user_activity.active = 10
        state_user_activity.inactive = 5
        state_user_activity.type = 'dummy'
        state_user_activity.state = 'guerrero'
        state_user_activity.raw_created_at = '2023-01-01'
        state_user_activity.created_at = datetime.now()
        mock_user_activity_repository.get_state_user_activity.return_value = state_user_activity

        city_user_activity = CityUserActivity()
        city_user_activity.active = 10
        city_user_activity.inactive = 5
        city_user_activity.type = 'dummy'
        city_user_activity.city = 'acapulco'
        city_user_activity.state = 'guerrero'
        city_user_activity.raw_created_at = '2023-01-01'
        city_user_activity.created_at = datetime.now()
        mock_user_activity_repository.get_city_user_activity.return_value = city_user_activity

        general_statistic = GeneralStatistic()
        general_statistic.total_customers = 0
        general_statistic.total_customers = 0
        general_statistic.earnings = 0
        general_statistic.raw_created_at = '2023-01-01'
        general_statistic.claims = 0
        general_statistic.created_at = datetime.now()
        mock_general_statistic_repository.get_general_statistic.return_value = general_statistic

        state_statisic = StateStatistic()
        state_statisic.total_customers = 0
        state_statisic.total_customers = 0
        state_statisic.earnings = 0
        state_statisic.state = 'guerrero'
        state_statisic.raw_created_at = '2023-01-01'
        state_statisic.claims = 0
        state_statisic.created_at = datetime.now()
        mock_general_statistic_repository.get_state_statistic.return_value = state_statisic

        city_statistic = CityStatistic()
        city_statistic.total_customers = 0
        city_statistic.total_customers = 0
        city_statistic.earnings = 0
        city_statistic.city = 'acapulco'
        city_statistic.state = 'guerrero'
        city_statistic.raw_created_at = '2023-01-01'
        city_statistic.claims = 0
        city_statistic.created_at = datetime.now()
        mock_general_statistic_repository.get_city_statistic.return_value = city_statistic

        top_general_escort = TopGeneralEscort()
        top_general_escort.escort_id = '63c0ca5bfb799d787493f6a1'
        top_general_escort.name = 'Dummy Escort'
        top_general_escort.services = 0
        top_general_escort.created_at = datetime.now()
        mock_top_escort_repository.get_general_place.return_value = top_general_escort

        top_state_escort = TopStateEscort()
        top_state_escort.escort_id = '63c0ca5bfb799d787493f6a1'
        top_state_escort.name = 'Dummy Escort'
        top_state_escort.state = 'guerrero'
        top_state_escort.services = 0
        top_state_escort.created_at = datetime.now()
        mock_top_escort_repository.get_state_place.return_value = top_state_escort

        top_city_escort = TopCityEscort()
        top_city_escort.escort_id = '63c0ca5bfb799d787493f6a1'
        top_city_escort.name = 'Dummy Escort'
        top_city_escort.city = 'acapulco'
        top_city_escort.state = 'guerrero'
        top_city_escort.services = 0
        top_city_escort.created_at = datetime.now()
        mock_top_escort_repository.get_city_place.return_value = top_city_escort

        top_state = TopState()
        top_state.name = 'guerrero'
        top_state.services = 0
        top_state.created_at = datetime.now()
        mock_top_place_repository.get_state.return_value = top_state

        top_city = TopCity()
        top_city.name = 'acapulco'
        top_city.state = 'guerrero'
        top_city.services = 0
        top_city.created_at = datetime.now()
        mock_top_place_repository.get_city.return_value = top_city

        payment_statistic = PaymentStatistic()
        payment_statistic.name = 'cash'
        payment_statistic.services = 1
        payment_statistic.raw_created_at = '2023-01-01'
        payment_statistic.created_at = datetime.now()
        mock_payment_statistic_repository.get_payment_statistic.return_value = [payment_statistic]

        payment_state_statistic = PaymentStateStatistic()
        payment_state_statistic.name = 'cash'
        payment_state_statistic.services = 1
        payment_state_statistic.state = 'guerrero'
        payment_state_statistic.raw_created_at = '2023-01-01'
        payment_state_statistic.created_at = datetime.now()
        mock_payment_statistic_repository.get_state_payment_statistic.return_value = [payment_state_statistic]

        payment_city_statistic = PaymentCityStatistic()
        payment_city_statistic.name = 'cash'
        payment_city_statistic.services = 1
        payment_city_statistic.city = 'acapulco'
        payment_city_statistic.state = 'guerrero'
        payment_city_statistic.raw_created_at = '2023-01-01'
        payment_city_statistic.created_at = datetime.now()
        mock_payment_statistic_repository.get_city_payment_statistic.return_value = [payment_city_statistic]

        message = {
            'customerId': '63bcdbf4ab73bec39946dbec',
            'escortId': '63bcdc096517542f46651fd0',
            'serviceCost': 880,
            'escortProfit': 800,
            'businessCommission': 80,
            'paymentMethods': ['cash'],
        }
        await payment_service.process_message(message)

        mock_user_statistic_repository.get_customer_statistic.assert_called()
        mock_user_statistic_repository.update_customer_statistic.assert_called()
        mock_user_statistic_repository.get_escort_statistic.assert_called()
        mock_user_statistic_repository.update_escort_statistic.assert_called()
        mock_user_activity_repository.get_general_user_activity.assert_called()
        mock_user_activity_repository.update_general_user_activity.assert_called()
        mock_user_activity_repository.get_state_user_activity.assert_called()
        mock_user_activity_repository.update_state_user_activity.assert_called()
        mock_user_activity_repository.get_city_user_activity.assert_called()
        mock_user_activity_repository.update_city_user_activity.assert_called()
        mock_general_statistic_repository.get_general_statistic.assert_called()
        mock_general_statistic_repository.update_general_statistic.assert_called()
        mock_general_statistic_repository.get_state_statistic.assert_called()
        mock_general_statistic_repository.update_state_statistic.assert_called()
        mock_general_statistic_repository.get_city_statistic.assert_called()
        mock_general_statistic_repository.update_city_statistic.assert_called()
        mock_top_escort_repository.get_general_place.assert_called()
        mock_top_escort_repository.update_general_place.assert_called()
        mock_top_escort_repository.get_state_place.assert_called()
        mock_top_escort_repository.update_state_place.assert_called()
        mock_top_escort_repository.get_city_place.assert_called()
        mock_top_escort_repository.update_city_place.assert_called()
        mock_top_place_repository.get_state.assert_called()
        mock_top_place_repository.update_state.assert_called()
        mock_top_place_repository.get_city.assert_called()
        mock_top_place_repository.update_city.assert_called()
        mock_payment_statistic_repository.get_payment_statistic.assert_called()
        mock_payment_statistic_repository.update_payment_statistic.assert_called()
        mock_payment_statistic_repository.get_state_payment_statistic.assert_called()
        mock_payment_statistic_repository.update_state_payment_statistic.assert_called()
        mock_payment_statistic_repository.get_city_payment_statistic.assert_called()
        mock_payment_statistic_repository.update_city_payment_statistic.assert_called()

if __name__ == '__main__':
    main()
