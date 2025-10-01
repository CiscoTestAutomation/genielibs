from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcp.configure import unconfigure_ipv6_cef
from unittest.mock import Mock


class TestUnconfigureIpv6Cef(TestCase):

    def test_unconfigure_ipv6_cef(self):
        self.device = Mock()
        result = unconfigure_ipv6_cef(self.device, 'distributed')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['no ipv6 cef distributed'],)
        )
