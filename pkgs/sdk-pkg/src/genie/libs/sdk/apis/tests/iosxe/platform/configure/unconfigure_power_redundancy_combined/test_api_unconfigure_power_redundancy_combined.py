from unittest import TestCase
from genie.libs.sdk.apis.iosxe.platform.configure import unconfigure_power_redundancy_combined
from unittest.mock import Mock


class TestUnconfigurePowerRedundancyCombined(TestCase):

    def test_unconfigure_power_redundancy_combined(self):
        self.device = Mock()
        result = unconfigure_power_redundancy_combined(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no power redundancy combined',)
        )
