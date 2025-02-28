from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcp.configure import configure_interface_ip_dhcp_client
from unittest.mock import Mock


class TestConfigureInterfaceIpDhcpClient(TestCase):

    def test_configure_interface_ip_dhcp_client(self):
        self.device = Mock()
        result = configure_interface_ip_dhcp_client(self.device, 'GigabitEthernet1/0/8', 'broadcast-flag', 'set', False)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface GigabitEthernet1/0/8', 'ip dhcp client broadcast-flag set'],)
        )
