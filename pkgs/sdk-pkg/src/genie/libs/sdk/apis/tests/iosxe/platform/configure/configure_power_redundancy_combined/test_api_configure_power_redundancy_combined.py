from unittest import TestCase
from genie.libs.sdk.apis.iosxe.platform.configure import configure_power_redundancy_combined
from unittest.mock import Mock


class TestConfigurePowerRedundancyCombined(TestCase):

    def test_configure_power_redundancy_combined(self):
        self.device = Mock()
        result = configure_power_redundancy_combined(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('power redundancy combined',)
        )
