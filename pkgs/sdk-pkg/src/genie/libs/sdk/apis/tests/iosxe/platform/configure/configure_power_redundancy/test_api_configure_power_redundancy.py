from unittest import TestCase
from genie.libs.sdk.apis.iosxe.platform.configure import configure_power_redundancy
from unittest.mock import Mock


class TestConfigurePowerRedundancy(TestCase):

    def test_configure_power_redundancy(self):
        self.device = Mock()
        result = configure_power_redundancy(self.device, '1', 'redundant', 'n+n', '8')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('power redundancy-mode switch 1 redundant n+n 8',)
        )
