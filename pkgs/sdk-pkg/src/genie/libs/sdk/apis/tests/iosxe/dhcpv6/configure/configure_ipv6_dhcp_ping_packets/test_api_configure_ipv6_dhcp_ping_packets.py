from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcpv6.configure import configure_ipv6_dhcp_ping_packets
from unittest.mock import Mock


class TestConfigureIpv6DhcpPingPackets(TestCase):

    def test_configure_ipv6_dhcp_ping_packets(self):
        self.device = Mock()
        result = configure_ipv6_dhcp_ping_packets(self.device, '5')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('ipv6 dhcp ping packets 5',)
        )
