from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcpv6.configure import unconfigure_ipv6_dhcp_relay_option
from unittest.mock import Mock


class TestUnconfigureIpv6DhcpRelayOption(TestCase):

    def test_unconfigure_ipv6_dhcp_relay_option(self):
        self.device = Mock()
        result = unconfigure_ipv6_dhcp_relay_option(self.device, 'client-link-addr')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['no ipv6 dhcp-relay option client-link-addr'],)
        )
