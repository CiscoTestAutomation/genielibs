from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcpv6.configure import unconfigure_interface_ipv6_dhcp_client_information
from unittest.mock import Mock


class TestUnconfigureInterfaceIpv6DhcpClientInformation(TestCase):

    def test_unconfigure_interface_ipv6_dhcp_client_information(self):
        self.device = Mock()
        result = unconfigure_interface_ipv6_dhcp_client_information(self.device, 'GigabitEthernet1/0/8', '60')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface GigabitEthernet1/0/8', 'no ipv6 dhcp client information refresh minimum 60'],)
        )
