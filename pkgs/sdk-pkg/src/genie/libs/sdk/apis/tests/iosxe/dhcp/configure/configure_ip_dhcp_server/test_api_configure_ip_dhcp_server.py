from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcp.configure import configure_ip_dhcp_server
from unittest.mock import Mock


class TestConfigureIpDhcpServer(TestCase):

    def test_configure_ip_dhcp_server(self):
        self.device = Mock()
        result = configure_ip_dhcp_server(self.device, '1.1.1.1', None, None, False)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['ip dhcp-server 1.1.1.1'],)
        )
