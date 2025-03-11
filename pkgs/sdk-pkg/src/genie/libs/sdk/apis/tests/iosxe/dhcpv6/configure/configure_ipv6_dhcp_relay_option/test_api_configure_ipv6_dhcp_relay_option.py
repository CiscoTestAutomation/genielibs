from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcpv6.configure import configure_ipv6_dhcp_relay_option
from unittest.mock import Mock


class TestConfigureIpv6DhcpRelayOption(TestCase):

    def test_configure_ipv6_dhcp_relay_option(self):
        self.device = Mock()
        result = configure_ipv6_dhcp_relay_option(self.device, 'client-link-addr')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['ipv6 dhcp-relay option client-link-addr'],)
        )
