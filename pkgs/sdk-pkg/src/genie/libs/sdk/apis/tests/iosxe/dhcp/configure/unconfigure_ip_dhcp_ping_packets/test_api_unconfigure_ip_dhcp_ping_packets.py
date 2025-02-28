from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcp.configure import unconfigure_ip_dhcp_ping_packets
from unittest.mock import Mock


class TestUnconfigureIpDhcpPingPackets(TestCase):

    def test_unconfigure_ip_dhcp_ping_packets(self):
        self.device = Mock()
        result = unconfigure_ip_dhcp_ping_packets(self.device, '5')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no ip dhcp ping packets 5',)
        )
