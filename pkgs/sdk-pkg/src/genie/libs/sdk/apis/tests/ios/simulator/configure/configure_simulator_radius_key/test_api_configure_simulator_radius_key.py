from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.ios.simulator.configure import configure_simulator_radius_key


class TestConfigureSimulatorRadiusKey(TestCase):

    def test_configure_simulator_radius_key(self):
        self.device = Mock()
        configure_simulator_radius_key(self.device, 'radkey123')
        self.device.configure.assert_called_once_with(
            "simulator radius key radkey123"
        )
