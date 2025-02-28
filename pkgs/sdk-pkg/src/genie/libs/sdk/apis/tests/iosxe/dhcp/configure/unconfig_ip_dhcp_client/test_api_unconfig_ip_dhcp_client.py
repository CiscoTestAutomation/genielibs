from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcp.configure import unconfig_ip_dhcp_client
from unittest.mock import Mock


class TestUnconfigIpDhcpClient(TestCase):

    def test_unconfig_ip_dhcp_client(self):
        self.device = Mock()
        result = unconfig_ip_dhcp_client(self.device, 'broadcast-flag', None, None, None, None, False, None)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['no ip dhcp-client broadcast-flag'],)
        )
