from unittest import TestCase
from unittest.mock import Mock
from unicon.core.errors import SubCommandFailure
from genie.libs.sdk.apis.ios.simulator.configure import unconfigure_service_simulator_radius_server


class TestUnconfigureServiceSimulatorRadiusServer(TestCase):

    def test_unconfigure_service_simulator_radius_server(self):
        self.device = Mock()
        unconfigure_service_simulator_radius_server(self.device)
        self.device.configure.assert_called_once_with(
            "no service simulator radius server"
        )

    def test_unconfigure_service_simulator_radius_server_failure(self):
        self.device = Mock()
        self.device.configure.side_effect = SubCommandFailure('error')
        with self.assertRaises(SubCommandFailure):
            unconfigure_service_simulator_radius_server(self.device)
