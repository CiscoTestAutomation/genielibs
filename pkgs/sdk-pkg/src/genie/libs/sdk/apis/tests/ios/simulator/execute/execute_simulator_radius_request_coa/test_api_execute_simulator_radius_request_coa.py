from unittest import TestCase
from unittest.mock import Mock
from unicon.core.errors import SubCommandFailure
from genie.libs.sdk.apis.ios.simulator.execute import execute_simulator_radius_request_coa


class TestExecuteSimulatorRadiusRequestCoa(TestCase):

    def test_execute_simulator_radius_request_coa_basic(self):
        self.device = Mock()
        execute_simulator_radius_request_coa(self.device, 10)
        self.device.execute.assert_called_once_with(
            "simulator radius request 1 coa 10"
        )

    def test_execute_simulator_radius_request_coa_with_client_host(self):
        self.device = Mock()
        execute_simulator_radius_request_coa(
            self.device, 10, client_ip='10.0.0.1', host_ip='10.0.0.2'
        )
        self.device.execute.assert_called_once_with(
            "simulator radius request 1 coa 10 client 10.0.0.1 host 10.0.0.2"
        )

    def test_execute_simulator_radius_request_coa_failure(self):
        self.device = Mock()
        self.device.execute.side_effect = SubCommandFailure('error')
        with self.assertRaises(SubCommandFailure):
            execute_simulator_radius_request_coa(self.device, 10)
