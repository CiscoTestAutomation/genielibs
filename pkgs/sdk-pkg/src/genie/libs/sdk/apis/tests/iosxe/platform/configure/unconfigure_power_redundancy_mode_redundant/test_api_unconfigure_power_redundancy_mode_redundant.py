from unittest import TestCase
from genie.libs.sdk.apis.iosxe.platform.configure import unconfigure_power_redundancy_mode_redundant
from unittest.mock import Mock


class TestUnconfigurePowerRedundancyModeRedundant(TestCase):

    def test_unconfigure_power_redundancy_mode_redundant(self):
        self.device = Mock()
        result = unconfigure_power_redundancy_mode_redundant(self.device, 'N+N', '1 2 3 4')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no power redundancy-mode redundant N+N 1 2 3 4',)
        )
