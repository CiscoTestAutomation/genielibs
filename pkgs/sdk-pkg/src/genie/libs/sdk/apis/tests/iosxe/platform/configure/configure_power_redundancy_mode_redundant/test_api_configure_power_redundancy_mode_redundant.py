from unittest import TestCase
from genie.libs.sdk.apis.iosxe.platform.configure import configure_power_redundancy_mode_redundant
from unittest.mock import Mock


class TestConfigurePowerRedundancyModeRedundant(TestCase):

    def test_configure_power_redundancy_mode_redundant(self):
        self.device = Mock()
        result = configure_power_redundancy_mode_redundant(self.device, 'N+N', '1 2 3 4')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('power redundancy-mode redundant N+N 1 2 3 4',)
        )
