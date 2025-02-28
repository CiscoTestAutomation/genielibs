from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcpv6.configure import unconfigure_ipv6_dhcp_relay_source
from unittest.mock import Mock


class TestUnconfigureIpv6DhcpRelaySource(TestCase):

    def test_unconfigure_ipv6_dhcp_relay_source(self):
        self.device = Mock()
        result = unconfigure_ipv6_dhcp_relay_source(self.device, 'HundredGigE1/0/27')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['no ipv6 dhcp-relay source-interface HundredGigE1/0/27'],)
        )
