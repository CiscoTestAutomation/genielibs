from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.ios.simulator.configure import unconfigure_simulator_radius_subscriber


class TestUnconfigureSimulatorRadiusSubscriber(TestCase):

    def test_unconfigure_simulator_radius_subscriber(self):
        self.device = Mock()
        unconfigure_simulator_radius_subscriber(self.device, 8)
        self.device.configure.assert_called_once_with(
            "no simulator radius subscriber 8"
        )
