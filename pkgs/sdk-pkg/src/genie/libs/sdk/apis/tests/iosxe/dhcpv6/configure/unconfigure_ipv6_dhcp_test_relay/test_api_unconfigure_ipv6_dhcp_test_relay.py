from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcpv6.configure import unconfigure_ipv6_dhcp_test_relay
from unittest.mock import Mock


class TestUnconfigureIpv6DhcpTestRelay(TestCase):

    def test_unconfigure_ipv6_dhcp_test_relay(self):
        self.device = Mock()
        result = unconfigure_ipv6_dhcp_test_relay(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['no ipv6 dhcp test relay packet-control'],)
        )
