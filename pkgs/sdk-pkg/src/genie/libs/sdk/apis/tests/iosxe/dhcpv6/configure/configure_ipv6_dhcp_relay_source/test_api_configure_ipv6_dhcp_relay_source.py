from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcpv6.configure import configure_ipv6_dhcp_relay_source
from unittest.mock import Mock


class TestConfigureIpv6DhcpRelaySource(TestCase):

    def test_configure_ipv6_dhcp_relay_source(self):
        self.device = Mock()
        result = configure_ipv6_dhcp_relay_source(self.device, 'HundredGigE1/0/27')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['ipv6 dhcp-relay source-interface HundredGigE1/0/27'],)
        )
