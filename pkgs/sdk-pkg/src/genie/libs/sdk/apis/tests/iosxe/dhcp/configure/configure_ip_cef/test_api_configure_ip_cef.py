from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcp.configure import configure_ip_cef
from unittest.mock import Mock


class TestConfigureIpCef(TestCase):

    def test_configure_ip_cef(self):
        self.device = Mock()
        result = configure_ip_cef(self.device, 'distributed')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['ip cef distributed'],)
        )
