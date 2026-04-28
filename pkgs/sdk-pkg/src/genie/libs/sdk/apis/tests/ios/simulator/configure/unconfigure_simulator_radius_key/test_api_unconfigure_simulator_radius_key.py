from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.ios.simulator.configure import unconfigure_simulator_radius_key


class TestUnconfigureSimulatorRadiusKey(TestCase):

    def test_unconfigure_simulator_radius_key(self):
        self.device = Mock()
        unconfigure_simulator_radius_key(self.device, 'radkey123')
        self.device.configure.assert_called_once_with(
            "no simulator radius key radkey123"
        )
