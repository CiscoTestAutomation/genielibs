from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcp.configure import unconfigure_interface_ip_dhcp_client
from unittest.mock import Mock


class TestUnconfigureInterfaceIpDhcpClient(TestCase):

    def test_unconfigure_interface_ip_dhcp_client(self):
        self.device = Mock()
        result = unconfigure_interface_ip_dhcp_client(self.device, 'GigabitEthernet1/0/8', 'broadcast-flag', 'set', False)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface GigabitEthernet1/0/8', 'no ip dhcp client broadcast-flag set'],)
        )
