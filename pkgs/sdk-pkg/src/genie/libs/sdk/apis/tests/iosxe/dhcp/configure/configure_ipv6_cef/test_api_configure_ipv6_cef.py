from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcp.configure import configure_ipv6_cef
from unittest.mock import Mock


class TestConfigureIpv6Cef(TestCase):

    def test_configure_ipv6_cef(self):
        self.device = Mock()
        result = configure_ipv6_cef(self.device, 'distributed')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['ipv6 cef distributed'],)
        )
