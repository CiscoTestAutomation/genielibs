from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dot1x.configure import enable_autoconfig
from unittest.mock import Mock


class TestEnableAutoconfig(TestCase):

    def test_enable_autoconfig(self):
        self.device = Mock()
        result = enable_autoconfig(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('uplink autoconfig',)
        )
