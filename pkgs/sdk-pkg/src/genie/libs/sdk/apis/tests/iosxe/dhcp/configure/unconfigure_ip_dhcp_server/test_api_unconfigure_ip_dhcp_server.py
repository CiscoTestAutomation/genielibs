from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcp.configure import unconfigure_ip_dhcp_server
from unittest.mock import Mock


class TestUnconfigureIpDhcpServer(TestCase):

    def test_unconfigure_ip_dhcp_server(self):
        self.device = Mock()
        result = unconfigure_ip_dhcp_server(self.device, '1.1.1.1', None, None, False)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['no ip dhcp-server 1.1.1.1'],)
        )
