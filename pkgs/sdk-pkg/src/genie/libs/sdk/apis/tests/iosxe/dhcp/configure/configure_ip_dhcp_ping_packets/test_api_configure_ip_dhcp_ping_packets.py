from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcp.configure import configure_ip_dhcp_ping_packets
from unittest.mock import Mock


class TestConfigureIpDhcpPingPackets(TestCase):

    def test_configure_ip_dhcp_ping_packets(self):
        self.device = Mock()
        result = configure_ip_dhcp_ping_packets(self.device, '5')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('ip dhcp ping packets 5',)
        )
