from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.ios.simulator.configure import unconfigure_simulator_radius_server


class TestUnconfigureSimulatorRadiusServer(TestCase):

    def test_unconfigure_simulator_radius_server(self):
        self.device = Mock()
        unconfigure_simulator_radius_server(self.device, '10.1.1.1')
        self.device.configure.assert_called_once_with(
            "no simulator radius server 10.1.1.1"
        )
