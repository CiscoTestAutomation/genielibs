from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcp.configure import config_ip_dhcp_client
from unittest.mock import Mock


class TestConfigIpDhcpClient(TestCase):

    def test_config_ip_dhcp_client(self):
        self.device = Mock()
        result = config_ip_dhcp_client(self.device, 'broadcast-flag', None, None, None, None, False, None)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['ip dhcp-client broadcast-flag'],)
        )
